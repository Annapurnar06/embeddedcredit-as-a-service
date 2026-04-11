# Embedded Credit-as-a-Service: Platform Overview

## For Lenders, Partners, and Platform Businesses

---

## WHAT IS THE PLATFORM

Embedded Credit-as-a-Service is a full-stack lending infrastructure that enables banks, NBFCs, fintechs, and platform businesses to originate, underwrite, disburse, and monitor loans across India's underserved borrower segments -- without building any of the underlying data, decisioning, or distribution infrastructure themselves.

```
    WHAT YOU GET
    ════════════════════════════════════════════════════════

    ┌──────────────────────────────────────────────────────┐
    │                                                       │
    │  "Plug in your capital.                              │
    │   We provide the intelligence, the data,              │
    │   the borrower access, and the monitoring."           │
    │                                                       │
    │   Your capital + Our stack = Credit at scale          │
    │   to 33 borrower segments you can't reach alone       │
    │                                                       │
    └──────────────────────────────────────────────────────┘
```

---

## PRODUCT CATALOGUE

### The 12 Products, What Each Does, and Who Uses It

```
    ┌─────────────────────────────────────────────────────────────────┐
    │                      PRODUCT MAP                                 │
    │                                                                  │
    │   DATA LAYER              DECISIONING LAYER                     │
    │   ┌────────────────┐     ┌────────────────────────┐            │
    │   │ DPI             │     │ Sentinel AI              │            │
    │   │ BankConnect     │────►│ RiskEngine               │            │
    │   │ DeviceConnect   │     │ MCP Protocol             │            │
    │   │ Multi AA        │     └──────────┬───────────────┘            │
    │   │ KYC             │                │                           │
    │   │ Superflows      │                ▼                           │
    │   └────────────────┘     ┌────────────────────────┐            │
    │                           │ DISTRIBUTION LAYER      │            │
    │                           │ Prism (lender matching)  │            │
    │                           │ Journey Studio (flows)   │            │
    │                           │ Digital Onboarding       │            │
    │                           │ LOS (origination)        │            │
    │                           │ Embedded Finance         │            │
    │                           └────────────────────────┘            │
    └─────────────────────────────────────────────────────────────────┘
```

---

### PRODUCT 1: SENTINEL AI -- The Decisioning Brain

**What it is**: AI-powered credit decisioning engine with no-code policy builder, shadow testing, champion/challenger, fraud detection, and 360-degree monitoring.

**What it does for you**:

```
    ┌─────────────────────────────────────────────────────────┐
    │  YOUR RISK TEAM TODAY              WITH SENTINEL AI      │
    │                                                          │
    │  Build scorecards in Excel         No-code policy        │
    │  → 3-6 months to deploy            builder → 3 days     │
    │                                                          │
    │  Test new models manually          Shadow testing        │
    │  → High risk, slow                 → Zero-risk parallel  │
    │                                    evaluation            │
    │                                                          │
    │  Monitor via monthly MIS           360° real-time        │
    │  → Detect problems in arrears      monitoring → detect   │
    │                                    drift in hours        │
    │                                                          │
    │  One model per product             Champion/Challenger   │
    │  → Stale, no experimentation       → Continuous          │
    │                                    improvement           │
    │                                                          │
    │  Compliance = separate audit       Every decision logged │
    │  → Expensive, retroactive          with full audit trail │
    │                                    → Compliance built-in │
    └─────────────────────────────────────────────────────────┘
```

**Who uses it**: Risk teams, credit heads, chief risk officers, compliance officers

**Client flow**:
1. Risk team logs into Sentinel AI dashboard
2. Creates a credit policy using no-code builder (e.g., "Dairy Animal Purchase Loan")
3. Defines data sources (bureau, bank, cooperative, satellite -- pulled via DPI/ULI)
4. Configures scoring model (weights per feature)
5. Sets product parameters (amount range, rate bands, schedule type)
6. Deploys in shadow mode alongside existing model
7. Compares performance over 2-4 weeks
8. Promotes to production with one click
9. Monitors live via 360-degree dashboard
10. AI Copilot answers questions in natural language: "Why did we reject application #4521?"

---

### PRODUCT 2: BANKCONNECT -- Bank Statement Intelligence

**What it is**: AI-powered bank statement analysis with cluster transaction intelligence that detects fraud patterns, income stability, and spending behavior from raw banking data.

**What it does for you**:

```
    RAW BANK STATEMENT          BANKCONNECT OUTPUT
    ═══════════════════          ════════════════════

    500 transactions             Income: INR 22,000/mo
    in 6 months                  (stable, cooperative credits)

    Messy narrations             Salary: none detected
    "UPI-CR-AMUL-DAI..."        Self-employed: dairy income

    No categorization            Spending: INR 14,000/mo
                                 Savings ratio: 36%

    Hard to spot fraud           Cluster Intelligence:
                                 ┌─────────────────────┐
                                 │ Round-trip detection │
                                 │ Cash deposit patterns│
                                 │ Circular transactions│
                                 │ Income inflation     │
                                 └─────────────────────┘

                                 FOIR: 0.38 (healthy)
                                 Risk flag: NONE
```

**Who uses it**: Underwriting teams, fraud analysts

**Client flow**: Integrated via API during application processing. Returns structured income/expense analysis + fraud flags in under 30 seconds.

---

### PRODUCT 3: DEVICECONNECT -- Alternative Data Scoring

**What it is**: Extracts 5,000+ behavioral features from borrower's device (with consent) to generate an inclusion score for thin-file borrowers who lack bureau history.

**What it does for you**: Scores borrowers that bureau data alone would reject. Combines device signals (app usage, location stability, communication patterns) with ULI non-financial data to build a composite credit profile.

**Who uses it**: Lenders targeting new-to-credit, informal economy, gig workers

**Client flow**: SDK integrated into borrower-facing app. Data collected with consent. Score returned via API alongside bureau score for blended decisioning.

---

### PRODUCT 4: DPI (Digital Public Infrastructure)

**What it is**: Single integration point for ULI (136 data services), ONDC (commerce data), and Account Aggregator (financial data). The data pipe that powers everything.

**What it does for you**:

```
    WITHOUT DPI                     WITH DPI
    ════════════                    ════════

    Build 10+ integrations          1 API → all 136 services
    6-12 months per source          Days to onboard
    INR 10-50L per lender           Near-zero marginal cost
    Patchy coverage                 Universal coverage
    No cross-source validation      Entity resolution +
                                    consistency scoring
    Manual consent management       Aadhaar-based consent,
                                    fully logged
```

**Who uses it**: Technology teams, product teams, anyone building lending products

**Client flow**: Single API integration. Configure which data sources per product. Parallel fetch returns enriched, validated, confidence-scored data packet per borrower.

---

### PRODUCT 5: PRISM -- Lender Marketplace & Matching

**What it is**: Multi-lender marketplace that matches approved borrowers to the optimal lender based on risk appetite, PSL requirements, geography, capital availability, and co-lending structures.

**What it does for you**:

```
    ┌─────────────────────────────────────────────────────────┐
    │  FOR BANKS (Capital Providers):                          │
    │                                                          │
    │  → Pre-underwritten borrower flow                        │
    │  → PSL-classified (agriculture, MSME, weaker sections)   │
    │  → Risk already assessed by Sentinel AI                  │
    │  → Co-lending structures available (RBI CLA compliant)   │
    │  → No origination cost -- borrowers arrive ready         │
    │                                                          │
    │  YOUR ROLE: Provide capital. We provide everything else. │
    └─────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────┐
    │  FOR NBFCs / FINTECHS (Operational Partners):            │
    │                                                          │
    │  → Access bank capital at lower cost via co-lending      │
    │  → FLDG structures for risk sharing                      │
    │  → Segment expertise valued (agri, gig, MSME)           │
    │  → Technology already handled by platform                │
    │                                                          │
    │  YOUR ROLE: Domain expertise + risk appetite. We         │
    │  provide technology, data, and distribution.             │
    └─────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────┐
    │  FOR PLATFORM BUSINESSES (Demand Partners):              │
    │                                                          │
    │  → Embed credit in your user journey (ONDC, gig, etc.)  │
    │  → Earn distribution fee per loan originated             │
    │  → Improve user retention (stickiness)                   │
    │  → Zero lending risk -- fully passed through             │
    │                                                          │
    │  YOUR ROLE: Provide borrower access. We provide          │
    │  underwriting, lender matching, and lifecycle mgmt.      │
    └─────────────────────────────────────────────────────────┘
```

**Client flow**: Configure lender profile (risk appetite, segment preferences, geography, ticket size, PSL targets). System auto-matches every approved application to best-fit lender. Dashboard shows fill rates, match quality, and portfolio composition.

---

### PRODUCT 6: JOURNEY STUDIO -- No-Code Loan Journey Builder

**What it is**: GenAI-powered journey builder that creates complete borrower-facing loan journeys (screens, flows, validations, integrations) in days instead of months. With A/B testing built in.

**What it does for you**:

```
    OLD WAY                         JOURNEY STUDIO
    ════════                        ══════════════

    Product team writes PRD         Describe journey in
    → 2 weeks                       natural language

    Design team creates UI          GenAI generates screens
    → 3 weeks                       + flows + validations

    Eng team builds + tests         Preview, test, deploy
    → 8-12 weeks                    → 3 days

    A/B test requires               Built-in A/B testing
    separate infrastructure         → Compare conversion

    Compliance review               "Journey IS policy"
    → Separate process              → Compliance embedded
                                    in flow design
```

**Who uses it**: Product managers, business heads, compliance teams

**Client flow**: Log in → Describe the loan product and borrower segment → GenAI generates journey → Review/edit screens → Configure data sources and policies → Deploy → Monitor conversion and A/B test results.

---

### PRODUCT 7: LOS -- Loan Origination System

**What it is**: End-to-end loan origination workflow from application through disbursement, including document management, approvals, e-sign, and payment processing.

**Who uses it**: Operations teams, loan processing teams

**Client flow**: Integrated with Sentinel AI for auto-decisioning. Applications that pass policy flow through automated disbursement. Edge cases route to human review queues. Full audit trail.

---

### PRODUCT 8: SUPERFLOWS -- KYC/KYB Verification Suite

**What it is**: Configurable verification workflow builder. Risk teams define which checks run in which order, with real-time monitoring of pass/fail rates.

**Who uses it**: Risk teams, operations teams

**Client flow**: Configure verification template (e.g., Aadhaar OTP + PAN match + bank account verification + land record check). Attach to loan product. Every application runs through the configured pipeline. Dashboard shows pass rates per step, drop-offs, and fraud flags.

---

### PRODUCTS 9-12: Supporting Infrastructure

| Product | What It Does | Who Uses It |
|---------|-------------|-------------|
| **Multi AA** | Fetches financial data from all Account Aggregators with consent management | Underwriting teams |
| **KYC** | Aadhaar, PAN, and eKYC verification | Onboarding |
| **Digital Onboarding** | Adaptive, omni-channel onboarding (app, web, WhatsApp, voice) | Product teams |
| **Embedded Finance** | SDK/API for embedding credit into partner apps (ONDC, gig platforms, OEM sites) | Platform businesses, LSPs |

---

## HOW WORK GETS DONE: LENDER CLIENT FLOWS

### Flow 1: Bank Wanting to Meet PSL Targets via Agriculture Lending

```
    ┌─────────────────────────────────────────────────────────────┐
    │  BANK: "We need INR 500 Cr more in agriculture PSL         │
    │         by March. We don't have rural distribution."        │
    │                                                              │
    │  WEEK 1: SETUP                                              │
    │  ┌───────────────────────────────────────────────────┐     │
    │  │ 1. Bank signs co-lending agreement                 │     │
    │  │ 2. Configures Prism profile:                       │     │
    │  │    - Segment: agriculture (dairy, crop, FPO)       │     │
    │  │    - Geography: Gujarat, Maharashtra, MP           │     │
    │  │    - Ticket size: INR 25K - 5L                     │     │
    │  │    - PSL: must classify as agriculture              │     │
    │  │    - Risk: FLDG from fintech partner available      │     │
    │  │ 3. Reviews Sentinel AI policies for dairy/crop     │     │
    │  │    segments (pre-configured, bank approves)         │     │
    │  │ 4. IT team integrates disbursement API              │     │
    │  └───────────────────────────────────────────────────┘     │
    │                                                              │
    │  WEEK 2-3: SHADOW MODE                                      │
    │  ┌───────────────────────────────────────────────────┐     │
    │  │ 1. Platform routes test applications to bank       │     │
    │  │ 2. Bank reviews Sentinel AI decisions in parallel  │     │
    │  │    (shadow mode -- no real lending yet)             │     │
    │  │ 3. Bank risk team validates scoring methodology    │     │
    │  │ 4. Adjusts risk appetite parameters if needed      │     │
    │  └───────────────────────────────────────────────────┘     │
    │                                                              │
    │  WEEK 4+: LIVE                                              │
    │  ┌───────────────────────────────────────────────────┐     │
    │  │ 1. Approved applications auto-routed to bank       │     │
    │  │ 2. Bank capital disbursed via API                  │     │
    │  │ 3. Monitoring agent watches all live loans          │     │
    │  │ 4. Monthly portfolio review on Sentinel dashboard  │     │
    │  │ 5. PSL report auto-generated for RBI compliance    │     │
    │  └───────────────────────────────────────────────────┘     │
    │                                                              │
    │  RESULT:                                                     │
    │  ┌───────────────────────────────────────────────────┐     │
    │  │ ✓ INR 500 Cr PSL agriculture target met            │     │
    │  │ ✓ Zero branch infrastructure needed                │     │
    │  │ ✓ Pre-underwritten, monitored portfolio            │     │
    │  │ ✓ FLDG covers first-loss for new segments          │     │
    │  │ ✓ Full compliance documentation auto-generated     │     │
    │  └───────────────────────────────────────────────────┘     │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```

---

### Flow 2: NBFC Launching Gig Worker Lending Product

```
    ┌─────────────────────────────────────────────────────────────┐
    │  NBFC: "We want to lend to delivery workers. We have        │
    │         capital but no data infrastructure for gig economy." │
    │                                                              │
    │  STEP 1: PRODUCT DESIGN (Journey Studio)                    │
    │  ┌───────────────────────────────────────────────────┐     │
    │  │ Product manager describes in natural language:      │     │
    │  │ "Delivery worker vehicle loan, INR 50K-2L,         │     │
    │  │  payout-linked repayment from Swiggy/Zomato,       │     │
    │  │  12-month tenure, daily micro-deductions"           │     │
    │  │                                                     │     │
    │  │ Journey Studio generates:                           │     │
    │  │ → WhatsApp-first onboarding flow                    │     │
    │  │ → DeviceConnect + platform API data collection      │     │
    │  │ → Sentinel AI policy (GIG_DELIVERY_VEHICLE)         │     │
    │  │ → Payout-linked repayment structure                 │     │
    │  │ → Complete journey in 3 days                        │     │
    │  └───────────────────────────────────────────────────┘     │
    │                                                              │
    │  STEP 2: RISK CONFIGURATION (Sentinel AI)                   │
    │  ┌───────────────────────────────────────────────────┐     │
    │  │ Risk team configures scoring model:                 │     │
    │  │ → Platform rating weight: 25%                       │     │
    │  │ → Delivery count/month weight: 20%                  │     │
    │  │ → Multi-platform presence weight: 15%               │     │
    │  │ → Bureau score weight: 20%                          │     │
    │  │ → DeviceConnect Inclusion Score weight: 20%         │     │
    │  │                                                     │     │
    │  │ Shadow test against 500 historical applications     │     │
    │  │ → Approval rate: 42% (vs. 18% with bureau-only)    │     │
    │  │ → Projected NPA: 4.2% (vs. 3.8% bureau-only)      │     │
    │  │ → Additional addressable market: 2.3x              │     │
    │  └───────────────────────────────────────────────────┘     │
    │                                                              │
    │  STEP 3: DISTRIBUTION (Prism + Embedded Finance)            │
    │  ┌───────────────────────────────────────────────────┐     │
    │  │ Option A: Direct -- WhatsApp bot in Swiggy         │     │
    │  │           driver groups                             │     │
    │  │ Option B: Embedded -- "Vehicle loan" button in      │     │
    │  │           gig platform partner app                  │     │
    │  │ Option C: Co-lend -- Bank provides 80% capital,     │     │
    │  │           NBFC provides 20% + operational expertise │     │
    │  └───────────────────────────────────────────────────┘     │
    │                                                              │
    │  STEP 4: LIVE + MONITOR                                     │
    │  ┌───────────────────────────────────────────────────┐     │
    │  │ Monitoring agent tracks:                            │     │
    │  │ → Daily platform earnings vs. expected              │     │
    │  │ → Auto-adjusts if platform switches payout cycle    │     │
    │  │ → Triggers collections agent if 5+ days behind      │     │
    │  │ → Triggers graduation offer after 6 months if       │     │
    │  │   repayment perfect                                 │     │
    │  └───────────────────────────────────────────────────┘     │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```

---

### Flow 3: Platform Business Embedding Credit (ONDC Merchant / Gig Platform)

```
    ┌─────────────────────────────────────────────────────────────┐
    │  ONDC NETWORK PARTICIPANT: "Our sellers need working         │
    │  capital. We want to offer credit without becoming a lender."│
    │                                                              │
    │  INTEGRATION (Embedded Finance SDK)                         │
    │  ┌───────────────────────────────────────────────────┐     │
    │  │ 1. Embed SDK in seller dashboard                   │     │
    │  │ 2. Pre-qualification runs in background:           │     │
    │  │    - ONDC order history (via DPI)                   │     │
    │  │    - GST returns (via ULI)                          │     │
    │  │    - Bank statements (via AA)                       │     │
    │  │    - Bureau check                                   │     │
    │  │ 3. Eligible sellers see "Working Capital Available" │     │
    │  │    with pre-approved amount                         │     │
    │  │ 4. One-click acceptance → disbursed in minutes      │     │
    │  │ 5. Repayment auto-deducted from order settlements   │     │
    │  └───────────────────────────────────────────────────┘     │
    │                                                              │
    │  WHAT PLATFORM GETS:                                        │
    │  ┌───────────────────────────────────────────────────┐     │
    │  │ ✓ Distribution fee per loan originated              │     │
    │  │ ✓ Seller retention improves (stickiness)            │     │
    │  │ ✓ Seller GMV increases (more inventory capital)     │     │
    │  │ ✓ Zero credit risk (fully passed to lender)         │     │
    │  │ ✓ No RBI licensing required (LSP model)             │     │
    │  └───────────────────────────────────────────────────┘     │
    │                                                              │
    │  WHAT LENDER GETS:                                          │
    │  ┌───────────────────────────────────────────────────┐     │
    │  │ ✓ Pre-qualified borrower flow from platform         │     │
    │  │ ✓ Commerce data (order history) improves UW quality │     │
    │  │ ✓ Payout-linked repayment = near-zero collection    │     │
    │  │   cost                                              │     │
    │  │ ✓ MSME PSL classification                           │     │
    │  └───────────────────────────────────────────────────┘     │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```

---

## VALUE PROPOSITION BY CLIENT TYPE

### For Banks

```
    ┌─────────────────────────────────────────────────────────────┐
    │                                                              │
    │  PROBLEM                        SOLUTION                    │
    │  ════════                       ════════                    │
    │                                                              │
    │  PSL shortfall penalties         Auto-classified PSL flow   │
    │  (INR 100s Cr annually)          from 33 underserved        │
    │                                  segments                   │
    │                                                              │
    │  No rural/informal               Voice + WhatsApp agents    │
    │  distribution                    reach borrowers you        │
    │                                  can't reach with branches  │
    │                                                              │
    │  Can't underwrite thin-file      ULI + DeviceConnect +      │
    │  borrowers                       segment intelligence       │
    │                                  = shadow credit files      │
    │                                                              │
    │  High origination cost           Near-zero marginal cost    │
    │  (INR 15,000/loan)              for agent-originated loans  │
    │                                                              │
    │  Static, stale models            Sentinel AI continuously   │
    │                                  learning from outcomes     │
    │                                                              │
    │  Co-lending compliance           RBI CLA-compliant          │
    │  complexity                      structures built-in        │
    │                                                              │
    │  RESULT: Access INR 25-30L Cr addressable credit market    │
    │  you couldn't profitably serve before                       │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```

### For NBFCs

```
    ┌─────────────────────────────────────────────────────────────┐
    │                                                              │
    │  PROBLEM                        SOLUTION                    │
    │                                                              │
    │  High cost of capital            Co-lend with banks via     │
    │  (vs. banks)                     Prism → blended lower cost │
    │                                                              │
    │  Building data infra             Plug into existing DPI,    │
    │  is expensive                    Sentinel AI, BankConnect   │
    │                                                              │
    │  Limited to known                Reach 33 segments via      │
    │  segments                        platform distribution      │
    │                                                              │
    │  Collections infrastructure      Monitoring agent handles    │
    │  expensive at small ticket       post-disburse proactively  │
    │                                                              │
    │  RESULT: 3x addressable market at lower infra cost          │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```

### For Fintechs / LSPs

```
    ┌─────────────────────────────────────────────────────────────┐
    │                                                              │
    │  PROBLEM                        SOLUTION                    │
    │                                                              │
    │  Need lending license            Operate as LSP with full   │
    │  or bank partner                 platform support            │
    │                                                              │
    │  Building underwriting           Sentinel AI + DPI = ready  │
    │  from scratch takes years        to deploy in weeks         │
    │                                                              │
    │  Finding lenders for             Prism auto-matches to      │
    │  each borrower segment           best-fit lender             │
    │                                                              │
    │  FLDG capital tied up            Portfolio-level FLDG        │
    │  inefficiently                   optimization via Prism     │
    │                                                              │
    │  RESULT: Launch lending products in weeks, not years         │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```

### For Platform Businesses

```
    ┌─────────────────────────────────────────────────────────────┐
    │                                                              │
    │  PROBLEM                        SOLUTION                    │
    │                                                              │
    │  Users need credit but           Embedded Finance SDK =     │
    │  you're not a lender             credit widget in your app  │
    │                                                              │
    │  Seller/driver churn             Credit access = stickiness │
    │  is high                         (users stay for the loan)  │
    │                                                              │
    │  No revenue from                 Distribution fee per       │
    │  financial services              loan originated             │
    │                                                              │
    │  Don't want credit risk          100% pass-through to       │
    │                                  licensed lenders            │
    │                                                              │
    │  RESULT: New revenue stream with zero credit risk            │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```

---

## HOW IMPACT IS COMMUNICATED

### What the Platform Reports to Each Client

```
    ┌─────────────────────────────────────────────────────────────┐
    │  LENDER DASHBOARD (Real-time)                                │
    │                                                              │
    │  ┌──────────────────────────────────────────────┐           │
    │  │ ORIGINATION                                   │           │
    │  │ Applications today:        342                │           │
    │  │ Auto-approved:             189 (55%)          │           │
    │  │ Manual review queue:        28 (8%)           │           │
    │  │ Rejected:                  125 (37%)          │           │
    │  │ Avg. decision time:        12 seconds         │           │
    │  │ Avg. disbursement time:    8 minutes           │           │
    │  └──────────────────────────────────────────────┘           │
    │                                                              │
    │  ┌──────────────────────────────────────────────┐           │
    │  │ PORTFOLIO HEALTH                              │           │
    │  │ Active loans:              14,283             │           │
    │  │ AUM:                       INR 182 Cr         │           │
    │  │ 0 DPD:                     91.2%              │           │
    │  │ 30+ DPD:                    5.1%              │           │
    │  │ 90+ DPD:                    1.8%              │           │
    │  │ NPA rate:                   2.1%              │           │
    │  │ Proactive interventions:   412 this month     │           │
    │  │ Interventions that prevented default: 78%     │           │
    │  └──────────────────────────────────────────────┘           │
    │                                                              │
    │  ┌──────────────────────────────────────────────┐           │
    │  │ PSL COMPLIANCE                                │           │
    │  │ Agriculture:    INR 89 Cr / 120 Cr target     │           │
    │  │ Weaker section: INR 34 Cr / 40 Cr target      │           │
    │  │ MSME:           INR 52 Cr / 60 Cr target      │           │
    │  │ Projected Q4:   On track for all categories   │           │
    │  └──────────────────────────────────────────────┘           │
    │                                                              │
    │  ┌──────────────────────────────────────────────┐           │
    │  │ MODEL PERFORMANCE                             │           │
    │  │ Gini coefficient:          0.72 (good)        │           │
    │  │ KS statistic:              0.48 (good)        │           │
    │  │ Model drift detected:      NONE               │           │
    │  │ Champion vs. Challenger:   Champion +2.3% KS  │           │
    │  │ Shadow test: new dairy v2  Running (week 2/4) │           │
    │  └──────────────────────────────────────────────┘           │
    │                                                              │
    │  ┌──────────────────────────────────────────────┐           │
    │  │ UNIT ECONOMICS                                │           │
    │  │ Avg. ticket size:          INR 68,000         │           │
    │  │ Acquisition cost/loan:     INR 180             │           │
    │  │   (vs. INR 15,000 branch)                     │           │
    │  │ Blended yield:             16.2%              │           │
    │  │ Credit cost:                2.1%              │           │
    │  │ Net margin:                 8.4%              │           │
    │  │ ROA on this portfolio:     4.2%               │           │
    │  └──────────────────────────────────────────────┘           │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```

---

## INTEGRATION MODEL: HOW YOU CONNECT

```
    ┌─────────────────────────────────────────────────────────────┐
    │  INTEGRATION OPTIONS                                         │
    │                                                              │
    │  OPTION A: FULL STACK (most common for new lenders)          │
    │  ┌────────────────────────────────────────────────┐         │
    │  │ You provide: Capital + risk appetite                │         │
    │  │ Platform provides: Everything else                  │         │
    │  │ Integration: API for disbursement + dashboard access│         │
    │  │ Time to live: 2-4 weeks                             │         │
    │  └────────────────────────────────────────────────┘         │
    │                                                              │
    │  OPTION B: MODULAR (for lenders with existing infra)         │
    │  ┌────────────────────────────────────────────────┐         │
    │  │ Pick products you need:                             │         │
    │  │ □ Sentinel AI only (decisioning)                    │         │
    │  │ □ BankConnect only (statement analysis)             │         │
    │  │ □ DPI only (ULI data access)                        │         │
    │  │ □ Prism only (lender matching)                      │         │
    │  │ □ Journey Studio only (journey builder)             │         │
    │  │ Integration: REST APIs, webhooks, SDK               │         │
    │  │ Time to live: 1-2 weeks per product                 │         │
    │  └────────────────────────────────────────────────┘         │
    │                                                              │
    │  OPTION C: EMBEDDED (for platform businesses)                │
    │  ┌────────────────────────────────────────────────┐         │
    │  │ You provide: Borrower access + distribution         │         │
    │  │ Platform provides: Underwriting + lender matching   │         │
    │  │ Integration: SDK / widget / WhatsApp API            │         │
    │  │ Time to live: 1-2 weeks                             │         │
    │  └────────────────────────────────────────────────┘         │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```

---

## THE MCP ADVANTAGE: WHY AGENTIC MATTERS TO LENDERS

```
    ┌─────────────────────────────────────────────────────────────┐
    │                                                              │
    │  WITHOUT MCP                      WITH MCP                  │
    │  ═══════════                      ════════                  │
    │                                                              │
    │  Your risk analyst asks:          Your AI copilot asks:     │
    │  "What's our dairy NPA            "What's our dairy NPA     │
    │   trending?"                       trending?"               │
    │                                                              │
    │  → Opens 3 dashboards             → Sentinel AI returns:    │
    │  → Exports CSV                    "Dairy NPA at 2.1%,       │
    │  → Builds pivot table              down from 2.8% last      │
    │  → 45 minutes later               quarter. Heat wave        │
    │    has answer                       moratorium policy        │
    │                                    reduced defaults by       │
    │                                    60% in affected pins.     │
    │                                    Recommend extending to    │
    │                                    3 more districts."        │
    │                                    → 3 seconds.             │
    │                                                              │
    │  Your compliance team needs       AI copilot generates:     │
    │  quarterly audit:                 Complete audit trail       │
    │                                   for every decision,       │
    │  → 2 weeks of manual              every adjustment,         │
    │    file preparation               every intervention.       │
    │                                   → 1 click. PDF ready.     │
    │                                                              │
    │  MCP turns Sentinel AI from a tool your team USES           │
    │  into a colleague your team TALKS TO.                       │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```

---

## SECURITY, COMPLIANCE, AND GOVERNANCE

```
    ┌─────────────────────────────────────────────────────────────┐
    │                                                              │
    │  DATA SECURITY                                              │
    │  ├── All data encrypted at rest and in transit               │
    │  ├── Consent-based access only (Aadhaar OTP / AA consent)   │
    │  ├── Data stored in lender-partitioned vaults                │
    │  ├── No cross-lender data sharing without explicit consent   │
    │  └── SOC 2 Type II compliant                                │
    │                                                              │
    │  REGULATORY COMPLIANCE                                      │
    │  ├── RBI Digital Lending Guidelines (Sep 2022) compliant    │
    │  ├── RBI CLA Directions (Jan 2026) for co-lending           │
    │  ├── DPDP Act 2023 consent framework built-in               │
    │  ├── PSL auto-classification and reporting                  │
    │  ├── Fair lending practices embedded in policy builder      │
    │  └── Every decision auditable with full explainability      │
    │                                                              │
    │  GOVERNANCE                                                  │
    │  ├── MCP audit logs for every AI agent interaction           │
    │  ├── Human-in-the-loop escalation for edge cases            │
    │  ├── Bias detection built into Sentinel AI                  │
    │  ├── Model governance: version control, drift detection,    │
    │  │   mandatory shadow testing before production              │
    │  └── Explainability: every reject comes with a reason        │
    │       the borrower can understand                            │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```

---

## SUMMARY: WHY LENDERS CHOOSE THIS PLATFORM

```
    ┌─────────────────────────────────────────────────────────────┐
    │                                                              │
    │  1. ACCESS          → 33 underserved segments, 300M         │
    │                       borrowers you can't reach alone       │
    │                                                              │
    │  2. INTELLIGENCE    → AI decisioning trained on the         │
    │                       richest lending dataset in India      │
    │                                                              │
    │  3. SPEED           → Launch new lending products in        │
    │                       3 days, not 3 months                  │
    │                                                              │
    │  4. COST            → INR 180/loan acquisition cost         │
    │                       vs. INR 15,000 via branch             │
    │                                                              │
    │  5. QUALITY         → Continuous monitoring prevents        │
    │                       defaults before they happen           │
    │                                                              │
    │  6. COMPLIANCE      → PSL auto-classified, audit-ready,     │
    │                       RBI-compliant by design               │
    │                                                              │
    │  7. PARTNERSHIP     → Co-lending, FLDG, embedded --         │
    │                       flexible structures for every need    │
    │                                                              │
    │  8. FUTURE-PROOF    → MCP-enabled agentic architecture     │
    │                       means every new AI capability         │
    │                       plugs in automatically                │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```
