# Working PoC Codebase: Embedded Credit-as-a-Service

**Date**: April 12, 2026  
**Status**: PoC Ready — 51 files, 7,330 lines, 31 passing tests, deploy-ready with Docker

---

## What Was Built

A complete, working lending intelligence platform for India's 300M underserved borrowers — integrating Cartesia Voice AI (10 Indian languages), Mem0 persistent borrower memory, MCP-enabled credit decisioning, and Finbox/ULI data orchestration across 33 borrower segments with 8 dynamic loan product types.

---

## Platform Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 3: LAST MILE AGENTS                                        │
│  Voice Agent (Cartesia, 10 langs) · WhatsApp Agent · Monitoring   │
├─────────────────────────────────────────────────────────────────────┤
│  LAYER 2: LENDING INTELLIGENCE                                     │
│  15 Scoring Models · 8 Dynamic Products · Data Quality · MCP      │
│  Compliance Engine · Graph Memory · Borrower Memory (Mem0)        │
├─────────────────────────────────────────────────────────────────────┤
│  LAYER 1: INTEGRATIONS                                             │
│  ULI (136 data services) · Finbox (BankConnect, DeviceConnect,    │
│  Sentinel AI) · Credit Bureaus · Account Aggregator · WhatsApp    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Source Code (`src/`)

### `src/agents/` — Borrower-Facing Agents

| File | Description |
|------|-------------|
| **voice_agent.py** | Cartesia Sonic-2 powered multilingual voice agent. Supports Hindi, Tamil, Telugu, Bengali, Gujarati, Kannada, Malayalam, Marathi, Punjabi, English. Segment-aware greetings (dairy farmer in Gujarati, fisherman in Tamil, ASHA worker in Hindi). Intent classification (loan inquiry, repayment, emergency, complaint, moratorium). Mem0 context retrieval for returning borrowers. Distress detection with human escalation. |
| **whatsapp_agent.py** | WhatsApp Business API agent with full conversation state machine: greeting → Aadhaar input → OTP verification → consent → data fetch → loan offer. Interactive button messages. Loan offer formatting with EMI/rate/tenure. Repayment reminders with UPI links. |
| **monitoring_agent.py** | Post-disbursement continuous monitoring. Segment-specific alert rules (milk pouring drop >30% for dairy, UPI collection drop >40% for vendor, sea condition alerts for fisherman, DBT delay for ASHA). Auto-interventions: moratorium, schedule adjustment, proactive outreach, emergency micro-loan, human escalation, graduation trigger, fraud flag. Weather event processing with mass moratorium capability. |

### `src/intelligence/` — Credit Intelligence Layer

| File | Description |
|------|-------------|
| **segment_intelligence.py** | 15 segment-specific scoring models: DairyScore (milk pouring + land + cooperative + satellite), VendorScore (UPI consistency + device behavioral + location), GigScore (platform earnings + multi-platform + rating), CropScore (land + satellite + KCC + weather + mandi prices), FisherScore (catch volume + vessel activity + sea conditions), SHGScore (group repayment + meeting attendance + NRLM grading), DBTScore (DBT regularity + service continuity), MerchantScore (transactions + GST + ONDC), SkillScore (institution + placement + sector demand), MedScore (income + insurance + treatment cost), IncomeScore, HousingScore, BridgeScore, ArtisanScore, AssetScore. Each model has weighted components, max score 900, minimum viable threshold, confidence scoring based on data completeness. |
| **dynamic_product_engine.py** | Designs all 8 dynamic loan products: (1) Seasonal Dynamic — EMI follows earning seasons, (2) Daily Micro — tiny daily UPI deductions with skip-on-low-collection, (3) Catch/Sale-Linked — repay when revenue lands at cooperative, (4) Income-Contingent — pay % of income not fixed EMI, (5) Moratorium-with-Trigger — auto-pause on weather/health events, (6) Bridge Zero-Interest — short-term gap funding for DBT delays, (7) Staged Disbursement — funds at milestones (medical/construction), (8) Payout-Linked — auto-deduct from gig platform payouts. Score-based amount/rate calibration. Insurance recommendations. Graduation pathway tracking (Tier 1→2→3). |
| **data_quality.py** | Entity resolution across data sources (Aadhaar ↔ PAN ↔ bank ↔ GST). Cross-source validation (bank AA vs UPI, KYC vs land records). Freshness checks with configurable max-age per source. Graceful degradation engine — identifies critical vs optional data per segment, scores quality, adjusts confidence. Determines if enough data exists to proceed or if fallback needed. |

### `src/mcp/` — MCP Server & Client

| File | Description |
|------|-------------|
| **lending_mcp_server.py** | MCP server exposing 10 lending intelligence tools: `trigger_credit_decision` (full pipeline), `fetch_segment_score`, `design_dynamic_product`, `check_portfolio_health`, `run_what_if` (policy simulation), `generate_compliance_report`, `detect_drift`, `compare_scorecards` (champion/challenger), `summarize_decision_logs`, `fetch_model_performance`. Every tool call logged with timestamp for audit. |
| **sentinel_client.py** | Client for Finbox Sentinel AI MCP server. Typed interface for: credit decisions, policy listing, shadow testing, fraud detection, model performance. Includes full PoC simulation mode when Sentinel endpoint not available (enterprise onboarding required). |

### `src/memory/` — Persistent Memory

| File | Description |
|------|-------------|
| **borrower_memory.py** | Mem0-powered persistent borrower memory. Stores: interaction history (voice/WhatsApp), loan context (applications, decisions, monitoring signals), credit signals (ULI data events), distress signals (for empathy routing). Retrieves: borrower context for agent conversations, loan history for graduation analysis, distress signals for escalation. DPDP Act compliant deletion. Stub mode when Mem0 unavailable. |
| **graph_memory.py** | Neo4j knowledge graph. Nodes: Borrower, Loan, Lender, Cooperative, Land, RepaymentEvent, WeatherEvent. Relationships: HAS_LOAN, FUNDED_BY, MEMBER_OF, OWNS_LAND, SHARES_ATTRIBUTE, AFFECTS. Fraud ring detection via shared-attribute clustering (devices, IPs, phones, addresses). Segment performance aggregation for RL reward surface. Cooperative/SHG membership tracking. Borrower network visualization. |

### `src/integrations/` — External Data & Services

| File | Description |
|------|-------------|
| **uli_connector.py** | ULI data orchestration with parallel async fetch from 136 services. Maps all data sources: Financial (credit bureaus, AA, GST, ITR, EPFO) and Non-Financial (land records across 9 states, dairy cooperative pouring, satellite NDVI, weather IMD, PMFBY, mandi prices, fishing GPS, SHG/NRLM, DBT, gig platforms, ONDC, UPI, device behavioral). Full simulation mode with realistic mock data for every source. |
| **finbox_client.py** | Finbox API client: BankConnect (session creation, bank statement analysis with cluster intelligence, fraud indicators, 400+ predictors), DeviceConnect (5000+ behavioral features, inclusion score), Superflows KYC (Aadhaar OTP + PAN verification). PoC simulation mode for all operations. |

### `src/lending/` — Core Lending Logic

| File | Description |
|------|-------------|
| **underwriting.py** | Credit decision engine. Per-segment policy thresholds (auto-approve, auto-reject, refer bands). Fraud score check (hard reject). Score-based amount calibration. Confidence check (low confidence → human review). DTI ratio validation. Every decision includes: decision_id, reasons array, risk_factors, explainability (primary reason + contributing factors), full audit trail with timestamp + model version + data sources. |
| **compliance.py** | Automated compliance for: (1) PSL auto-classification — maps 33 segments to agriculture/micro_enterprise/weaker_section/education/housing categories with amount limits, (2) RBI Digital Lending Guidelines — 7 checks (KYC, consent, KFS, cooling-off, disbursement, grievance, data privacy), (3) CLA Directions — minimum bank share, FLDG cap, risk sharing, (4) DPDP Act — purpose limitation, consent, minimization, retention, deletion, localization. PSL gap report generation per lender. |

### `src/api/` — FastAPI Application

| File | Description |
|------|-------------|
| **main.py** | FastAPI app with 21 routes, CORS, auth middleware, audit middleware. Health check exposes service configuration status. |
| **routes/borrower.py** | `POST /v1/borrower/apply` — Full loan application pipeline (ULI fetch → quality check → score → decide → product design → PSL classify → memory store). `POST /v1/borrower/context` — Retrieve borrower memory. `GET /v1/borrower/segments` — List all 33 segments with configuration. |
| **routes/lender.py** | `GET /v1/lender/portfolio/health` — Portfolio metrics. `GET /v1/lender/policies` — Sentinel AI policies. `POST /v1/lender/compliance/report` — Auto-generated compliance report. `POST /v1/lender/shadow-test` — Shadow test a policy. `GET /v1/lender/model/{id}/performance` — Model metrics. `GET /v1/lender/decision-log` — Decision audit log. |
| **routes/voice.py** | `POST /v1/agent/voice/session` — Create voice session. `POST /v1/agent/voice/input` — Process transcribed input. `GET /v1/agent/voice/tts` — Cartesia TTS streaming. `POST /v1/agent/voice/end` — End session. `POST /v1/agent/whatsapp/webhook` — WhatsApp incoming. `GET /v1/agent/voice/languages` — List 10 supported languages. |
| **middleware/audit.py** | Every API call logged: request_id, timestamp, method, path, client_ip, duration_ms, status_code. 7-year retention for RBI compliance. |
| **middleware/auth.py** | Lender API key validation. PoC mode accepts `poc_` prefixed keys. Per-lender context on request state. |

### `src/config/` — Configuration

| File | Description |
|------|-------------|
| **settings.py** | Central config for all services: Cartesia (API key, model, voice map, languages), Mem0 (API key, org, project), Finbox (API key, Sentinel MCP URL, DeviceConnect), ULI (OAuth2, mTLS cert paths), Database (Postgres, Redis, Neo4j), WhatsApp Business, Compliance (RBI DL, DPDP, PSL, CLA, audit retention). Environment-aware (dev/staging/production). |
| **segment_config.py** | All 33 borrower segments with: category (agricultural/informal/gig/lifecycle), channels (voice/WhatsApp/app/partner/embedded), primary languages, ULI data sources required, scoring model, product types, ticket range (INR), interest rate range, monitoring signals, PSL category, government guarantee scheme. |

---

## Tests (`tests/`) — 31 Passing

| File | Tests | Coverage |
|------|-------|---------|
| **test_segment_intelligence.py** | 7 tests — DairyScore full data, VendorScore partial data, GigScore, empty data neutral score, data quality full bundle, missing critical data, data quality assessment | Scoring models + data quality engine |
| **test_underwriting.py** | 7 tests — Auto-approve high score, auto-reject low score, refer mid score, fraud rejection, amount capping, ASHA worker low threshold, audit trail presence | Decision engine + explainability |
| **test_dynamic_product.py** | 7 tests — Dairy seasonal, vendor daily micro, ASHA bridge zero-interest, gig payout-linked, ITI income-contingent, score affects amount, graduation pathway | All 8 product types |
| **test_compliance.py** | 10 tests — PSL agriculture/weaker/micro/not-eligible, digital lending compliant/missing-consent, CLA compliant/FLDG-exceeded, DPDP compliance, PSL report generation | All 4 compliance frameworks |

---

## Analysis Documents (`analysis/`) — 8 Files

| Document | Contents |
|----------|---------|
| **pmf-analysis.md** | YC-aligned PMF signals (leading + lagging indicators), "hair on fire" test for dairy/ASHA/vendor, 5 concrete experiments for first 90 days, competitive analysis (vs Finbox standalone, MFIs, bureaus), defensibility moat (sovereign context + network effects + switching costs), traction milestones pre-seed→Series A, unit economics per segment |
| **product-roadmap.md** | Phase 0 (4 weeks: PoC sprint), Phase 1 (months 1-3: MVP 3 segments), Phase 2 (months 3-6: 8 segments + monitoring), Phase 3 (months 6-12: all 33 segments + co-lending), Phase 4 (months 12-24: scale + ONDC). Per-phase: deliverables, team size, metrics. Agent development lifecycle (build/test/evaluate/deploy/improve). Technical debt management. |
| **gtm-strategy.md** | Sales playbook for 5 lender personas (PSB, agri NBFC, MFI, green NBFC, fintech) with pain points, value prop, pricing, objection handling, pilot structure. First 10 lender acquisition plan. Messaging for technical/business/board/regulator audiences. 6 pricing models. Partnership strategy (Finbox, RBIH, NABARD, cooperatives). |
| **cost-analysis.md** | API costs (Cartesia $0-239/mo, Mem0 $0-249/mo, Finbox INR 3.5-8.25L/mo, bureaus INR 1.6-2.75L/mo). Infra (AWS/GCP $110-$4,250/mo). Team (INR 7.5L-103L/mo). Total burn by phase. Revenue model. Break-even ~Month 18-20. Funding: Pre-seed 50-75L, Seed 3-4Cr, Series A 10-15Cr. Stack optimization opportunities (40-70% savings). |
| **compliance-evaluation.md** | Clause-by-clause: RBI Digital Lending (12 clauses), CLA Directions (6 checks), DPDP Act (6 sections), PSL classification rules for all segments, AA framework consent flow, voice AI recording consent, WhatsApp financial messaging rules, per-lender compliance matrix, audit trail requirements (7-year retention). |
| **risk-management.md** | 23 risks across technical (8), credit (7), operational (6), regulatory (5), business (5). Risk matrices with probability/impact. Risk appetite by lender type. 10-scenario incident response playbook (mass default, fraud ring, wrong loan terms, outage, data breach, regulatory inquiry, borrower distress, model drift, data deletion, cooperative data loss). Insurance/guarantee integration (CGTMSE, PMFBY, FLDG). Model risk management. |
| **three-layer-gap-analysis.md** | Layer 1: Current state of PSB/NBFC/SFB/MFI/platform tech stacks and integration complexity. Layer 2: Finbox dependency analysis (12 products rated critical/high/medium/low), what we build on top. Layer 3: Voice AI gap (Cartesia = TTS only, need ASR provider). 3 integration flows (PSB agriculture, MFI SHG graduation, ONDC embedded). Data availability by segment. 3 lender personas (advanced/evolving/basic). Build vs buy matrix. |
| **stack-optimization.md** | Complete solution stack inventory. Production readiness per component (40-80%). Optimization: model layer (TTS caching, edge intent classifier, ML model training), application layer (connection pooling, batching, WebSocket voice), infra layer (spot instances, read replicas, multi-region). Communication guide for each platform layer to different audiences. Testing strategy (unit/integration/load/security/compliance). |

---

## Deployment Infrastructure

| File | Description |
|------|-------------|
| **Dockerfile** | Python 3.11-slim, production-ready with 4 Uvicorn workers |
| **docker-compose.yml** | Full stack: API server + MCP server + PostgreSQL 16 + Redis 7 + Neo4j 5 with health checks |
| **requirements.txt** | 18 production dependencies (FastAPI, Cartesia, Mem0, MCP SDK, Neo4j, SQLAlchemy, Redis, etc.) |
| **.env.example** | All configuration variables with placeholder values (no secrets) |
| **Makefile** | Commands: `make dev` (hot reload), `make run` (production), `make test`, `make docker-up` |

---

## 33 Borrower Segments Configured

**Agricultural (8)**: Dairy farmer, Crop farmer, Fisherman, Warehouse receipt, Solar pump, Mandi trader, FPO, Community solar

**Informal Economy (8)**: Street vendor, Domestic worker, Beauty salon, Handloom weaver, Potter/artisan, Private teacher, ASHA worker, SHG woman

**Gig/Platform (7)**: Delivery worker, Auto-rickshaw, Urban Company, Ola/Uber driver, Social reseller, Kirana ONDC, EV buyer

**Lifecycle (10)**: Medical patient, IVF borrower, ITI student, Upskilling, Rental deposit, Home builder, Wedding, Death bridge, Maternity, Construction worker

---

## How to Run

```bash
# Development (hot reload)
cp .env.example .env  # Fill in API keys
make dev

# Production (Docker)
make docker-up

# Tests
make test
```

---

## Critical Dependencies Identified

1. **Cartesia provides TTS only** — Need separate ASR (Bhashini/Google/Deepgram) for speech-to-text
2. **Finbox Sentinel AI MCP** — Enterprise onboarding required, no public docs; PoC simulation built as fallback
3. **ULI (RBIH)** — No public developer documentation; requires institutional TSP registration
4. **Scoring models are rule-based** — Need real loan outcome data to train ML models (XGBoost/LightGBM)
5. **Platform builds ON Finbox** — Layer 4-5 intelligence + agents on top of Finbox Layer 2-3 infrastructure
