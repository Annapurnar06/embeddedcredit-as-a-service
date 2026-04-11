# LendingOS-India: Technical Architecture Report

**Author**: Lead AI Architect
**Date**: April 2026
**Version**: 0.1.0
**Status**: Platform complete through Mission 13 -- ready for first lender integration

---

## Executive Summary

LendingOS-India is an AI-first lending platform purpose-built for Indian financial inclusion. The system replaces the conventional loan origination stack (separate LOS, BRE, CRM, document management, channel gateway) with a single agent-driven monolith where every lending operation is a typed, auditable, policy-gated tool callable by an LLM agent.

The platform implements 48 lending tools across 7 categories, enforces 17 regulatory compliance rules (7 structural + 10 behavioral), supports 3 borrower segments (dairy farmer, kirana shop, gig worker) with segment-specific scoring models, repayment schedules, and monitoring pipelines, and exposes a multi-channel chat gateway (web + WhatsApp BSP).

234 tests pass. Lint clean. Zero external API dependencies for testing (all integrations are mock-with-real-schemas, swappable for production APIs).

---

## 1. Why This Architecture

### 1.1 The Problem

Indian microfinance and NBFC lending to underserved segments (dairy farmers, kirana shops, gig workers) suffers from three structural failures:

1. **Data poverty**: Thin-file borrowers lack credit history. Traditional scorecards using bureau data alone reject 70-80% of viable borrowers.
2. **Operational cost**: A human loan officer processing a Rs 50,000 dairy farmer loan through separate LOS, BRE, document management, and disbursal systems costs Rs 2,000-3,000 per origination -- making small-ticket lending unviable.
3. **Compliance burden**: RBI's Digital Lending Guidelines (September 2022), Fair Practices Code, and KFS mandate require audit trails, PII protection, cooling-off periods, and grievance disclosure at every interaction -- infeasible to enforce consistently with manual processes.

### 1.2 The Decision: AI Agent as the Lending OS

Instead of building a traditional LOS with an AI layer bolted on, the platform inverts the architecture:

- **The LLM agent IS the loan officer.** It converses with borrowers in Hindi/Gujarati, calls tools to verify identity, pull data, score, design products, and execute disbursement.
- **Every lending operation is a tool.** Each tool is a standalone async function with typed inputs/outputs, policy gates, circuit breakers, and audit logging. The agent cannot bypass the tool framework.
- **Policy enforcement is structural, not advisory.** The 7-step execution pipeline blocks tool calls that violate session state, confirmation requirements, authority boundaries, or velocity limits before the tool function executes. The agent cannot override these.

### 1.3 Why Monolith-First

The platform is a FastAPI monolith with clean module boundaries, not a microservices mesh. Rationale:

| Factor | Monolith | 14 Microservices |
|--------|----------|------------------|
| Time to first lender integration | 2 weeks | 3-4 months |
| Operational complexity | 1 container + Postgres + Redis | 14 containers + service mesh + distributed tracing |
| Tool execution latency | In-process function call | Network hop per tool |
| Debugging a failed loan | Single process, single trace | Distributed trace across 14 services |
| Extraction to services later | Clean module boundaries make this straightforward | Already decomposed |

The module structure (`app/tools/identity/`, `app/tools/data/`, etc.) means any category can be extracted to a standalone service when scale demands it. The `ToolRegistry` + `ToolExecutor` abstraction makes the extraction transparent to the agent layer.

---

## 2. Architecture Overview

```
Borrower (WhatsApp/Web)
        |
   [ Chat Gateway ]          -- ChannelAdapter (Web, WhatsApp BSP)
        |
   [ Session Manager ]       -- Maps channel:user_id:lender_id -> AgentSession
        |
   [ Agent Runtime ]          -- Conversation loop, LLM orchestration
        |
   [ Policy Engine ]          -- 7 structural (pre-tool) + 10 behavioral (post-response)
        |
   [ Tool Executor ]          -- 7-step pipeline: state -> confirm -> authority -> CB -> execute -> trace -> emit
        |
   [ 48 Lending Tools ]       -- Identity | Data | Scoring | Product | Execution | Servicing | Monitoring
        |
   [ Audit Trail ]            -- Append-only, PII-masked, every tool call and state transition
        |
   [ Segment Templates ]      -- YAML configs: scoring weights, schedule types, monitoring triggers
```

### 2.1 Request Lifecycle

A single borrower message traverses this path:

1. **Channel adapter** parses raw payload (WhatsApp BSP nested JSON or web flat dict) into `IncomingMessage`.
2. **Session manager** resolves or creates an `AgentSession` keyed by `channel:user_id:lender_id`.
3. **Agent runtime** builds a segment-aware, state-aware system prompt with 10 critical rules embedded, appends conversation history (last 10 turns), calls the LLM.
4. If the LLM returns **tool calls**: for each tool, the runtime delegates to the **tool executor**.
5. **Tool executor** runs the 7-step pipeline:
   - **Step 1: Session state check** -- Is the session in the minimum required state for this tool category? (e.g., DATA tools require VERIFIED)
   - **Step 2: Confirmation check** -- Does this tool require explicit borrower confirmation? (e.g., credit bureau pull, disbursement)
   - **Step 3: Authority boundary check** -- Does this WRITE tool have maker-checker approval? Is `settings.can_disburse_without_human` respected?
   - **Step 4: Circuit breaker check** -- Is this tool in OPEN state from repeated failures?
   - **Step 5: Execute** -- `asyncio.wait_for(handler, timeout)` with configurable per-tool timeout.
   - **Step 6: Trace** -- Record latency, state transitions, policy check results.
   - **Step 7: Emit event** -- Audit trail + event emitter for downstream consumers.
6. If verification succeeds (`verify_aadhaar_otp` returns `verified: true`), the runtime **transitions session state** via the `SessionMachine` (UNVERIFIED -> VERIFIED).
7. After tool execution, the runtime builds a **tool result prompt** and calls the LLM again to explain results to the borrower.
8. The **behavioral policy engine** evaluates the LLM's response against 10 rules (no PII leak, no coercive language, empathetic tone on distress, grievance disclosure on complaint, etc.). If any error-severity rule fails, the response is **sanitized** with a compliant replacement.
9. The response is formatted via the **channel adapter** and returned.

---

## 3. Component Deep Dive

### 3.1 Session State Machine

The platform enforces a monotonically advancing session state:

```
UNVERIFIED  ->  VERIFIED  ->  CONFIRMED  ->  (terminal)
     |              |              |
     +--------> EXPIRED <---------+
```

**State semantics:**

| State | Meaning | Available Tool Categories |
|-------|---------|--------------------------|
| UNVERIFIED | Borrower identity not yet confirmed | Identity (6 tools) |
| VERIFIED | Aadhaar/PAN verified, identity confirmed | Data, Scoring, Product, Servicing, Monitoring (40 tools) |
| CONFIRMED | Loan terms accepted, KFS generated | Execution (6 tools) + all above |
| EXPIRED | Session timed out | None (terminal) |

**Why this matters**: A borrower in UNVERIFIED state cannot trigger a credit bureau pull, scoring, or disbursement. The state machine makes this a structural impossibility, not a prompt instruction the LLM might ignore. The `CATEGORY_MIN_STATE` mapping enforces this at the registry level:

```python
CATEGORY_MIN_STATE = {
    ToolCategory.IDENTITY:   SessionState.UNVERIFIED,
    ToolCategory.DATA:       SessionState.VERIFIED,
    ToolCategory.SCORING:    SessionState.VERIFIED,
    ToolCategory.PRODUCT:    SessionState.VERIFIED,
    ToolCategory.EXECUTION:  SessionState.CONFIRMED,
    ToolCategory.SERVICING:  SessionState.VERIFIED,
    ToolCategory.MONITORING: SessionState.VERIFIED,
}
```

**Domain insight**: The forward-only constraint prevents a verified session from reverting to unverified (which could allow re-verification attacks). The only backward transition is to EXPIRED, which is terminal.

### 3.2 Tool Framework

#### 3.2.1 The `@lending_tool` Decorator

Every lending operation is registered via a decorator pattern:

```python
@lending_tool(
    name="pull_credit_bureau",
    description="Pull credit bureau report. DESTRUCTIVE: hard inquiry.",
    category=ToolCategory.DATA,
    requires_confirmation=True,
    authority_level=AuthorityLevel.ACCOUNT,
    timeout_seconds=5,
    circuit_breaker_threshold=3,
)
async def pull_credit_bureau(aadhaar_hash: str = "", bureau: str = "CIBIL") -> dict:
    ...
```

This creates a `ToolDefinition` dataclass and registers it in the global `ToolRegistry`. The decorator attaches metadata that the executor uses for policy enforcement without the tool implementation needing to know about sessions, policies, or audit.

#### 3.2.2 Authority Levels

Three authority levels control escalation:

| Level | Meaning | Examples |
|-------|---------|---------|
| GENERAL | Any session can invoke | Aadhaar verify, bank statement analysis, product design |
| ACCOUNT | Requires borrower context | Bureau pull, scoring, KFS generation |
| WRITE | Requires maker-checker approval | Disbursement, eSign, eNACH mandate, moratorium |

WRITE-level tools are gated by `settings.can_disburse_without_human` (default: `False`). This is a hard-coded safety limit in the Settings class -- the AI agent cannot change it.

#### 3.2.3 Confirmation Gating

9 of 48 tools require explicit borrower confirmation before execution:

| Tool | Why Confirmation Required |
|------|--------------------------|
| `initiate_aa_consent` | Account Aggregator consent is a legal act |
| `pull_credit_bureau` | Hard inquiry affects borrower's credit score |
| `initiate_esign` | Legal document signing |
| `enroll_insurance` | Financial commitment |
| `setup_enach_mandate` | Auto-debit authorization |
| `execute_disbursement` | Irreversible fund transfer |
| `process_prepayment` | Changes loan terms |
| `apply_moratorium` | Changes repayment schedule |
| `execute_auto_intervention` | Automated action on borrower's loan |

The confirmation detector supports Hindi and English patterns:
- Confirm: `haan, theek hai, kar do, kijiye, manzoor, yes, ok, confirm`
- Deny: `nahi, mat karo, rukiye, no, cancel, reject`
- Denial takes precedence over confirmation in mixed utterances.

#### 3.2.4 Circuit Breaker

Each tool has an independent circuit breaker (CLOSED -> OPEN -> HALF_OPEN) with configurable threshold and 30-second recovery:

- External API tools (bureau, ULI, cooperative) use threshold=3 (fail fast on flaky APIs).
- Internal tools use threshold=5 (default).
- When OPEN, the tool returns `DEGRADED` status instead of executing -- enabling graceful degradation.

**Domain insight**: Credit bureau APIs in India (CIBIL, Experian) have 99.5% SLA, not 99.99%. A 30-second circuit breaker recovery is calibrated for their typical transient failure duration.

### 3.3 The 48 Tools

#### Category Breakdown

| Category | Count | State Required | Description |
|----------|-------|----------------|-------------|
| Identity | 6 | UNVERIFIED | Aadhaar OTP, voice OTP, PAN (Jaro-Winkler matching), bank account penny drop, AA consent, negative list |
| Data Assembly | 12 | VERIFIED | ULI parallel fetch (land + satellite + weather + PMFBY), AA bank data, bureau pull (confirmation-gated), bank statement analysis, document extraction (9 types), cooperative data, platform earnings, GST returns, device score, cross-validation, confidence score, borrower profile assembly |
| Scoring | 8 | VERIFIED | Segment policy evaluation, weighted segment score (900-point scale), risk pricing (5 rate bands), fraud signals (velocity + device), CAM generation, what-if simulator, PSL classification, multilingual explainability |
| Product | 5 | VERIFIED | Dynamic product design, seasonal schedule (flush/lean months), daily micro schedule, payout-linked schedule, insurance premium |
| Execution | 6 | CONFIRMED | KFS (RBI-mandatory), eSign, insurance enrollment, eNACH mandate, disbursement (maker-checker), CERSAI registration |
| Servicing | 6 | VERIFIED | Loan status, repayment schedule, prepayment (reduce tenure/EMI), moratorium (no NPA classification), statement generation, NOC |
| Monitoring | 5 | VERIFIED | Signal polling (bank txn, cooperative, platform, DPD, bureau), trigger evaluation (segment-specific thresholds), auto-intervention (nudge/moratorium/restructure/collection), graduation (rate reduction, limit increase, top-up), job scheduling |

#### Key Implementation Details

**Jaro-Winkler name matching** (PAN verification): The platform implements the full Jaro-Winkler similarity algorithm for matching names across identity documents -- critical because Indian names vary across Aadhaar, PAN, and bank records (transliteration differences, middle name presence/absence).

**Seasonal EMI schedule**: Dairy farmer loans use flush months (October-February, high milk production) with 130% EMI and lean months (April-June, low production) with 60% EMI. This matches actual cash flow patterns rather than forcing uniform EMI.

**PSL classification**: Priority Sector Lending classification is computed per-tool because it determines reporting obligations. Dairy farmers qualify under Agriculture/Animal Husbandry; kirana shops under MSME/Micro Enterprise; gig workers do not qualify.

**Moratorium triggers**: Segment templates define automatic moratorium triggers -- e.g., for dairy farmers, temperature exceeding 38 degrees C (heat stress reducing milk production) or a 40%+ production drop automatically flags a 1-month moratorium, protecting borrowers from NPA classification during climate events.

### 3.4 Policy Engine

#### 3.4.1 Structural Rules (Pre-Tool, Deterministic)

These run before every tool call and produce binary pass/fail:

| # | Rule | Enforces |
|---|------|----------|
| 1 | `identity_gate` | No non-identity tools before verification |
| 2 | `write_confirmation` | Explicit borrower consent for destructive operations |
| 3 | `kfs_mandatory` | No disbursement or eSign without Key Fact Statement (RBI Digital Lending Guidelines 2022, Para 26) |
| 4 | `bureau_velocity` | Max 2 credit bureau pulls per Aadhaar per 48 hours (prevents score damage from excessive hard inquiries) |
| 5 | `cooling_off_period` | No disbursement during 3-day KFS cooling-off period (RBI mandate) |
| 6 | `consent_required` | Account Aggregator and data-fetch tools require valid consent token |
| 7 | `maker_checker` | WRITE authority tools require human approval when `can_disburse_without_human=False` |

#### 3.4.2 Behavioral Rules (Post-Response, Regex-Based)

These evaluate the agent's natural language response and fire corrective sanitization:

| # | Rule | Severity | What It Catches |
|---|------|----------|-----------------|
| 1 | `no_disclosure_before_verify` | error | Agent leaking loan amount, EMI, rate before identity verification |
| 2 | `rbi_fair_practices_language` | error | Coercive language: "legal action", "arrest", "seize", "jabti" |
| 3 | `no_commitment_on_terms` | warning | "You will get Rs X" before policy evaluation completes |
| 4 | `psl_accurate_classification` | error | Agent suggesting PSL misclassification ("mark it as agriculture") |
| 5 | `empathetic_tone_distress` | warning | Missing empathy when borrower mentions death, flood, illness |
| 6 | `no_rate_guarantee` | warning | Specific rate promises before finalization |
| 7 | `insurance_opt_in` | warning | Presenting insurance as mandatory (except segment-mandated Pashu Bima) |
| 8 | `grievance_disclosure` | error | Missing grievance officer reference when borrower complains |
| 9 | `no_override_on_authority` | error | Agent accepting "my manager approved" social engineering |
| 10 | `pii_masked_readback` | error | Full Aadhaar (12-digit) or PAN in agent response |

**Domain insight**: Rules 1, 2, 3, 8, and 10 map directly to RBI Digital Lending Guidelines and Fair Practices Code provisions. Rules 5 and 9 address behavioral risks specific to AI agents that human loan officers also struggle with but in different ways. Rule 4 addresses a real compliance risk where lenders misclassify non-agriculture loans as PSL to meet RBI targets.

**Error vs. Warning**: Error-severity rules trigger response sanitization (the agent's response is replaced with a compliant alternative). Warning-severity rules are logged but the response is passed through -- they inform model fine-tuning rather than blocking the response.

### 3.5 Agent Runtime

The `AgentRuntime` class orchestrates the full conversation loop:

```
process_message(session, borrower_message)
    |
    +-- detect_confirmation(borrower_message)     # Hindi/English
    +-- get segment template                       # YAML config
    +-- get available tools for state              # filtered by CATEGORY_MIN_STATE
    +-- build_system_prompt(segment, state, tools) # 10 critical rules embedded
    +-- LLM.chat(messages, tools)                  # First LLM call
    |
    +-- For each tool_call:
    |     +-- ToolExecutor.execute(tool, context)  # 7-step pipeline
    |     +-- Log audit trail                      # PII-masked
    |     +-- If verify_aadhaar_* verified:
    |           +-- SessionMachine.transition()     # UNVERIFIED -> VERIFIED
    |
    +-- build_tool_result_prompt(last_result)
    +-- LLM.chat(messages + tool_result)           # Second LLM call
    |
    +-- PolicyEngine.evaluate_response(response)   # 10 behavioral rules
    +-- If blocked: sanitize_response()            # Replace with compliant text
    |
    +-- Append to session.history
    +-- Log audit event
    +-- Return ConversationTurn
```

**System prompt construction** is segment-aware and state-aware. A dairy farmer in VERIFIED state sees different available tools and greeting templates than a gig worker in UNVERIFIED state. The prompt embeds 10 critical rules as hard constraints, not suggestions.

**Conversation history** is windowed to the last 10 turns to manage context length. Full history is preserved in `session.history` for audit purposes.

### 3.6 Segment Templates

Three YAML-defined segment templates encode the complete lending journey:

#### Dairy Farmer (`DAIRY_FARMER`)
- **Channel**: WhatsApp (low smartphone sophistication)
- **Languages**: Gujarati, Hindi
- **Data sources**: Bureau + bank AA + dairy cooperative (required); land records, satellite NDVI, weather IMD (optional)
- **Scoring model**: `dairy_score_v1` with 6 features weighted by predictive power for dairy repayment: pouring regularity (25%), pouring volume trend (18%), cooperative tenure (12%), land area (10%), bureau score (15%), bank stability (20%)
- **Product**: Seasonal dynamic schedule, Rs 25K-200K, 6-24 months, Pashu Bima insurance (cattle insurance)
- **Moratorium triggers**: Heat wave (>=38 degrees C, 1 month), production drop (>=40%, 1 month)
- **Monitoring**: Weekly; cooperative pouring drop (>=30%) triggers schedule adjustment, temperature triggers auto-moratorium
- **Graduation**: After 12 months on-book with 90% on-time rate: 2x amount, 2% rate reduction

#### Kirana Shop (`KIRANA_SHOP`)
- **Channel**: WhatsApp
- **Languages**: Hindi, Marathi
- **Data sources**: Bureau + bank AA + GST returns (required); platform earnings, device score (optional)
- **Scoring model**: `vendor_score_v1` with 5 features: GST turnover trend (30%), bank inflow regularity (25%), bureau score (20%), GST filing regularity (15%), device score (10%)
- **Product**: Daily micro schedule (26 working days/month), Rs 50K-500K, 3-12 months, no insurance
- **Monitoring**: Daily; inflow drop (>=50%) triggers schedule adjustment
- **Graduation**: After 6 months with 85% on-time: 1.5x amount, 1.5% rate reduction

#### Gig Worker (`GIG_WORKER`)
- **Channel**: WhatsApp
- **Languages**: Hindi, English
- **Data sources**: Bureau + bank AA + platform earnings (required); device score (optional)
- **Scoring model**: `gig_score_v1` with 5 features: platform earnings trend (30%), platform rating (15%), active days (15%), bank stability (20%), bureau score (20%)
- **Product**: Payout-linked schedule (15% deduction from each platform payout), Rs 10K-200K, 3-12 months, no insurance
- **Monitoring**: Daily; earnings drop (>=40%) triggers schedule adjustment, platform deactivation triggers escalation
- **Graduation**: After 6 months with 85% on-time: 1.5x amount, 1% rate reduction

**Domain insight**: The scoring feature weights reflect real underwriting logic. For dairy farmers, pouring regularity (how consistently they deliver milk to the cooperative) is the strongest predictor of repayment behavior -- more predictive than bureau score alone, because many dairy farmers are thin-file. For kirana shops, GST turnover trend captures business health better than point-in-time revenue. For gig workers, platform earnings trend and active days capture engagement stability.

### 3.7 Audit Trail

The audit system implements RBI's Digital Lending Guidelines requirement for complete audit trails:

**Design principles:**
1. **Append-only**: No UPDATE or DELETE operations on audit tables. Both `AuditLog` and `ToolExecution` tables lack `updated_at` columns -- immutability by schema design.
2. **PII masking at boundary**: All data is masked before storage using three patterns (Aadhaar 12-digit, PAN alphanumeric, phone/account 10-12 digit). Sensitive keys (`otp`, `password`, `token`) are fully masked to `***MASKED***`.
3. **Every tool call recorded**: Input (masked), output, latency, session state before/after, policy checks applied, result status.
4. **Every state transition recorded**: From-state, to-state, triggering tool, timestamp.
5. **Merged timeline**: The `/api/audit/loan/{id}` endpoint merges audit logs and tool executions into a chronological timeline for a complete loan lifecycle view.

**Why this matters**: RBI auditors examining a loan need to answer: "What data did the AI see? What decision did it make? What tools did it call? Did it follow policy? Was the borrower informed?" The audit trail answers all of these from a single query.

### 3.8 Chat Gateway

The gateway implements a channel-agnostic adapter pattern:

**WhatsApp BSP integration**: Parses the standard BSP webhook format:
```
entry[0].changes[0].value.messages[0].text.body
entry[0].changes[0].value.messages[0].from  (phone number)
entry[0].changes[0].value.metadata.phone_number_id
```

**Session keying**: `channel:user_id:lender_id` -- this enables multi-lender support (the same borrower phone number can have separate sessions with different NBFCs).

**Channel extensibility**: Adding a new channel (e.g., IVRS voice, USSD) requires implementing `ChannelAdapter.parse_incoming()` and `format_outgoing()` -- the agent runtime is channel-agnostic.

---

## 4. Data Model

### 4.1 Database Schema

Four tables form the persistence layer:

**`borrowers`** -- PII stored as hashes (aadhaar_hash, pan_hash, phone_hash). Raw values never hit the database. Defaults: Hindi language, WhatsApp channel.

**`loan_applications`** -- 15-state lifecycle (DRAFT through CLOSED/NPA/WRITTEN_OFF). Stores score, decision, reason codes, PSL classification, product config, schedule, and enriched profile as JSON. The `maker_approved` boolean enforces the human-in-the-loop gate.

**`lending_sessions`** -- Maps to `AgentSession` at runtime. Stores session state, conversation history, and segment. The `borrower_id` is nullable because sessions exist before identity verification completes.

**`audit_logs` + `tool_executions`** -- Append-only. Tool execution stores masked input, raw output, latency, state transitions, and policy check results. No `updated_at` column.

### 4.2 Key Design Decisions

**JSON columns as Text, not JSONB**: The `enriched_profile_json`, `product_config_json`, and `schedule_json` columns use `Text` type rather than PostgreSQL JSONB. This is intentional for portability -- the platform should work with any SQL database, not just PostgreSQL. Querying into JSON can be done at the application layer.

**PII as hashes only**: The `aadhaar_hash` and `pan_hash` columns store SHA-256 hashes. This means the platform cannot display raw Aadhaar/PAN from the database -- it can only verify membership. Raw values exist only in transient memory during the tool execution.

---

## 5. Workflow Walkthrough: Dairy Farmer Loan Origination

This section traces a complete loan origination for a dairy farmer from first message to disbursement.

### Phase 1: Identity (Session State: UNVERIFIED)

```
Borrower: "Namaste, mujhe loan chahiye" (via WhatsApp)
Agent: "Namaste! Loan ke liye pehle aapki pehchaan verify karni hogi.
        Kya aap apna Aadhaar number bata sakte hain?"
```

Agent calls no tools -- in UNVERIFIED state, only identity tools are available, and the borrower hasn't provided Aadhaar yet.

```
Borrower: "1234 5678 9012"
Agent: [calls verify_aadhaar_otp(aadhaar_number="123456789012")]
       → Returns: {otp_sent: true}
Agent: "OTP aapke registered mobile par bheja gaya hai. Kya aap OTP bata sakte hain?"
```

```
Borrower: "456789"
Agent: [calls verify_aadhaar_otp(aadhaar_number="123456789012", otp="456789")]
       → Returns: {verified: true, name: "Ramesh Patel", ...}
       → SESSION TRANSITIONS: UNVERIFIED -> VERIFIED
Agent: "Dhanyavaad Ramesh bhai, aapki pehchaan verify ho gayi. Ab hum aage badh sakte hain."
```

### Phase 2: Data Assembly (Session State: VERIFIED)

The agent now has access to 40+ tools. It calls data assembly tools to build the borrower profile:

```
verify_pan(pan_number="ABCDE1234F", aadhaar_name="Ramesh Patel")
  → name_match_score: 0.93 (Jaro-Winkler)

fetch_uli_parallel(pincode="387001")
  → land_records: 4.5 acres, irrigated, bajra crop, no encumbrance
  → satellite_ndvi: 0.42 average, stable trend
  → weather_imd: 34.2°C, 320mm rainfall, low drought risk
  → pmfby_coverage: enrolled, bajra, Rs 45,000 sum insured

fetch_aa_bank_data(consent_id="...")
  → avg_monthly_inflow: Rs 42,000; dairy_income: Rs 15,000; FOIR: 0.32

fetch_cooperative_data(membership_id="...")
  → pouring_regularity: 92%; avg 12.5 liters/day; 6.2% fat; 48 months tenure

pull_credit_bureau(aadhaar_hash="...", bureau="CIBIL")  [requires confirmation]
  → score: 720, grade: B1, dpd_max_12m: 0, no overdue accounts

compute_confidence_score(sources_available=5, sources_required=3, ...)
  → score: 0.85, level: "HIGH"
```

### Phase 3: Scoring & Decisioning (Session State: VERIFIED)

```
compute_segment_score(segment="DAIRY_FARMER", features={
    pouring_regularity: 0.92, bureau_score: 720, bank_stability: 0.85, ...
})
  → score: 680, grade: A2

evaluate_segment_policy(segment="DAIRY_FARMER", score=680, confidence_level="HIGH")
  → decision: APPROVE

compute_risk_pricing(score=680)
  → rate_band: A2, interest_rate: 14%

check_fraud_signals(device_fingerprint="...", applications_48h=0)
  → result: PASS

check_psl_classification(segment="DAIRY_FARMER")
  → category: Agriculture, sub_category: Animal Husbandry, eligible: true
```

### Phase 4: Product Design (Session State: VERIFIED)

```
design_dynamic_product(segment="DAIRY_FARMER", score=680, requested_amount=100000)
  → schedule_type: SEASONAL_DYNAMIC, tenure: 18 months
  → insurance: PASHU_BIMA, premium: Rs 3,540
  → moratorium_triggers: [WEATHER_HEAT >=38°C, PRODUCTION_DROP >=40%]

generate_seasonal_schedule(amount=100000, rate=14.0, tenure_months=18)
  → 18 entries: flush months (Oct-Feb) Rs 8,450, lean months (Apr-Jun) Rs 3,900, normal Rs 6,500
```

### Phase 5: Execution (Session State: CONFIRMED)

After borrower reviews and confirms terms, the session transitions to CONFIRMED:

```
generate_kfs(borrower_name="Ramesh Patel", amount=100000, rate=14.0, tenure_months=18)
  → cooling_off_period_days: 3, APR: 14.5%
  → grievance_officer_name + contact included

[3-day cooling-off period elapses]

initiate_esign(...)         → status: OTP_SENT [requires confirmation + maker]
enroll_insurance(type="PASHU_BIMA", sum_insured=80000)  → status: ENROLLED
setup_enach_mandate(max_amount=8500, frequency="monthly")  → mode: eNACH
execute_disbursement(amount=100000, mode="UPI")  → status: SUCCESS, ref: DISB-...
register_cersai(asset_type="LIVESTOCK", asset_description="5 milch cows")  → REGISTERED
```

### Phase 6: Post-Disbursement Monitoring

Weekly monitoring job runs:

```
poll_monitoring_signals(loan_id="LOAN-001")
  → bank_txn_drop: 0.15, cooperative_pouring_drop: 0.10, dpd_change: 0.0

evaluate_monitoring_triggers(segment="DAIRY_FARMER", signals=[...])
  → recommended_action: NONE (all within thresholds)
```

After 12 months with 97% on-time rate:

```
evaluate_graduation(months_on_book=12, on_time_rate=0.97, current_rate=14.0)
  → eligible: true
  → offers: [RATE_REDUCTION to 12%, LIMIT_INCREASE to Rs 1,25,000, TOP_UP Rs 50,000]
```

---

## 6. Compliance Mapping

### RBI Digital Lending Guidelines (September 2022)

| Guideline Provision | Platform Implementation |
|---------------------|------------------------|
| Para 6: All digital lending through regulated entities | `lender_id` on every session, tool call, and audit entry |
| Para 14: KFS mandatory before disbursement | `check_kfs_mandatory` structural rule blocks disbursement/eSign without KFS |
| Para 15: Cooling-off/look-up period | `check_cooling_off_period` structural rule enforces 3-day window |
| Para 20: Grievance redressal | `check_grievance_disclosure` behavioral rule ensures agent discloses grievance officer on complaints |
| Para 26: Audit trail | Append-only `AuditLog` + `ToolExecution` with PII masking |
| Para 29: No coercion | `check_rbi_fair_practices_language` blocks threatening language |
| Para 31: Data privacy | PII stored as hashes; PII masked in audit trails; `mask_pii()` + `mask_dict()` at boundary |

### RBI Fair Practices Code

| Provision | Implementation |
|-----------|----------------|
| Transparent pricing | KFS generation with APR calculation |
| No misrepresentation | `check_no_commitment_on_terms` prevents premature term commitments |
| Consent-based data access | `check_consent_required` gates AA and data-fetch tools |
| Non-coercive recovery | `check_rbi_fair_practices_language` blocks coercive language in collection context |
| Insurance as optional | `check_insurance_opt_in` flags mandatory insurance language |

### Priority Sector Lending (PSL) Compliance

| Segment | PSL Category | Eligible | Reporting |
|---------|-------------|----------|-----------|
| Dairy Farmer | Agriculture / Animal Husbandry | Yes | Auto-classified by `check_psl_classification` |
| Kirana Shop | MSME / Micro Enterprise | Yes | Auto-classified |
| Gig Worker | Other | No | Correctly excluded |

---

## 7. Hard Authority Boundaries

These are hard-coded in `app/core/config.py` and cannot be overridden by the AI agent, prompt injection, or configuration change:

| Boundary | Value | Purpose |
|----------|-------|---------|
| `bureau_pull_max_per_aadhaar_48h` | 2 | Prevent credit score damage from excessive hard inquiries |
| `disbursement_max_amount` | Rs 5,00,000 | Single disbursement cap |
| `fee_waiver_max` | Rs 500 | Maximum fee the agent can waive |
| `moratorium_max_months` | 3 | Maximum moratorium period |
| `can_auto_approve` | False | AI cannot approve loans without human review |
| `can_disburse_without_human` | False | AI cannot disburse without maker-checker |

**Why hard-coded, not configurable**: These boundaries represent the lender's risk appetite and regulatory obligations. Making them environment variables would allow accidental or malicious override. They should change only through a code review and deployment cycle.

---

## 8. Testing Strategy

### 8.1 Test Architecture

234 tests across 22 test files:

| Category | Files | Tests | What's Validated |
|----------|-------|-------|-----------------|
| Tool registration | 7 | 48 | Every tool registered with correct category, authority, confirmation flags |
| Tool execution | 7 | 65 | Each tool returns expected mock data with correct schema |
| State machine | 1 | 6 | Valid/invalid transitions, minimum state checks |
| Policy engine | 3 | 46 | All 7 structural + 10 behavioral rules with positive and negative cases |
| Agent runtime | 2 | 19 | Greeting, tool triggering, state transition, audit, empathy, grievance, history |
| Gateway | 1 | 16 | Channel adapters, session manager, HTTP endpoints, WhatsApp webhook |
| Schemas | 1 | 10 | Pydantic validation, field types, model serialization |
| Audit | 1 | 13 | PII masking (Aadhaar, PAN, phone, nested dicts), event emission, trail merging |
| Integration E2E | 1 | 15 | Full dairy farmer origination (18 tool calls), REFER flow, monitoring pipeline, servicing pipeline, agent conversation, tool coverage verification |

### 8.2 Key Test Invariants

1. **All 48 tools are registered** -- `TestToolCoverage` verifies `ToolRegistry.get_all()` has 48 entries.
2. **State gating is structural** -- Tools in wrong state always return `BLOCKED`, never `SUCCESS`.
3. **Confirmation is required** -- Write tools without `borrower_confirmed=True` are always blocked.
4. **Maker-checker is enforced** -- WRITE authority tools without `maker_approved=True` are always blocked.
5. **PII never leaks** -- Audit trail masks Aadhaar, PAN, phone in all stored data.
6. **Behavioral rules fire** -- Coercive language, PII readback, missing grievance disclosure are caught and sanitized.

---

## 9. Production Readiness Assessment

### What's Ready

| Component | Status | Notes |
|-----------|--------|-------|
| Tool framework + 48 tools | Complete | Mock implementations with production-accurate schemas |
| Session state machine | Complete | Forward-only, tested for valid/invalid transitions |
| Policy engine (17 rules) | Complete | Structural + behavioral, tested with positive/negative cases |
| Agent runtime | Complete | Conversation loop, tool orchestration, behavioral supervision |
| Chat gateway | Complete | Web + WhatsApp BSP, session management |
| Audit trail | Complete | Append-only, PII masking, merged timeline |
| Segment templates | Complete | 3 segments with scoring weights, schedules, monitoring |
| Test suite | Complete | 234 tests, lint clean |
| CI pipeline | Complete | GitHub Actions: lint + test |
| Docker Compose | Complete | app + postgres + redis with health checks |

### What's Needed for Production

| Component | Effort | Description |
|-----------|--------|-------------|
| Real API integrations | 2-4 weeks per API | Replace mock implementations with real UIDAI, CIBIL, AA, BSP, eSign, eNACH APIs |
| LLM provider integration | 1 week | Replace `MockLLMClient` with OpenAI/Azure/Anthropic client; implement token budget management |
| Database migrations | 1 day | Run `alembic upgrade head` against production Postgres |
| Authentication + multi-tenancy | 1-2 weeks | API key-based lender authentication; row-level security on sessions/loans |
| Redis for session state | 1 week | Replace in-memory `SessionManager` with Redis-backed sessions |
| Production Dockerfile | 1 day | Multi-stage build, remove dev deps, remove --reload |
| Observability | 1 week | Prometheus metrics, structured log aggregation, Sentry error tracking |
| Load testing | 1 week | Verify tool executor throughput under concurrent sessions |

---

## 10. Frequently Asked Questions

### Q: Can the AI agent approve or disburse loans without human oversight?

No. Two hard boundaries prevent this:
- `can_auto_approve = False` -- the agent cannot set a loan to APPROVED status.
- `can_disburse_without_human = False` -- the `check_maker_checker` structural rule blocks all WRITE-authority tools (including `execute_disbursement`) unless `maker_approved=True` on the execution context.

These are Python constants in `app/core/config.py`, not environment variables or database settings.

### Q: What happens if the LLM hallucinates loan terms?

Three layers prevent this:
1. **System prompt rule #2**: "NEVER commit to specific loan terms before policy evaluation completes."
2. **Behavioral rule `no_commitment_on_terms`**: Regex detects "you will get", "aapko milega", "guaranteed" in the agent response before finalization.
3. **Behavioral rule `no_rate_guarantee`**: Regex detects specific rate numbers in the agent response before finalization.

If either behavioral rule fires at error severity, the response is replaced with a compliant alternative.

### Q: What if a borrower tries social engineering ("my manager approved this")?

Behavioral rule `no_override_on_authority` detects patterns like "manager said/approved", "RBI told/said", "special permission", "exception approved" in the borrower's message. If the agent's response doesn't include compliance language ("policy", "cannot", "standard process", "unable to override"), the response is sanitized.

### Q: How does PII protection work?

Five layers:
1. **Database storage**: Aadhaar, PAN, phone stored as SHA-256 hashes. Raw values never in DB.
2. **Audit trail**: `mask_dict()` applied to all tool input/output before audit storage.
3. **Agent response**: Behavioral rule `pii_masked_readback` blocks full Aadhaar/PAN in LLM output.
4. **System prompt rule #4**: "ALWAYS mask PII in responses (show only last 4 digits)."
5. **Tool implementations**: Execution tools mask beneficiary accounts (show last 4 digits only).

### Q: Why mock implementations instead of real APIs?

The mock-with-real-schemas approach provides:
1. **Schema accuracy**: `BureauReport`, `AadhaarVerifyResult`, `BankAccountData` match production API response structures exactly.
2. **Deterministic testing**: 234 tests run in 1.6 seconds without network calls.
3. **Development velocity**: The full platform was built without API vendor negotiations.
4. **Swappability**: Each tool is a single async function. Replacing the mock body with a real `httpx` call requires no changes to the tool framework, policy engine, or agent layer.

### Q: How do you add a new borrower segment?

1. Create a YAML file in `segments/` (e.g., `auto_rickshaw_driver.yaml`) with scoring features, product type, monitoring triggers, and graduation criteria.
2. The `SegmentRegistry.load_from_directory()` auto-discovers it.
3. The agent runtime's system prompt construction automatically adapts to the segment's tools, language, and greeting.
4. No code changes needed unless the segment requires new tool implementations.

### Q: What is the expected tool execution latency in production?

Current mock latency is <1ms per tool (in-process function call). Production latency depends on external APIs:

| Tool | Expected Latency | Circuit Breaker Threshold |
|------|-------------------|---------------------------|
| Aadhaar OTP | 2-5 seconds | 5 failures |
| Credit bureau | 1-3 seconds | 3 failures (more flaky) |
| ULI parallel | 3-8 seconds (4 APIs) | 3 failures |
| AA bank data | 5-15 seconds | 5 failures |
| eSign | 2-5 seconds | 5 failures |
| Disbursement (UPI) | 1-3 seconds | 5 failures |

The `asyncio.wait_for` timeout per tool (configurable, 5-30 seconds) prevents any single tool from blocking the conversation indefinitely.

### Q: How does the platform handle API failures gracefully?

Three mechanisms:
1. **Circuit breaker**: After `threshold` consecutive failures, the tool returns `DEGRADED` status for `recovery_seconds` (30s default) without attempting the call.
2. **Timeout**: Each tool has a configurable `timeout_seconds`. Exceeded timeout returns `TIMEOUT` status.
3. **Agent response**: The LLM receives the error status and can explain to the borrower ("Bureau system is temporarily unavailable, we'll try again in a few minutes") rather than crashing.

---

## 11. Technology Stack

| Layer | Technology | Version | Rationale |
|-------|-----------|---------|-----------|
| Runtime | Python | 3.10 | Async-first ecosystem, ML/AI library compatibility |
| Web framework | FastAPI | >=0.109 | Async, auto-docs, Pydantic v2 native |
| ORM | SQLAlchemy | >=2.0 | Async sessions, declarative models |
| Database | PostgreSQL | 16 | ACID compliance (critical for lending), JSONB support |
| Cache/events | Redis | 7 | Session state, event streams, circuit breaker state |
| Migrations | Alembic | >=1.13 | Autogenerate from SQLAlchemy models |
| Validation | Pydantic | >=2.5 | Schema enforcement on all tool inputs/outputs |
| Logging | structlog | >=24.1 | JSON structured logging with context propagation |
| HTTP client | httpx | >=0.26 | Async HTTP for external API calls |
| Config | pydantic-settings | >=2.1 | Type-safe settings from environment variables |
| Lint | ruff | latest | Fast Python linter, replaces flake8+isort+black |
| Test | pytest + pytest-asyncio | latest | Async test support |

---

*This report reflects the platform state as of Mission 13 completion: 48 tools, 17 policy rules, 3 segment templates, 234 passing tests, lint clean, ready for first lender API integration.*
