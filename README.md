# Embedded Credit as a Service

**An AI-native lending operating system for India's 300 million underserved borrowers.**

> A dairy farmer in Banaskantha earns Rs 42,000 a month pouring milk at a cooperative.
> His income is seasonal -- flush in winter, lean in summer. He has no salary slip,
> no ITR, no credit score above 300. Every bank has turned him away.
>
> But his cooperative pouring record tells a story: 92% regularity, 48 months of
> membership, 6.2% fat content (above average). His bank account shows stable
> deposits matching cooperative payout dates. Satellite imagery shows his 4.5 acres
> are irrigated and planted.
>
> He is not uncreditworthy. He is **differently creditworthy**.
>
> This platform reads that story -- through WhatsApp, in Gujarati, in 15 minutes --
> and turns it into a Rs 1,00,000 seasonal loan with EMIs that rise when his milk
> production rises and fall when it falls. No branch visit. No paperwork. No
> rejection at the door.
>
> That is what we are building.

---

## What This Platform Is

Embedded Credit as a Service is a full-stack AI lending infrastructure that replaces the conventional loan origination stack -- separate LOS, BRE, CRM, document management, disbursal systems -- with a single agent-driven platform where every lending operation is a typed, auditable, policy-gated tool callable by an LLM agent over WhatsApp.

It is not a chatbot bolted onto a legacy LOS. It is the LOS. The agent IS the loan officer.

The platform originates, underwrites, disburses, services, and monitors microloans for **38 borrower segments** across agriculture, micro-enterprise, gig economy, asset financing, and social lending -- each with segment-specific scoring models, repayment schedules, monitoring triggers, and culturally tuned communication.

```
                              ┌──────────────────────────┐
                              │     BORROWER             │
                              │  (WhatsApp / Web)        │
                              └────────────┬─────────────┘
                                           │
                              ┌────────────▼─────────────┐
                              │     CHAT GATEWAY         │
                              │  WhatsApp BSP + WebChat  │
                              │  Session: ch:user:lender │
                              └────────────┬─────────────┘
                                           │
                              ┌────────────▼─────────────┐
                              │     AGENT RUNTIME        │
                              │  Segment-aware prompts   │
                              │  State-aware tool access │
                              │  Hindi/English bilingual │
                              └────────────┬─────────────┘
                                           │
                    ┌──────────────────────┬┴┬──────────────────────┐
                    │                      │ │                      │
           ┌────────▼────────┐  ┌──────────▼─▼──────────┐ ┌───────▼────────┐
           │  POLICY ENGINE  │  │    TOOL EXECUTOR      │ │  AUDIT TRAIL   │
           │  7 structural   │  │    7-step pipeline    │ │  Append-only   │
           │  10 behavioral  │  │    60 lending tools   │ │  PII-masked    │
           └─────────────────┘  └───────────┬───────────┘ └────────────────┘
                                            │
              ┌──────────┬──────────┬───────┼───────┬──────────┬──────────┐
              │          │          │       │       │          │          │
         ┌────▼───┐ ┌───▼────┐ ┌──▼───┐ ┌─▼──┐ ┌──▼───┐ ┌───▼────┐ ┌──▼───┐
         │Identity│ │  Data  │ │Score │ │Prod│ │ Exec │ │Service│ │Monitor│
         │   6    │ │   24   │ │  8   │ │ 5  │ │  6   │ │   6   │ │   5  │
         └────────┘ └────────┘ └──────┘ └────┘ └──────┘ └───────┘ └──────┘
                                            │
              ┌─────────────────────────────▼──────────────────────────────┐
              │              38 SEGMENT TEMPLATES (YAML)                  │
              │  Scoring weights ∙ Schedule types ∙ Moratorium triggers   │
              │  Data sources ∙ Monitoring cadence ∙ Graduation criteria  │
              └────────────────────────────────────────────────────────────┘
```

---

## The Problem We Solve

India has **300 million** creditworthy people with no formal credit history. Traditional lending infrastructure, designed for salaried employees with bureau scores above 700, structurally excludes:

- **63 million dairy farmers** who earn through cooperative milk sales but show irregular bank deposits
- **12 million kirana shop owners** with thriving businesses but no records beyond GST
- **15 million gig workers** with steady platform earnings but no employment letter
- **80 million agricultural workers** whose income is legible only through FPO records, mandi transactions, and satellite imagery
- **40 million micro-entrepreneurs** (street vendors, tailors, salon owners, dhaba operators) whose entire cash flow runs through UPI

These borrowers are not uncreditworthy. Their repayment capacity is legible through **alternative data** -- cooperative pouring records, GST filings, platform earnings, warehouse receipts, telematics, UPI collections, SHG group records -- that traditional loan origination systems cannot ingest, score, or act upon.

Meanwhile, the cost to originate a single Rs 50,000 loan through a human loan officer is Rs 2,000-3,000 (field visit, data entry, compliance checks). At 15% interest, that origination cost consumes 40-60% of the first year's revenue. **The unit economics of small-ticket lending are broken.**

This platform fixes both problems simultaneously: an AI agent that reads alternative data, scores using segment-specific models, designs cash-flow-aligned repayment schedules, and disburses -- all through a WhatsApp conversation in the borrower's language -- at a cost of Rs 140-275 per origination. **80-90% cost reduction.** That is what makes Rs 10,000 nano-loans and Rs 25,000 seasonal crop loans economically viable.

---

## Products and How They Shape Borrower Journeys

Every segment gets a product engineered for its cash flow pattern. The repayment schedule is not a configuration option -- it is the core product insight.

### Agriculture & Allied

| Segment | Product Type | How It Works | What Makes It Different |
|---------|-------------|--------------|------------------------|
| **Dairy Farmer** | Seasonal Dynamic EMI | EMIs rise in flush season (Oct-Feb, high milk output) and fall in lean season (Apr-Jun). Pashu Bima mandatory. | Cooperative pouring regularity is the #1 scoring feature (25% weight). Auto-moratorium on heat waves >38 degrees C. |
| **Sugarcane Farmer** | Crop Receivable Linked | Repayment linked to sugar mill FRP payments. Bullet at harvest. | Mill payment delay (common in India) triggers auto-moratorium instead of NPA. |
| **Cotton Farmer** | Harvest Linked | Repayment after ginning mill sale. PMFBY crop insurance mandatory. | NDVI satellite imagery monitors crop health. Bollworm outbreak triggers moratorium. |
| **Vegetable Grower** | Short Crop Cycle | 3-9 month tenure matching 45-90 day crop cycles. | FPO membership data and mandi price realization are primary scoring signals. |
| **Poultry Farmer** | Batch Cycle Loan | Aligned to 42-day broiler batch cycles. | Integrator data (mortality rate, FCR) replaces traditional income proof. Disease outbreak moratorium. |
| **Fishery** | Seasonal Catch | Adjusted for monsoon fishing ban (2 months). Cyclone auto-moratorium. | Cooperative catch data and vessel ownership are scoring signals. |

### Micro-Enterprise

| Segment | Product Type | How It Works | What Makes It Different |
|---------|-------------|--------------|------------------------|
| **Kirana Shop** | Daily Micro Collection | Rs 400-600/day, 26 working days/month, Sundays off. | GST turnover trend (30% weight) is stronger signal than bureau score. |
| **Street Vendor** | PM SVANidhi Plus | Daily UPI autopay from merchant collections. Ultra-small ticket. | UPI daily collections are the ONLY required data source besides bureau. |
| **Medical Shop** | Inventory Finance | Monthly EMI against drug inventory cycle. | Drug license validity check. Distributor credit terms inform scoring. |
| **Beauty Salon** | Micro Business | Daily UPI collection. Festival season spikes factored. | Booking platform data and customer retention rate are scoring signals. |
| **Dhaba/Restaurant** | Daily Micro | Daily UPI + food aggregator deductions. | Swiggy/Zomato aggregator data combined with FSSAI compliance. |
| **Tailoring Unit** | Micro Business | Daily UPI. Seasonal demand (weddings/festivals). | E-commerce order trend captures digital expansion. |

### Gig & Transport

| Segment | Product Type | How It Works | What Makes It Different |
|---------|-------------|--------------|------------------------|
| **Gig Worker** | Payout Linked | 15% deducted from each Swiggy/Zomato/Uber payout. | Platform deactivation is catastrophic risk -- instant escalation trigger. |
| **Cab Driver** | Vehicle Finance PV | Daily payout-linked from Ola/Uber. | Platform earnings trend + rating + active days replace employment proof. |
| **Truck Operator** | Vehicle Finance CV | Monthly EMI against FASTag + telematics data. | FASTag trip regularity and load utilization are unique scoring features. |
| **Auto Rickshaw** | Three-Wheeler Finance | Daily payout-linked. Flood/waterlogging moratorium. | Daily trip count from telematics replaces income documentation. |
| **E-Rickshaw** | EV Finance | Daily payout-linked. Battery failure moratorium. | Battery health percentage is a unique scoring and monitoring signal. |

### Asset-Backed & Specialized

| Segment | Product Type | How It Works | What Makes It Different |
|---------|-------------|--------------|------------------------|
| **Gold Loan** | Gold Pledge | Bullet or monthly-interest-only. LTV 75%. | Real-time gold price monitoring. Margin call at 85% LTV breach. |
| **Warehouse Receipt** | Commodity Pledge | Bullet at harvest/sale. LTV 70%. | Commodity price monitoring. Physical inspection trigger on quality flags. |
| **EV Financing** | Asset Linked | Daily payout from delivery platform. | Battery health + charging regularity from telematics data. |
| **Solar Financing** | Savings Linked | EMI equals monthly electricity bill savings. 5-7 year tenure. | Solar generation kWh and net metering status are scoring signals. |
| **Micro Housing** | Home Loan | Standard monthly EMI, 3-10 year tenure. | Property title verification + income stability. PMAY eligibility check. |

### Social & Institutional

| Segment | Product Type | How It Works | What Makes It Different |
|---------|-------------|--------------|------------------------|
| **SHG Member** | Group Linked | Monthly group repayment. Group guarantee model. | Group repayment rate (25% weight) replaces individual collateral. NRLM grading. |
| **FPO Entity** | Working Capital | Seasonal bullet for procurement/aggregation. Larger ticket. | Entity-level scoring: NABARD grade, governance score, member count. |
| **NBFC BC Agent** | Float Finance | Daily settlement-linked. | Transaction volume and active customer count are primary signals. |
| **EdTech Student** | ISA Hybrid | Pay-after-placement. Course-in-progress moratorium. | Course completion rate and platform placement track record drive scoring. |

### Additional Segments

Construction workers (weekly income smoothing), domestic workers (nano loans), dairy processors (supply chain finance), agri input dealers (seasonal working capital), rental income earners (receivable-backed), rice millers (procurement finance), health clinics (equipment finance), micro contractors (milestone-linked), student housing (semester-aligned).

**38 segments total. Each with a YAML config defining the entire journey.**

---

## The Layer Stack

The platform is a **monolith with clean module boundaries** -- each layer is independently testable and extractable to a microservice when scale demands it.

```
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 7: CHANNEL GATEWAY                                       │
│  WhatsApp BSP adapter ∙ Web adapter ∙ Session routing           │
│  channel:user_id:lender_id keying ∙ Multi-lender isolation      │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 6: AGENT RUNTIME                                         │
│  LLM orchestration ∙ Segment-aware system prompts               │
│  38 segment contexts ∙ Hindi/English confirmation detection      │
│  Tool result explanation ∙ 10-turn conversation window           │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 5: BEHAVIORAL SUPERVISION                                │
│  10 post-response rules ∙ Coercive language detection            │
│  PII leak prevention ∙ Grievance disclosure enforcement          │
│  Empathy-first on distress ∙ Social engineering defense          │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 4: STRUCTURAL POLICY                                     │
│  7 pre-tool rules ∙ Session state gating                        │
│  Confirmation enforcement ∙ KFS mandatory ∙ Cooling-off period  │
│  Bureau velocity limit ∙ Maker-checker ∙ Consent gating         │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 3: TOOL EXECUTOR                                         │
│  7-step pipeline: State→Confirm→Authority→CB→Execute→Trace→Emit │
│  Circuit breaker per tool ∙ Timeout per tool ∙ Audit every call │
│  60 lending tools across 7 categories                           │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 2: DOMAIN MODEL                                          │
│  Forward-only session state machine (UNVERIFIED→VERIFIED→CONFIRMED) │
│  15-state loan lifecycle ∙ Append-only audit trail              │
│  PII stored as hashes only ∙ 27+ Pydantic schemas              │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 1: INFRASTRUCTURE                                        │
│  FastAPI ∙ SQLAlchemy async ∙ PostgreSQL ∙ Redis                │
│  Alembic migrations ∙ Docker Compose ∙ GitHub Actions CI        │
│  structlog JSON logging ∙ 6 hard authority boundaries           │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 0: SEGMENT TEMPLATES                                     │
│  38 YAML configs ∙ Scoring features + weights                   │
│  Product type + schedule ∙ Insurance requirements               │
│  Moratorium triggers ∙ Monitoring cadence + signals             │
│  Graduation criteria ∙ Journey greeting in regional language    │
└─────────────────────────────────────────────────────────────────┘
```

### Why This Ordering Matters

The stack is ordered by **trust boundary**. Layer 0 (segment configs) is the most trusted -- it encodes domain expertise that changes only through deliberate product decisions. Layer 7 (channel gateway) is the least trusted -- it receives raw borrower input from the internet.

Each layer constrains the layer above it:

- **Layer 0** (segments) defines what data sources exist, what features matter, and what products are possible
- **Layer 1** (infrastructure) enforces hard authority boundaries that no higher layer can override
- **Layer 2** (domain model) makes non-compliance structurally impossible through forward-only state machines and append-only audit
- **Layer 3** (executor) runs every tool call through a 7-step gauntlet before the function body executes
- **Layer 4** (structural policy) blocks tools that violate session state, confirmation, or authority rules
- **Layer 5** (behavioral supervision) catches compliance violations in the agent's natural language output
- **Layer 6** (runtime) orchestrates the conversation but cannot bypass any lower layer
- **Layer 7** (gateway) routes messages but has no authority over lending operations

**The agent is powerful but constrained.** It can do everything a loan officer can do. It cannot do anything a loan officer should not do.

---

## How a Loan Happens

A dairy farmer in Banaskantha messages a WhatsApp number printed on a cooperative society poster.

### Phase 1: Identity (Session State: UNVERIFIED)

```
Farmer:  "Namaste, mujhe loan chahiye"

Agent:   "Namaste, Ramesh bhai! Aapne cooperative loan ke liye contact kiya hai.
          Loan ke liye pehle aapki pehchaan verify karni hogi.
          Kya aap apna Aadhaar number bata sakte hain?"
```

The agent has access to only 6 identity tools. It cannot pull data, score, or disburse. The state machine makes this a structural impossibility.

```
Farmer:  "1234 5678 9012"
Agent:   → verify_aadhaar_otp(aadhaar_number="123456789012")
         "OTP aapke registered mobile par bheja gaya hai.
          Agar padhne mein dikkat ho toh main voice call kar sakta hoon."

Farmer:  "456789"
Agent:   → verify_aadhaar_otp(otp="456789") → verified: true
         → SESSION TRANSITIONS: UNVERIFIED → VERIFIED
         "Dhanyavaad Ramesh bhai! Ab main aapke cooperative se jaankari le sakta hoon."
```

### Phase 2: Data Assembly (State: VERIFIED)

The agent now orchestrates 6-8 tool calls, explaining each step conversationally:

```
→ fetch_cooperative_data(membership_id="BD-2020-12345")
  Pouring regularity: 92%, tenure: 48 months, fat: 6.2%

→ fetch_aa_bank_data(consent_id="...")
  Avg monthly inflow: Rs 42,000, FOIR: 0.32

→ "Bureau check ke liye permission chahiye. Kya main check karun?"
  Farmer: "Haan, kar do"
→ pull_credit_bureau() → score: 720, grade: B1

→ fetch_uli_parallel(pincode="387001")
  Land: 4.5 acres irrigated, NDVI: 0.42 stable, weather: low drought risk

→ compute_confidence_score() → 0.85, HIGH
→ cross_validate_sources() → consistent, no anomalies
```

### Phase 3: Scoring and Decision

```
→ compute_segment_score(segment="DAIRY_FARMER", features={...})
  Score: 680, Grade: A2

→ evaluate_segment_policy(score=680, confidence="HIGH")
  Decision: APPROVE

→ compute_risk_pricing(score=680)
  Rate: 14%, Band: A2

→ design_dynamic_product(segment="DAIRY_FARMER", score=680)
  Seasonal Dynamic, Rs 1,00,000, 18 months
  Flush EMI: Rs 8,450 | Lean EMI: Rs 3,900 | Pashu Bima: Rs 3,540/year
```

### Phase 4: Execution (State: CONFIRMED)

After the borrower reviews and confirms terms:

```
→ generate_kfs() → Key Fact Statement with APR, 3-day cooling-off
→ initiate_esign() → Aadhaar eSign
→ enroll_insurance() → Pashu Bima enrolled
→ setup_enach_mandate() → Monthly auto-debit
  [3-day cooling-off period elapses]
→ execute_disbursement(amount=100000, mode="UPI")

Agent: "Ramesh bhai, Rs 1,00,000 aapke account mein aa gaya hai.
        Pehli kist 15 May ko hogi. Koi sawal ho toh yahi message karein."
```

### Phase 5: Living Loan (Post-Disbursement)

Every week, the monitoring pipeline runs automatically:

- **Signal polling**: cooperative pouring data, bank inflows, weather data
- **Trigger evaluation**: if pouring drops 30%, schedule adjusts. If temperature exceeds 38 degrees C, moratorium auto-flags.
- **Graduation**: after 12 months at 90% on-time rate, the farmer gets offered 2x limit and 2% rate reduction.

The loan breathes with the farmer's life.

---

## Compliance as Architecture

Compliance is not a checklist applied after the fact. It is baked into the execution pipeline as structural constraints that cannot be bypassed by the AI agent, prompt injection, or configuration change.

| What Cannot Happen | How It Is Prevented | RBI Reference |
|-------------------|---------------------|---------------|
| Disbursement without KFS | `check_kfs_mandatory` structural rule blocks `execute_disbursement` | Digital Lending Para 14 |
| Disbursement during cooling-off | `check_cooling_off_period` structural rule enforces 3-day window | Digital Lending Para 15 |
| PII in agent response | `pii_masked_readback` behavioral rule catches 12-digit Aadhaar | Data protection |
| PII in database | Aadhaar/PAN stored as SHA-256 hashes only | Digital Lending Para 31 |
| PII in audit trail | `mask_dict()` applied to all tool I/O before storage | Digital Lending Para 26 |
| Coercive language | `rbi_fair_practices_language` detects "legal action", "arrest", "jabti" | Fair Practices Code |
| Missing grievance disclosure | `grievance_disclosure` catches complaints without officer reference | Digital Lending Para 20 |
| Bureau score damage | `bureau_velocity` limits to 2 hard inquiries per 48 hours | Borrower protection |
| AI auto-disbursement | `can_disburse_without_human = False` hard-coded constant | Operational risk |
| AI auto-approval | `can_auto_approve = False` hard-coded constant | Operational risk |
| Social engineering | `no_override_on_authority` detects "manager approved" patterns | Behavioral defense |
| Insurance mis-selling | `insurance_opt_in` flags mandatory insurance language (except Pashu Bima) | Fair Practices Code |

Six hard authority boundaries are **Python constants** in `app/core/config.py`, not environment variables. They change only through code review and deployment:

```
bureau_pull_max_per_aadhaar_48h = 2       # Protect borrower credit score
disbursement_max_amount         = 500,000  # Rs 5 lakh cap
fee_waiver_max                  = 500      # Rs 500 max auto-waiver
moratorium_max_months           = 3        # 3-month max pause
can_auto_approve                = False    # Human must review
can_disburse_without_human      = False    # Human must approve
```

---

## The 60-Tool Operating System

Every lending operation is a standalone, typed, circuit-breaker-protected, auditable async function. The agent orchestrates tools; it never accesses APIs directly.

### Tool Categories

| Category | Tools | Session State | Purpose |
|----------|-------|---------------|---------|
| **Identity** | 6 | UNVERIFIED | Aadhaar OTP/voice, PAN (Jaro-Winkler matching), bank penny drop, AA consent, negative list |
| **Data Assembly** | 24 | VERIFIED | ULI (land + satellite + weather), AA bank, bureau, cooperative, platform, GST, warehouse receipt, gold appraisal, EV telematics, solar generation, SHG records, vehicle telematics, poultry integrator, fishery cooperative, FPO, UPI transactions, property records, edtech platform, device score, cross-validation, confidence, borrower profile |
| **Scoring** | 8 | VERIFIED | 38-segment weighted scoring (900-point scale), policy evaluation, risk pricing (5 bands), fraud signals, CAM, what-if simulator, PSL classification, multilingual explainability |
| **Product** | 5 | VERIFIED | Dynamic product design (38 schedule types, 19 moratorium configs), seasonal/daily/payout-linked schedules, insurance premium |
| **Execution** | 6 | CONFIRMED | KFS (RBI mandatory), eSign, insurance enrollment, eNACH mandate, disbursement (maker-checker), CERSAI registration |
| **Servicing** | 6 | VERIFIED | Loan status, repayment schedule, prepayment, moratorium, statement, NOC |
| **Monitoring** | 5 | VERIFIED | Signal polling, trigger evaluation, auto-intervention, graduation, job scheduling |

### The 7-Step Execution Pipeline

Every tool call passes through this gauntlet before the function body runs:

```
1. SESSION STATE CHECK   → Is the session in the minimum state for this tool category?
2. CONFIRMATION CHECK    → Does this tool need explicit borrower consent?
3. AUTHORITY CHECK       → Does this WRITE tool have maker-checker approval?
4. CIRCUIT BREAKER       → Is this tool in OPEN state from repeated failures?
5. EXECUTE               → Run the handler with per-tool timeout
6. TRACE                 → Record latency, state transitions, policy results
7. EMIT EVENT            → Append to audit trail, fire downstream events
```

---

## Platform Numbers

| Metric | Count |
|--------|-------|
| Borrower segments | 38 |
| Lending tools | 60 |
| Pydantic schemas | 39+ |
| Policy rules | 17 (7 structural + 10 behavioral) |
| Segment scoring models | 38 (weighted feature sums) |
| Product schedule types | 38 |
| Moratorium trigger configs | 19 |
| Segment prompt contexts | 38 |
| Tests | 256 (all passing) |
| Python source files | 105 |
| Test files | 25 |
| Segment YAML configs | 38 |
| Hard authority boundaries | 6 |
| Git commits | 21 (organized, conventional) |

---

## Running the Platform

```bash
# Install
pip install -e ".[dev]"

# Run tests (256 tests, ~2.5 seconds)
make test

# Lint
make lint

# Dev server
make run                        # uvicorn on :8000

# Docker (app + postgres + redis)
docker-compose up -d

# Migrate
make migrate                    # alembic upgrade head
```

---

## Project Structure

```
├── app/
│   ├── main.py                         # FastAPI app, 5 routers
│   ├── core/                           # Config, DB, logging, audit, Redis
│   │   ├── config.py                   # 6 hard authority boundaries
│   │   ├── audit.py                    # PII masking, append-only trail
│   │   └── ...
│   ├── models/                         # SQLAlchemy: borrower, loan, session, audit
│   ├── schemas/                        # 39+ Pydantic v2 schemas
│   ├── tools/
│   │   ├── registry.py                 # @lending_tool decorator, ToolRegistry
│   │   ├── executor.py                 # 7-step execution pipeline
│   │   ├── circuit_breaker.py          # Per-tool CLOSED/OPEN/HALF_OPEN
│   │   ├── session_machine.py          # Forward-only state transitions
│   │   ├── identity/                   # 6 tools: Aadhaar, PAN, bank, AA, negative
│   │   ├── data/                       # 24 tools: ULI, AA, bureau, cooperative,
│   │   │                               #   platform, GST, warehouse, gold, EV,
│   │   │                               #   solar, SHG, vehicle, poultry, fishery,
│   │   │                               #   FPO, UPI, property, edtech, ...
│   │   ├── scoring/                    # 8 tools: score, policy, pricing, fraud, CAM
│   │   ├── product/                    # 5 tools: design, schedules, insurance
│   │   ├── execution/                  # 6 tools: KFS, eSign, disburse, CERSAI
│   │   ├── servicing/                  # 6 tools: status, prepay, moratorium, NOC
│   │   └── monitoring/                 # 5 tools: signals, triggers, intervention
│   ├── policy/
│   │   ├── structural.py              # 7 pre-tool deterministic rules
│   │   ├── behavioral.py             # 10 post-response regex rules
│   │   └── engine.py                  # Policy orchestrator
│   ├── agent/
│   │   ├── prompts.py                 # 38 segment contexts + system prompt builder
│   │   ├── confirmation.py            # Hindi/English confirm/deny detection
│   │   └── runtime.py                 # Conversation loop, tool orchestration
│   ├── gateway/
│   │   ├── channels.py                # WhatsApp BSP + Web adapters
│   │   └── session_manager.py         # Multi-lender session routing
│   └── segments/
│       └── loader.py                  # YAML → SegmentTemplate → SegmentRegistry
│
├── segments/                           # 38 YAML segment configs
│   ├── dairy_farmer.yaml
│   ├── kirana_shop.yaml
│   ├── gig_worker.yaml
│   ├── gold_loan.yaml
│   ├── ev_financing.yaml
│   ├── warehouse_receipt.yaml
│   ├── shg_member.yaml
│   ├── ... (35 more)
│
├── tests/                              # 25 test files, 256 tests
├── pyproject.toml                      # Build config, dependencies
├── Dockerfile                          # Python 3.10, uvicorn
├── docker-compose.yml                  # app + postgres:16 + redis:7
├── Makefile                            # install, test, lint, run, migrate
└── alembic/                            # Database migrations
```

---

## What We Are Building Next

The core platform is complete. Mock implementations use production-accurate schemas and are swappable for real API integrations with no changes to the tool framework, policy engine, or agent layer.

**Immediate (Weeks 1-4):**
- Real API integrations: UIDAI eKYC, CIBIL, Account Aggregator, WhatsApp BSP, eSign, eNACH, UPI disbursement
- LLM provider integration (OpenAI/Anthropic) with token budget management
- Maker-checker dashboard for human review of AI recommendations
- Redis-backed session persistence

**Near-term (Months 2-3):**
- ML model training on segment-specific repayment outcomes (replacing rule-based scoring)
- Multi-tenant lender isolation with API key authentication and row-level security
- Production observability: Prometheus metrics, structured log aggregation, Sentry
- Load testing and performance optimization for concurrent sessions

**Medium-term (Months 4-6):**
- Voice agent for IVR channel (Hindi/regional language speech-to-text)
- USSD fallback for feature phone borrowers
- Segment auto-detection from initial conversation context
- Portfolio-level risk dashboard for lenders

---

## The Story

We started with a question: **Why does it cost Rs 3,000 to give someone a Rs 25,000 loan?**

The answer was not technology. India has UPI, Aadhaar, Account Aggregator, eSign, eNACH -- the digital public infrastructure exists. The answer was **architecture**. The lending stack was designed 20 years ago for large-ticket loans processed by humans through siloed systems. Every new regulatory requirement (KFS, cooling-off, audit trail, PII protection) added another layer of manual process.

AI changes the equation -- but only if the AI is the system, not a layer on top of it. A chatbot that fills forms in a legacy LOS saves 30% cost. An AI agent that IS the loan officer, operating through policy-gated tools with structural compliance, saves 90%.

We built the second kind.

38 borrower segments. 60 lending tools. 17 compliance rules. One WhatsApp conversation. That is embedded credit as a service.

---

## Technology

| Layer | Technology | Why |
|-------|-----------|-----|
| Runtime | Python 3.10 | Async-first, ML/AI ecosystem |
| Framework | FastAPI | Async, Pydantic v2 native, auto-docs |
| ORM | SQLAlchemy 2.0 | Async sessions, declarative models |
| Database | PostgreSQL 16 | ACID for lending, JSONB support |
| Cache | Redis 7 | Sessions, events, circuit breaker state |
| Validation | Pydantic v2 | Schema enforcement on all tool I/O |
| Logging | structlog | JSON structured with context propagation |
| Lint | ruff | Fast, replaces flake8+isort+black |
| Tests | pytest + pytest-asyncio | Async test support, 256 tests in 2.5s |
| CI | GitHub Actions | Lint + test on every push |
| Container | Docker Compose | app + postgres + redis, health-checked |

---

## License

Proprietary. All rights reserved.

---

*Built for the 300 million.*
