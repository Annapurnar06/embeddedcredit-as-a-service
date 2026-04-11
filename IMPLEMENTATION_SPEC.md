# AI-First Enterprise Lending Platform: Implementation Specification

**Document Type**: Technical Implementation Reference
**Platform**: LendingOS-India v0.1.0
**Codebase**: 117 files | 48 tools | 234 tests | 17 policy rules

---

## Part I: Project Structure and File Manifest

### Directory Tree

```
workspace/
├── pyproject.toml                      # Build config, dependencies, tool settings
├── Dockerfile                          # Python 3.10-slim, uvicorn dev server
├── docker-compose.yml                  # app + postgres:16 + redis:7
├── Makefile                            # install, test, lint, run, migrate
├── alembic.ini                         # Migration config
├── .env.example                        # Environment variable template
├── .github/workflows/ci.yml            # GitHub Actions: lint + test
│
├── segments/                           # Borrower segment YAML configs
│   ├── dairy_farmer.yaml               # Seasonal schedule, Pashu Bima, cooperative data
│   ├── kirana_shop.yaml                # Daily micro schedule, GST data
│   ├── gig_worker.yaml                 # Payout-linked schedule, platform earnings
│   └── default_policy.yaml             # Base policy defaults
│
├── app/
│   ├── main.py                         # FastAPI app, lifespan, 5 routers
│   │
│   ├── core/
│   │   ├── config.py                   # Settings + 6 hard authority boundaries
│   │   ├── database.py                 # Async SQLAlchemy engine, session factory
│   │   ├── logging.py                  # structlog JSON with 10 processors
│   │   ├── audit.py                    # AuditTrail, EventEmitter, PII masking
│   │   └── redis.py                    # Async Redis client singleton
│   │
│   ├── models/                         # SQLAlchemy ORM models
│   │   ├── borrower.py                 # PII as hashes, segment, language prefs
│   │   ├── loan.py                     # 15-state LoanStatus, PSL, maker_approved
│   │   ├── session.py                  # SessionState enum, LendingSession
│   │   └── audit.py                    # Append-only AuditLog + ToolExecution
│   │
│   ├── schemas/                        # Pydantic v2 validation schemas
│   │   ├── borrower.py                 # 15 schemas: Aadhaar, PAN, Bureau, Bank, etc.
│   │   ├── loan.py                     # 12 schemas: Score, Pricing, KFS, CAM, etc.
│   │   └── session.py                  # SessionCreate, SessionResponse, Chat
│   │
│   ├── tools/
│   │   ├── registry.py                 # ToolDefinition, ToolRegistry, @lending_tool
│   │   ├── executor.py                 # 7-step pipeline, ExecutionContext, ToolResult
│   │   ├── circuit_breaker.py          # CLOSED/OPEN/HALF_OPEN per tool
│   │   ├── session_machine.py          # Forward-only state transitions
│   │   │
│   │   ├── identity/                   # 6 tools (UNVERIFIED state)
│   │   │   ├── aadhaar.py              # verify_aadhaar_otp, verify_aadhaar_voice_otp
│   │   │   ├── pan.py                  # verify_pan (Jaro-Winkler matching)
│   │   │   ├── bank_account.py         # verify_bank_account (penny drop)
│   │   │   ├── aa_consent.py           # initiate_aa_consent
│   │   │   └── negative_list.py        # check_negative_list
│   │   │
│   │   ├── data/                       # 12 tools (VERIFIED state)
│   │   │   ├── uli.py                  # fetch_uli_parallel (land+satellite+weather+PMFBY)
│   │   │   ├── aa.py                   # fetch_aa_bank_data
│   │   │   ├── bureau.py               # pull_credit_bureau (confirmation-gated)
│   │   │   ├── bank_statement.py       # analyze_bank_statement
│   │   │   ├── document.py             # extract_document (9 types)
│   │   │   ├── cooperative.py          # fetch_cooperative_data
│   │   │   ├── platform.py             # fetch_platform_earnings
│   │   │   ├── gst.py                  # fetch_gst_returns
│   │   │   ├── device.py               # compute_device_score
│   │   │   └── validation.py           # cross_validate, confidence, borrower_profile
│   │   │
│   │   ├── scoring/                    # 8 tools (VERIFIED state)
│   │   │   ├── policy_eval.py          # evaluate_segment_policy
│   │   │   ├── score.py                # compute_segment_score (weighted, 900-point)
│   │   │   ├── pricing.py              # compute_risk_pricing (5 rate bands)
│   │   │   ├── fraud.py                # check_fraud_signals
│   │   │   ├── cam.py                  # generate_cam (Credit Assessment Memo)
│   │   │   ├── whatif.py               # run_what_if (policy simulator)
│   │   │   ├── psl.py                  # check_psl_classification
│   │   │   └── explain.py              # generate_explainability (multilingual)
│   │   │
│   │   ├── product/                    # 5 tools (VERIFIED state)
│   │   │   ├── design.py               # design_dynamic_product
│   │   │   ├── schedules.py            # seasonal, daily_micro, payout_linked
│   │   │   └── insurance.py            # compute_insurance_premium
│   │   │
│   │   ├── execution/                  # 6 tools (CONFIRMED state)
│   │   │   ├── kfs.py                  # generate_kfs (RBI-mandatory)
│   │   │   ├── esign.py                # initiate_esign
│   │   │   ├── insurance.py            # enroll_insurance
│   │   │   ├── enach.py                # setup_enach_mandate
│   │   │   ├── disbursement.py         # execute_disbursement (maker-checker)
│   │   │   └── cersai.py               # register_cersai
│   │   │
│   │   ├── servicing/                  # 6 tools (VERIFIED state)
│   │   │   ├── status.py               # get_loan_status
│   │   │   ├── schedule.py             # get_repayment_schedule
│   │   │   ├── prepayment.py           # process_prepayment
│   │   │   ├── moratorium.py           # apply_moratorium
│   │   │   ├── statements.py           # generate_statement
│   │   │   └── noc.py                  # generate_noc
│   │   │
│   │   └── monitoring/                 # 5 tools (VERIFIED state)
│   │       ├── signals.py              # poll_monitoring_signals
│   │       ├── triggers.py             # evaluate_monitoring_triggers
│   │       ├── intervention.py         # execute_auto_intervention
│   │       ├── graduation.py           # evaluate_graduation
│   │       └── scheduler.py            # schedule_monitoring_job
│   │
│   ├── policy/
│   │   ├── structural.py              # 7 pre-tool rules (deterministic)
│   │   ├── behavioral.py             # 10 post-response rules (regex)
│   │   ├── engine.py                  # PolicyEngine orchestrator
│   │   └── config.py                  # YAML policy loader + merge
│   │
│   ├── agent/
│   │   ├── llm.py                     # LLMMessage, ToolCall, MockLLMClient
│   │   ├── prompts.py                 # System prompt builder (segment+state-aware)
│   │   ├── confirmation.py            # Hindi/English confirm/deny detection
│   │   └── runtime.py                 # AgentRuntime, AgentSession, conversation loop
│   │
│   ├── gateway/
│   │   ├── channels.py                # ChannelAdapter, WebChat, WhatsApp BSP
│   │   └── session_manager.py         # channel:user_id:lender_id -> AgentSession
│   │
│   ├── api/
│   │   ├── health.py                  # GET /health
│   │   ├── sessions.py                # POST/GET /api/sessions
│   │   ├── loans.py                   # GET /api/loans
│   │   ├── audit.py                   # GET /api/audit/logs, tools, loan trail
│   │   └── chat.py                    # POST /api/chat/message, webhook/whatsapp
│   │
│   └── segments/
│       └── loader.py                  # SegmentTemplate, SegmentRegistry
│
└── tests/                             # 22 test files, 234 tests
    ├── conftest.py                    # anyio_backend, async client fixtures
    ├── test_health.py
    ├── test_models.py
    ├── test_schemas.py
    ├── test_session_machine.py
    ├── test_tool_registry.py
    ├── test_circuit_breaker.py
    ├── test_executor.py
    ├── test_identity_tools.py
    ├── test_data_tools.py
    ├── test_scoring_tools.py
    ├── test_product_tools.py
    ├── test_execution_tools.py
    ├── test_servicing_tools.py
    ├── test_monitoring_tools.py
    ├── test_structural_policy.py
    ├── test_behavioral_policy.py
    ├── test_policy_engine.py
    ├── test_confirmation.py
    ├── test_audit.py
    ├── test_agent_runtime.py
    ├── test_gateway.py
    └── test_integration.py
```

---

## Part II: Core Infrastructure

### 2.1 Build Configuration (`pyproject.toml`)

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "lendingos-india"
version = "0.1.0"
description = "AI-first lending platform for Indian financial inclusion"
requires-python = ">=3.10"
dependencies = [
    "fastapi>=0.109.0,<1.0.0",
    "uvicorn[standard]>=0.27.0,<1.0.0",
    "sqlalchemy>=2.0.25,<3.0.0",
    "alembic>=1.13.0,<2.0.0",
    "asyncpg>=0.29.0,<1.0.0",
    "redis>=5.0.0,<6.0.0",
    "pydantic>=2.5.0,<3.0.0",
    "pydantic-settings>=2.1.0,<3.0.0",
    "python-dotenv>=1.0.0,<2.0.0",
    "structlog>=24.1.0,<25.0.0",
    "httpx>=0.26.0,<1.0.0",
    "pyyaml>=6.0,<7.0",
    "python-multipart>=0.0.6,<1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0,<9.0.0",
    "pytest-asyncio>=0.23.0,<1.0.0",
    "pytest-cov>=4.1.0,<6.0.0",
    "ruff>=0.2.0,<1.0.0",
    "mypy>=1.8.0,<2.0.0",
    "httpx>=0.26.0,<1.0.0",
]

[tool.ruff]
target-version = "py310"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "SIM"]
ignore = ["B008"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

### 2.2 Docker Compose (`docker-compose.yml`)

Three services with health-check-gated startup:

```yaml
version: "3.9"
services:
  app:
    build: .
    ports: ["8000:8000"]
    environment:
      DATABASE_URL: ${DATABASE_URL}
      REDIS_URL: redis://redis:6379/0
      ENVIRONMENT: development
      LOG_LEVEL: INFO
    depends_on:
      postgres: {condition: service_healthy}
      redis: {condition: service_healthy}
    volumes:
      - ./app:/app/app
      - ./segments:/app/segments

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: lendingos
    ports: ["5432:5432"]
    volumes: [pgdata:/var/lib/postgresql/data]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER}"]
      interval: 5s

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
volumes:
  pgdata:
```

### 2.3 Hard Authority Boundaries (`app/core/config.py`)

These constants cannot be overridden by the AI agent or environment variables:

```python
class Settings(BaseSettings):
    # ... standard config ...

    bureau_pull_max_per_aadhaar_48h: int = 2    # Protect borrower credit score
    disbursement_max_amount: int = 500_000       # ₹5 lakh single disbursement cap
    fee_waiver_max: int = 500                    # ₹500 max auto-waiver
    moratorium_max_months: int = 3               # 3-month max moratorium
    can_auto_approve: bool = False               # AI cannot approve loans
    can_disburse_without_human: bool = False     # AI cannot disburse without maker-checker
```

---

## Part III: Domain Model

### 3.1 Session State Machine

```
UNVERIFIED ──→ VERIFIED ──→ CONFIRMED ──→ (terminal)
     │              │              │
     └──────→ EXPIRED ←───────────┘
```

**Implementation** (`app/tools/session_machine.py`):

```python
VALID_TRANSITIONS = {
    SessionState.UNVERIFIED: [SessionState.VERIFIED, SessionState.EXPIRED],
    SessionState.VERIFIED:   [SessionState.CONFIRMED, SessionState.EXPIRED],
    SessionState.CONFIRMED:  [SessionState.EXPIRED],
    SessionState.EXPIRED:    [],  # terminal
}
```

**Tool category gating** (`app/tools/registry.py`):

| Category | Min State | Tool Count |
|----------|-----------|------------|
| IDENTITY | UNVERIFIED | 6 |
| DATA | VERIFIED | 12 |
| SCORING | VERIFIED | 8 |
| PRODUCT | VERIFIED | 5 |
| EXECUTION | CONFIRMED | 6 |
| SERVICING | VERIFIED | 6 |
| MONITORING | VERIFIED | 5 |

### 3.2 Loan Application Lifecycle

15-state enum (`app/models/loan.py`):

```
DRAFT → DATA_ASSEMBLY → SCORING → APPROVED/REFERRED/REJECTED
                                        ↓
                                 OFFER_PRESENTED → OFFER_ACCEPTED
                                        ↓
                                 KFS_GENERATED → ESIGNED → DISBURSED → ACTIVE
                                                                         ↓
                                                              CLOSED / NPA / WRITTEN_OFF
```

### 3.3 Database Schema

**4 tables:**

| Table | Key Columns | Design |
|-------|-------------|--------|
| `borrowers` | aadhaar_hash, pan_hash, phone_hash, segment, language | PII as hashes only |
| `loan_applications` | status (15-state), amount, score, decision, maker_approved, psl_category | JSON columns for profile/schedule |
| `lending_sessions` | state (4-state), channel, segment, conversation_history_json | Nullable borrower_id (pre-verification) |
| `audit_logs` + `tool_executions` | append-only, input_masked_json, latency_ms, state transitions | No updated_at column |

---

## Part IV: Complete Tool Catalog (48 Tools)

### 4.1 Identity Tools (6) — State: UNVERIFIED

| Tool | Authority | Confirmation | Timeout | CB | Key Logic |
|------|-----------|-------------|---------|-----|-----------|
| `verify_aadhaar_otp` | GENERAL | No | 15s | 5 | 12-digit validation, 6-digit OTP, returns AadhaarVerifyResult |
| `verify_aadhaar_voice_otp` | GENERAL | No | 20s | 5 | Spoken OTP ≥4 chars, voice call for low-literacy |
| `verify_pan` | GENERAL | No | 10s | 5 | Regex `^[A-Z]{5}[0-9]{4}[A-Z]$`, Jaro-Winkler name match |
| `verify_bank_account` | GENERAL | No | 15s | 5 | Penny drop verification, Jaro-Winkler against account name |
| `initiate_aa_consent` | GENERAL | **Yes** | 10s | 5 | Account Aggregator consent, legal act requiring confirmation |
| `check_negative_list` | GENERAL | No | 5s | 3 | RBI wilful defaulter, CIBIL fraud, sanctions, PEP |

### 4.2 Data Assembly Tools (12) — State: VERIFIED

| Tool | Authority | Confirmation | Timeout | CB | Key Logic |
|------|-----------|-------------|---------|-----|-----------|
| `fetch_uli_parallel` | GENERAL | No | 5s | 3 | 4 parallel sources: land records, satellite NDVI, weather IMD, PMFBY |
| `fetch_aa_bank_data` | GENERAL | No | 10s | 5 | AA bank data with transaction categories, FOIR |
| `pull_credit_bureau` | ACCOUNT | **Yes** | 5s | 3 | **Hard inquiry**, confirmation-gated, CIBIL/Experian |
| `analyze_bank_statement` | GENERAL | No | 30s | 3 | Income, expense, FOIR, bounce rate, fraud flags |
| `extract_document` | GENERAL | No | 15s | 3 | 9 types: Aadhaar, PAN, salary slip, ITR, GST, property, vehicle RC, gold, bank stmt |
| `fetch_cooperative_data` | GENERAL | No | 5s | 3 | Pouring regularity, fat %, tenure, payouts |
| `fetch_platform_earnings` | GENERAL | No | 5s | 3 | Swiggy/Zomato/Uber earnings, rating, active days |
| `fetch_gst_returns` | GENERAL | No | 5s | 3 | GSTIN validation (15 chars), filing regularity, turnover trend |
| `compute_device_score` | GENERAL | No | 3s | 5 | Device fingerprint risk score (0-1000) |
| `cross_validate_sources` | GENERAL | No | 2s | 5 | Income delta check (>30% = anomaly), name/address consistency |
| `compute_confidence_score` | GENERAL | No | 1s | 5 | Weighted: 0.3×source + 0.3×freshness + 0.2×validation + 0.2×anomaly |
| `compute_borrower_profile` | GENERAL | No | 2s | 5 | Assembles full BorrowerProfile with all verification flags |

### 4.3 Scoring Tools (8) — State: VERIFIED

| Tool | Authority | Confirmation | Timeout | CB | Key Logic |
|------|-----------|-------------|---------|-----|-----------|
| `evaluate_segment_policy` | ACCOUNT | No | 5s | 5 | Fraud→REJECT, Low confidence→REFER, Score≥650→APPROVE, ≥500→REFER, <500→REJECT |
| `compute_segment_score` | ACCOUNT | No | 3s | 5 | Weighted sum × 900. Segment-specific weights (6 features dairy, 5 kirana, 5 gig) |
| `compute_risk_pricing` | ACCOUNT | No | 1s | 5 | 5 bands: A1(12%), A2(14%), B1(16%), B2(18%), C(22%) |
| `check_fraud_signals` | ACCOUNT | No | 5s | 5 | Velocity (>3 apps/48h), device fingerprint presence |
| `generate_cam` | ACCOUNT | No | 10s | 5 | Credit Assessment Memo with FOIR, recommendation |
| `run_what_if` | ACCOUNT | No | 10s | 5 | Policy parameter simulator (min_score, max_amount impact) |
| `check_psl_classification` | ACCOUNT | No | 1s | 5 | Dairy→Agriculture, Kirana→MSME, Gig→Not eligible |
| `generate_explainability` | ACCOUNT | No | 3s | 5 | Bilingual (en/hi) borrower-facing reason codes |

### 4.4 Product Tools (5) — State: VERIFIED

| Tool | Authority | Confirmation | Timeout | CB | Key Logic |
|------|-----------|-------------|---------|-----|-----------|
| `design_dynamic_product` | GENERAL | No | 5s | 5 | Segment→schedule mapping, max_emi=income×0.4, moratorium triggers |
| `generate_seasonal_schedule` | GENERAL | No | 3s | 5 | Flush months (Oct-Feb) 130% EMI, lean (Apr-Jun) 60% EMI |
| `generate_daily_micro_schedule` | GENERAL | No | 3s | 5 | 26 working days/month, skip Sundays |
| `generate_payout_linked_schedule` | GENERAL | No | 3s | 5 | % deduction from platform payouts |
| `compute_insurance_premium` | GENERAL | No | 2s | 5 | PASHU_BIMA 3%, CROP_PMFBY 2%, HEALTH 4% + 18% GST |

### 4.5 Execution Tools (6) — State: CONFIRMED

| Tool | Authority | Confirmation | Timeout | CB | Key Logic |
|------|-----------|-------------|---------|-----|-----------|
| `generate_kfs` | ACCOUNT | No | 5s | 5 | RBI-mandatory Key Fact Statement, 3-day cooling off, APR calculation |
| `initiate_esign` | **WRITE** | **Yes** | 15s | 5 | Aadhaar eSign, OTP-based, requires maker-checker |
| `enroll_insurance` | **WRITE** | **Yes** | 10s | 5 | PASHU_BIMA/CROP enrollment |
| `setup_enach_mandate` | **WRITE** | **Yes** | 10s | 5 | Auto-debit authorization |
| `execute_disbursement` | **WRITE** | **Yes** | 15s | 5 | UPI/NEFT, masks beneficiary account, requires maker-checker |
| `register_cersai` | ACCOUNT | No | 10s | 5 | CERSAI charge registration for movable assets |

### 4.6 Servicing Tools (6) — State: VERIFIED

| Tool | Authority | Confirmation | Timeout | CB | Key Logic |
|------|-----------|-------------|---------|-----|-----------|
| `get_loan_status` | ACCOUNT | No | 5s | 5 | Balance, rate, next EMI, DPD, insurance status |
| `get_repayment_schedule` | ACCOUNT | No | 5s | 5 | Full schedule with actual vs expected |
| `process_prepayment` | **WRITE** | **Yes** | 5s | 5 | reduce_tenure or reduce_emi mode |
| `apply_moratorium` | **WRITE** | **Yes** | 5s | 5 | Pause EMI, no late fees, no NPA classification |
| `generate_statement` | ACCOUNT | No | 10s | 5 | Account statement, interest certificate PDF |
| `generate_noc` | ACCOUNT | No | 5s | 5 | No Objection Certificate on loan closure |

### 4.7 Monitoring Tools (5) — State: VERIFIED

| Tool | Authority | Confirmation | Timeout | CB | Key Logic |
|------|-----------|-------------|---------|-----|-----------|
| `poll_monitoring_signals` | GENERAL | No | 15s | 5 | 5 signal types: bank_txn, cooperative, platform, DPD, bureau |
| `evaluate_monitoring_triggers` | GENERAL | No | 5s | 5 | Segment-specific thresholds, severity HIGH/MEDIUM, action NONE/WATCH/ESCALATE |
| `execute_auto_intervention` | **WRITE** | **Yes** | 10s | 5 | nudge(auto)/moratorium(review)/restructure(review)/collection(auto) |
| `evaluate_graduation` | GENERAL | No | 5s | 5 | 6mo+90% OTR→rate reduction; 9mo+95%→limit increase; 12mo→top-up |
| `schedule_monitoring_job` | **WRITE** | No | 5s | 5 | Segment presets: dairy=weekly, kirana/gig=daily |

---

## Part V: Policy Engine

### 5.1 Structural Rules (Pre-Tool, Deterministic)

| # | Rule | Blocks When | RBI Reference |
|---|------|-------------|---------------|
| 1 | `identity_gate` | Non-identity tool + UNVERIFIED state | KYC mandate |
| 2 | `write_confirmation` | `requires_confirmation=True` + no borrower consent | Fair Practices Code |
| 3 | `kfs_mandatory` | `execute_disbursement`/`initiate_esign` + no KFS | Digital Lending Para 14 |
| 4 | `bureau_velocity` | `pull_credit_bureau` + ≥2 pulls in 48h | Borrower protection |
| 5 | `cooling_off_period` | `execute_disbursement` + within 3-day cooling off | Digital Lending Para 15 |
| 6 | `consent_required` | 5 data-fetch tools without consent token | Data protection |
| 7 | `maker_checker` | WRITE authority + no human approval | Operational risk |

### 5.2 Behavioral Rules (Post-Response, Regex)

| # | Rule | Severity | Triggers On |
|---|------|----------|-------------|
| 1 | `no_disclosure_before_verify` | error | Loan terms in response + UNVERIFIED state |
| 2 | `rbi_fair_practices_language` | error | "legal action", "arrest", "seize", "jabti" |
| 3 | `no_commitment_on_terms` | warning | "you will get", "guaranteed", "pakka" before finalization |
| 4 | `psl_accurate_classification` | error | "classify as", "mark it as agriculture" |
| 5 | `empathetic_tone_distress` | warning | Distress keywords without empathy in response |
| 6 | `no_rate_guarantee` | warning | Specific rate numbers before finalization |
| 7 | `insurance_opt_in` | warning | "insurance mandatory" for non-dairy segments |
| 8 | `grievance_disclosure` | error | Complaint without grievance officer reference |
| 9 | `no_override_on_authority` | error | "manager approved" without compliance enforcement |
| 10 | `pii_masked_readback` | error | Full 12-digit Aadhaar or PAN in response |

**Error rules** trigger response sanitization. **Warning rules** are logged for model fine-tuning.

---

## Part VI: Agent Layer

### 6.1 Conversation Loop (`app/agent/runtime.py`)

```
process_message(session, borrower_message)
    ├── detect_confirmation(borrower_message)        # Hindi/English patterns
    ├── get segment template from YAML               # scoring, schedule, monitoring config
    ├── get available tools for session.state         # filtered by CATEGORY_MIN_STATE
    ├── build_system_prompt(segment, state, tools)    # 10 critical rules embedded
    ├── LLM.chat(messages, tools)                     # First call
    │
    ├── For each tool_call:
    │     ├── ToolExecutor.execute()                  # 7-step pipeline
    │     ├── Audit log (PII-masked)
    │     └── If verify_aadhaar_* → verified:
    │           └── SessionMachine.transition(UNVERIFIED → VERIFIED)
    │
    ├── build_tool_result_prompt(last_result)
    ├── LLM.chat(messages + result)                   # Second call (explain to borrower)
    │
    ├── PolicyEngine.evaluate_response()              # 10 behavioral rules
    ├── If error: sanitize_response()                 # Replace with compliant text
    │
    └── Append to session.history, log audit event
```

### 6.2 System Prompt Template

The system prompt is dynamically constructed per-turn with:
- Lender name and borrower segment
- Current session state and available tools
- 10 critical rules (never disclose before verify, mask PII, empathy on distress, etc.)
- State-specific behavior instructions
- Segment greeting template from YAML

### 6.3 Confirmation Detection

Hindi/English bilingual patterns (`app/agent/confirmation.py`):

- **Confirm**: haan, theek hai, kar do, kijiye, manzoor, razi, yes, ok, confirm
- **Deny**: nahi, mat karo, rukiye, band, no, cancel, reject
- **Deny takes precedence** in mixed utterances
- **PII extraction**: Aadhaar (12-digit), OTP (6-digit), PAN (ABCDE1234F pattern)

---

## Part VII: Segment Templates

### 7.1 Dairy Farmer

```yaml
segment: {id: DAIRY_FARMER, channel: whatsapp, languages: [gu, hi]}
data_sources:
  required: [CREDIT_BUREAU, BANK_ACCOUNT_AA, DAIRY_COOPERATIVE]
  optional: [LAND_RECORDS, SATELLITE_NDVI, WEATHER_IMD]
scoring:
  model: dairy_score_v1
  features:
    - {name: pouring_regularity, weight: 0.25}
    - {name: pouring_volume_trend, weight: 0.18}
    - {name: cooperative_tenure, weight: 0.12}
    - {name: land_area, weight: 0.10}
    - {name: bureau_score, weight: 0.15}
    - {name: bank_stability, weight: 0.20}
product:
  type: SEASONAL_DYNAMIC
  amount_range: {min: 25000, max: 200000}
  insurance_required: PASHU_BIMA
  moratorium_triggers:
    - {type: WEATHER_HEAT, threshold_celsius: 38, duration_months: 1}
    - {type: PRODUCTION_DROP, threshold_percent: 40, duration_months: 1}
monitoring: {cadence: weekly}
graduation: {min_months: 12, min_otr: 0.90, amount_multiplier: 2.0, rate_reduction: 2.0}
```

### 7.2 Kirana Shop

```yaml
segment: {id: KIRANA_SHOP, channel: whatsapp, languages: [hi, mr]}
data_sources:
  required: [CREDIT_BUREAU, BANK_ACCOUNT_AA, GST_RETURNS]
scoring:
  model: vendor_score_v1
  features:
    - {name: gst_turnover_trend, weight: 0.30}
    - {name: bank_inflow_regularity, weight: 0.25}
    - {name: bureau_score, weight: 0.20}
    - {name: gst_filing_regularity, weight: 0.15}
    - {name: device_score, weight: 0.10}
product:
  type: DAILY_MICRO
  amount_range: {min: 50000, max: 500000}
  insurance_required: false
monitoring: {cadence: daily}
graduation: {min_months: 6, min_otr: 0.85, amount_multiplier: 1.5, rate_reduction: 1.5}
```

### 7.3 Gig Worker

```yaml
segment: {id: GIG_WORKER, channel: whatsapp, languages: [hi, en]}
data_sources:
  required: [CREDIT_BUREAU, BANK_ACCOUNT_AA, PLATFORM_EARNINGS]
scoring:
  model: gig_score_v1
  features:
    - {name: platform_earnings_trend, weight: 0.30}
    - {name: platform_rating, weight: 0.15}
    - {name: active_days, weight: 0.15}
    - {name: bank_stability, weight: 0.20}
    - {name: bureau_score, weight: 0.20}
product:
  type: PAYOUT_LINKED
  amount_range: {min: 10000, max: 200000}
  deduction_rate: 0.15
  insurance_required: false
monitoring: {cadence: daily}
graduation: {min_months: 6, min_otr: 0.85, amount_multiplier: 1.5, rate_reduction: 1.0}
```

---

## Part VIII: API Surface

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Service health check |
| POST | `/api/sessions` | Create lending session |
| GET | `/api/sessions/{id}` | Get session details |
| GET | `/api/loans/{id}` | Get loan application |
| GET | `/api/loans` | List loans (filter by lender, status) |
| GET | `/api/audit/logs/{session_id}` | Audit logs for session |
| GET | `/api/audit/tools/{session_id}` | Tool executions for session |
| GET | `/api/audit/loan/{loan_id}` | Merged loan timeline |
| POST | `/api/chat/message` | Send chat message (any channel) |
| POST | `/api/chat/webhook/whatsapp` | WhatsApp BSP webhook |
| GET | `/api/chat/sessions/active` | Active session count |

---

## Part IX: Test Coverage Matrix

| Component | Test File | Tests | Coverage |
|-----------|-----------|-------|----------|
| Health API | test_health.py | 1 | Endpoint response |
| DB Models | test_models.py | 3 | Enum values, state ordering |
| Schemas | test_schemas.py | 10 | All 27 Pydantic schemas |
| State Machine | test_session_machine.py | 6 | Valid/invalid transitions, minimum state |
| Tool Registry | test_tool_registry.py | 6 | Registration, lookup, category filter, state filter |
| Circuit Breaker | test_circuit_breaker.py | 5 | CLOSED/OPEN/HALF_OPEN transitions |
| Tool Executor | test_executor.py | 12 | All 7 pipeline steps, timeout, circuit breaker |
| Identity Tools | test_identity_tools.py | 12 | All 6 tools + state gating |
| Data Tools | test_data_tools.py | 18 | All 12 tools + confirmation gating |
| Scoring Tools | test_scoring_tools.py | 13 | All 8 tools + decision logic |
| Product Tools | test_product_tools.py | 9 | All 5 tools + segment templates |
| Execution Tools | test_execution_tools.py | 12 | All 6 tools + state/confirm/maker gates |
| Servicing Tools | test_servicing_tools.py | 9 | All 6 tools |
| Monitoring Tools | test_monitoring_tools.py | 12 | All 5 tools + trigger thresholds |
| Structural Policy | test_structural_policy.py | 15 | All 7 rules with pass/fail |
| Behavioral Policy | test_behavioral_policy.py | 17 | All 10 rules with pass/fail |
| Policy Engine | test_policy_engine.py | 9 | Orchestration of structural + behavioral |
| Confirmation | test_confirmation.py | 9 | Hindi/English confirm/deny + PII extraction |
| Audit | test_audit.py | 13 | PII masking, event emission, trail merge |
| Agent Runtime | test_agent_runtime.py | 9 | Conversation flow, tool triggering, empathy |
| Gateway | test_gateway.py | 16 | Adapters, session manager, HTTP endpoints |
| Integration E2E | test_integration.py | 15 | Full origination, REFER, monitoring, servicing, tool coverage |
| **Total** | **22 files** | **234** | |

---

## Part X: Running the Platform

```bash
# Install
pip install -e ".[dev]"

# Test
make test                    # 234 tests, ~1.6s

# Lint
make lint                    # ruff check + format check

# Run dev server
make run                     # uvicorn on :8000

# Docker
docker-compose up -d         # app + postgres + redis

# Migrate (requires DATABASE_URL)
make migrate                 # alembic upgrade head
```

---

*This specification documents every file, tool, rule, schema, endpoint, and test in the LendingOS-India platform as of Mission 13 completion.*
