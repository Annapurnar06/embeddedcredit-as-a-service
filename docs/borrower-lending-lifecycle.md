# Borrower Journeys, Loan Products, Lending Lifecycle & Impact Metrics

## A Complete Overview of How Credit Reaches 33 Segments and How to Measure It

---

## PART 1: THE LENDING LIFECYCLE -- END TO END

Every loan on the platform moves through 7 stages. Each stage is powered by specific products, generates specific signals, and maps to specific lender metrics.

```
    THE 7-STAGE LENDING LIFECYCLE
    ═══════════════════════════════════════════════════════════

    ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
    │    1    │──►│    2    │──►│    3    │──►│    4    │
    │DISCOVERY│   │  DATA   │   │DECISION │   │ PRODUCT │
    │& ACCESS │   │  FETCH  │   │  ING    │   │ DESIGN  │
    └─────────┘   └─────────┘   └─────────┘   └─────────┘
                                                    │
    ┌─────────┐   ┌─────────┐   ┌─────────┐        │
    │    7    │◄──│    6    │◄──│    5    │◄───────┘
    │GRADUAT- │   │MONITOR- │   │DISBURSE │
    │  ION    │   │  ING    │   │  MENT   │
    └─────────┘   └─────────┘   └─────────┘

    ┌──────────────────────────────────────────────────────┐
    │  TRADITIONAL: Stages 1-5 exist. 6 barely. 7 never.  │
    │  THIS PLATFORM: All 7. Stages 6-7 are the moat.     │
    └──────────────────────────────────────────────────────┘
```

---

### STAGE 1: DISCOVERY & ACCESS

**What happens**: The borrower encounters the lending system for the first time. This is where channel strategy determines who you can serve.

```
    ┌─────────────────────────────────────────────────────────────┐
    │  CHANNEL              SEGMENT               HOW IT WORKS    │
    │                                                              │
    │  Voice (toll-free)    Dairy farmer           Calls number,   │
    │                       SHG woman              says "mujhe     │
    │                       ASHA worker            loan chahiye"   │
    │                       Fisherman              in any of 12+   │
    │                       Migrant worker         Indian languages│
    │                       Weaver                                 │
    │                                                              │
    │  WhatsApp             Street vendor          Sends message   │
    │                       Kirana owner           or photo of     │
    │                       Beauty salon           sales register. │
    │                       Gig worker             Agent responds  │
    │                       Domestic worker        in chat.        │
    │                       Private teacher                        │
    │                                                              │
    │  App/Web (embedded)   EV buyer               Credit widget   │
    │                       Rental deposit         appears at      │
    │                       Medical patient        point of need   │
    │                       IVF borrower           in partner app/ │
    │                       Uber driver            website.        │
    │                       Upskilling student                     │
    │                                                              │
    │  Partner dashboard    FPO (group WC)         Manager submits │
    │                       Community solar        bulk request    │
    │                       Warehouse receipt      for members     │
    │                                                              │
    │  Monitoring trigger   All 33 segments        System detects  │
    │  (proactive)          (existing borrowers)   need before     │
    │                                              borrower asks   │
    └─────────────────────────────────────────────────────────────┘
```

**Products used**: Digital Onboarding, Embedded Finance SDK, Journey Studio, KYC, Superflows

**Lender metrics for this stage**:

| Metric | What It Measures | Target |
|--------|-----------------|--------|
| Reach rate | % of target segment that encounters the offer | Track by segment |
| Channel conversion | Applications started / impressions or calls | >15% voice, >8% WhatsApp, >25% embedded |
| KYC pass rate | Successful identity verification / attempts | >85% |
| Drop-off rate | Started but didn't complete application | <40% |
| Cost per lead | Total channel cost / applications received | <INR 50 |
| Language coverage | % of borrowers served in their native language | >90% |
| Time to application | From first contact to completed application | <10 min voice, <5 min WhatsApp |

---

### STAGE 2: DATA FETCH & ENRICHMENT

**What happens**: Once a borrower consents, the system fetches data from multiple sources in parallel via ULI, cross-validates, and builds a unified borrower profile.

```
    ┌─────────────────────────────────────────────────────────────┐
    │                                                              │
    │  BORROWER CONSENTS (Aadhaar OTP / AA consent)               │
    │           │                                                  │
    │           ▼                                                  │
    │  ┌───────────────────────────────────────────────┐          │
    │  │        PARALLEL ULI DATA FETCH                 │          │
    │  │                                                 │          │
    │  │  Financial:          Non-Financial:             │          │
    │  │  • Credit bureau     • Land records             │          │
    │  │  • Bank account (AA) • Cooperative data         │          │
    │  │  • GST returns       • Satellite imagery        │          │
    │  │  • ITR               • Weather data             │          │
    │  │  • EPFO              • Platform earnings        │          │
    │  │                      • ONDC order history       │          │
    │  │                      • DigiLocker docs          │          │
    │  │                      • PMFBY crop insurance     │          │
    │  │                                                 │          │
    │  │  + DeviceConnect (5,000+ behavioral features)   │          │
    │  │  + BankConnect (statement analysis + fraud)      │          │
    │  └───────────────┬───────────────────────────────┘          │
    │                  │                                            │
    │                  ▼                                            │
    │  ┌───────────────────────────────────────────────┐          │
    │  │        DATA QUALITY ENGINE                     │          │
    │  │                                                 │          │
    │  │  1. Entity resolution (match across sources)    │          │
    │  │  2. Cross-source validation (income ↔ bank)     │          │
    │  │  3. Anomaly detection (inconsistencies flagged)  │          │
    │  │  4. Freshness scoring (how recent is the data)  │          │
    │  │  5. Confidence score (0.0 - 1.0)                │          │
    │  │  6. Graceful degradation (partial data handled)  │          │
    │  └───────────────────────────────────────────────┘          │
    │                                                              │
    │  OUTPUT: Enriched, validated, confidence-scored               │
    │          borrower profile                                    │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```

**Products used**: DPI, BankConnect, DeviceConnect, Multi AA, Superflows

**Lender metrics for this stage**:

| Metric | What It Measures | Target |
|--------|-----------------|--------|
| Data fetch success rate | APIs returning valid data / APIs called | >95% |
| Avg. data sources per borrower | How many sources contribute to the profile | >3 for high-confidence |
| Data confidence score distribution | % of applications scoring HIGH / MEDIUM / LOW | >60% HIGH |
| Fetch latency (p95) | Time to complete all parallel data fetches | <3 seconds |
| Entity resolution match rate | Borrowers successfully matched across sources | >90% |
| Fraud flag rate | Applications flagged by BankConnect cluster intelligence | Track, target <5% |
| Thin-file rate | Borrowers with no/limited bureau history | Track by segment |
| DeviceConnect coverage | % of applications with device data available | >70% for app channel |

---

### STAGE 3: DECISIONING

**What happens**: Sentinel AI applies the segment-specific policy to the enriched borrower profile, generates a score, and makes an approve/reject/refer decision.

```
    ┌─────────────────────────────────────────────────────────────┐
    │                                                              │
    │  ENRICHED PROFILE ──► SENTINEL AI POLICY ENGINE             │
    │                                                              │
    │  ┌──────────────────────────────────────────────┐           │
    │  │ 1. SEGMENT DETECTION                          │           │
    │  │    Intent + data → dairy / vendor / gig / etc  │           │
    │  │                                                │           │
    │  │ 2. POLICY SELECTION                            │           │
    │  │    → DAIRY_ANIMAL_PURCHASE_v3                   │           │
    │  │    → VENDOR_DAILY_WC_v2                         │           │
    │  │    → GIG_DELIVERY_VEHICLE_v1                    │           │
    │  │                                                │           │
    │  │ 3. SCORING                                     │           │
    │  │    Segment-specific model applies weights       │           │
    │  │    to data features. Outputs: score + grade.    │           │
    │  │                                                │           │
    │  │ 4. FRAUD CHECK                                 │           │
    │  │    BankConnect cluster intelligence +            │           │
    │  │    cross-application velocity +                  │           │
    │  │    identity inconsistency detection              │           │
    │  │                                                │           │
    │  │ 5. DECISION                                    │           │
    │  │    APPROVE → continue to product design         │           │
    │  │    REJECT  → with explainable reason             │           │
    │  │    REFER   → to human review queue               │           │
    │  │                                                │           │
    │  │ 6. RISK-BASED PRICING                          │           │
    │  │    Score → rate band                            │           │
    │  │    Higher score = lower rate for borrower       │           │
    │  └──────────────────────────────────────────────┘           │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```

**Products used**: Sentinel AI, RiskEngine, MCP Protocol

**Lender metrics for this stage**:

| Metric | What It Measures | Target |
|--------|-----------------|--------|
| Approval rate | Approved / total applications | Track by segment (30-60%) |
| Auto-approval rate | Approved without human review / total | >80% of approvals |
| Decision latency | Time from data ready to decision | <15 seconds |
| Rejection explainability | % of rejections with clear reason codes | 100% |
| Fraud detection rate | Fraudulent applications caught / total fraud | >95% |
| False positive rate | Legitimate borrowers flagged as fraud | <2% |
| Score distribution (Gini) | Discriminatory power of scoring model | >0.65 |
| Score distribution (KS) | Separation between goods and bads | >0.40 |
| Refer-to-human rate | Applications needing manual review | <15% |
| Override rate | Manual decisions overriding AI recommendation | Track (target <5%) |
| Rate spread | Range of risk-based pricing across approvals | 12-24% across segments |

---

### STAGE 4: DYNAMIC PRODUCT DESIGN

**What happens**: For approved borrowers, the system doesn't select a product from a static catalogue. It designs one -- amount, rate, tenure, schedule type, insurance, and embedded protections -- tailored to this specific borrower.

```
    ┌─────────────────────────────────────────────────────────────┐
    │  8 PRODUCT TYPES × 33 SEGMENTS = INFINITE COMBINATIONS     │
    │                                                              │
    │  ┌──────────────────────────────────────────────────────┐  │
    │  │                                                       │  │
    │  │  PRODUCT TYPE         SCHEDULE             SEGMENTS   │  │
    │  │  ═══════════          ════════             ════════   │  │
    │  │                                                       │  │
    │  │  1. Seasonal          Flush: high EMI      Dairy      │  │
    │  │     Dynamic           Lean: low EMI        Crop       │  │
    │  │                       Transition: medium   Fisherman  │  │
    │  │                                            Mango      │  │
    │  │                                                       │  │
    │  │  2. Daily Micro       INR 100-300/day      Vendor     │  │
    │  │                       auto-deducted from   Gig worker │  │
    │  │                       UPI collections or   Auto-rick  │  │
    │  │                       platform payouts     Salon      │  │
    │  │                                                       │  │
    │  │  3. Catch/Sale-       Repay when sale      Fisherman  │  │
    │  │     Linked            event detected       Warehouse  │  │
    │  │                       by ULI data          Weaver     │  │
    │  │                                            Mandi      │  │
    │  │                                                       │  │
    │  │  4. Income-           % of verified        ITI grad   │  │
    │  │     Contingent        post-course income   Upskilling │  │
    │  │     (ISA-like)        via EPFO detection    │  │
    │  │                                                       │  │
    │  │  5. Moratorium-       Auto-pause when      Monsoon    │  │
    │  │     with-Trigger      trigger fires:       Heat wave  │  │
    │  │                       weather, health,     Medical    │  │
    │  │                       platform shutdown    recovery   │  │
    │  │                                                       │  │
    │  │  6. Bridge            Zero-interest,       ASHA (DBT) │  │
    │  │     (Zero-Interest)   auto-repay when      Death      │  │
    │  │                       expected payment     Maternity  │  │
    │  │                       arrives              │  │
    │  │                                                       │  │
    │  │  7. Staged            Disbursed in         Home build │  │
    │  │     Disbursement      milestone-linked     Medical    │  │
    │  │                       tranches             IVF        │  │
    │  │                                            Construct. │  │
    │  │                                                       │  │
    │  │  8. Payout-           Auto-deduct from     Meesho     │  │
    │  │     Linked            platform payouts     ONDC merch │  │
    │  │                       at source            Gig worker │  │
    │  │                                            Uber/Ola   │  │
    │  └──────────────────────────────────────────────────────┘  │
    │                                                              │
    │  EACH PRODUCT ALSO INCLUDES:                                │
    │  ├── Insurance layer (crop/animal/health where applicable)  │
    │  ├── Auto-moratorium triggers (weather, health, platform)   │
    │  ├── Graduation pathway (clear criteria for next tier)      │
    │  └── Emergency micro-loan eligibility (for distress events) │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```

**Products used**: Sentinel AI (policy engine), Dynamic Product Engine (Layer 4), Journey Studio

**Lender metrics for this stage**:

| Metric | What It Measures | Target |
|--------|-----------------|--------|
| Product-market fit | Borrower acceptance rate of designed offer | >70% |
| Avg. ticket size | Mean loan amount per segment | Track by segment |
| Rate distribution | Spread of risk-based pricing across approvals | Within lender-approved bands |
| Schedule type distribution | Mix of seasonal/daily/payout-linked etc. | Track alignment with segment |
| Insurance attach rate | % of loans with insurance layer | >80% where applicable |
| Time from approval to offer | Latency of product design step | <5 seconds |

---

### STAGE 5: DISBURSEMENT

**What happens**: The borrower accepts the offer, e-signs, and funds are disbursed -- typically via UPI, directly to borrower or to vendor/dealer for asset purchases.

```
    ┌─────────────────────────────────────────────────────────────┐
    │                                                              │
    │  BORROWER ACCEPTS OFFER                                     │
    │         │                                                    │
    │         ▼                                                    │
    │  ┌──────────────────────────────────────────────┐           │
    │  │ e-Sign via Aadhaar (voice OTP for voice      │           │
    │  │ channel, screen OTP for app/WhatsApp)         │           │
    │  └──────────┬───────────────────────────────────┘           │
    │             │                                                │
    │             ▼                                                │
    │  ┌──────────────────────────────────────────────┐           │
    │  │ LOS processes:                                │           │
    │  │  1. Final compliance check                    │           │
    │  │  2. Lender-specific approval (if required)    │           │
    │  │  3. Insurance enrollment                      │           │
    │  │  4. Disbursement instruction                  │           │
    │  └──────────┬───────────────────────────────────┘           │
    │             │                                                │
    │             ▼                                                │
    │  ┌──────────────────────────────────────────────┐           │
    │  │ DISBURSEMENT OPTIONS:                         │           │
    │  │                                                │           │
    │  │  Direct to borrower   → UPI to bank account   │           │
    │  │  Direct to vendor     → UPI to dealer/seller  │           │
    │  │                         (EV, equipment, cart)  │           │
    │  │  Staged               → First tranche now,    │           │
    │  │                         rest on milestones     │           │
    │  │  To partner/FPO       → Bulk to group account  │           │
    │  │  To hospital/school   → Direct to institution  │           │
    │  └──────────────────────────────────────────────┘           │
    │                                                              │
    │  CONFIRMATION: Borrower receives SMS/WhatsApp/voice          │
    │  confirmation with loan details and repayment schedule       │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```

**Products used**: LOS, Digital Onboarding, KYC

**Lender metrics for this stage**:

| Metric | What It Measures | Target |
|--------|-----------------|--------|
| Disbursement TAT | Approval to money-in-account | <30 min (voice), <10 min (digital) |
| e-Sign completion rate | Successful e-sign / attempts | >95% |
| Disbursement success rate | Successful transfers / attempted | >99% |
| First-day confirmation | Borrower acknowledged receipt | >95% |
| Insurance enrollment rate | Successfully enrolled / required | >90% |
| Avg. end-to-end TAT | First contact to disbursement | <15 min (WhatsApp), <30 min (voice) |

---

### STAGE 6: POST-DISBURSEMENT MONITORING (The Differentiator)

**What happens**: This is where the platform fundamentally differs from traditional lending. Instead of waiting for EMI due dates and reacting to missed payments, the monitoring agent continuously watches ULI data streams and proactively intervenes.

```
    ┌─────────────────────────────────────────────────────────────┐
    │           THE MONITORING AGENT (Always-On)                   │
    │                                                              │
    │  DATA STREAMS WATCHED:                                      │
    │  ├── Cooperative records (production changes)                │
    │  ├── Bank account (AA) (income pattern shifts)              │
    │  ├── Weather/satellite (environmental events)               │
    │  ├── Platform APIs (gig earnings, order volume)             │
    │  ├── EPFO (employment status changes)                       │
    │  ├── GST (business volume trends)                           │
    │  └── BankConnect (spending/savings pattern changes)          │
    │                                                              │
    │  TRIGGERS AND RESPONSES:                                    │
    │                                                              │
    │  ┌──────────────────────────────────────────────────────┐  │
    │  │ TRIGGER: Production drop >30%                         │  │
    │  │ (e.g., milk pouring drop, catch volume drop)          │  │
    │  │                                                       │  │
    │  │ RESPONSE:                                             │  │
    │  │  1. Flag for early warning                            │  │
    │  │  2. Call borrower: "Is everything ok?"                │  │
    │  │  3. Offer schedule adjustment (reduce EMI)            │  │
    │  │  4. If asset-related: offer emergency micro-loan      │  │
    │  │  5. If insured: initiate claim pre-processing         │  │
    │  └──────────────────────────────────────────────────────┘  │
    │                                                              │
    │  ┌──────────────────────────────────────────────────────┐  │
    │  │ TRIGGER: Weather event in borrower's pincode          │  │
    │  │ (heat wave, flood, drought, cyclone approaching)      │  │
    │  │                                                       │  │
    │  │ RESPONSE:                                             │  │
    │  │  1. Auto-activate moratorium for affected borrowers   │  │
    │  │  2. Proactive call: "Aapka payment adjust kiya gaya"  │  │
    │  │  3. Recalculate remaining schedule                    │  │
    │  │  4. No late fees, no NPA classification during pause  │  │
    │  └──────────────────────────────────────────────────────┘  │
    │                                                              │
    │  ┌──────────────────────────────────────────────────────┐  │
    │  │ TRIGGER: Income increase detected                     │  │
    │  │ (higher platform earnings, new EPFO contribution)     │  │
    │  │                                                       │  │
    │  │ RESPONSE:                                             │  │
    │  │  1. Offer early repayment option (with rate benefit)  │  │
    │  │  2. Pre-approve for larger next loan (graduation)     │  │
    │  │  3. Update credit profile positively                  │  │
    │  └──────────────────────────────────────────────────────┘  │
    │                                                              │
    │  ┌──────────────────────────────────────────────────────┐  │
    │  │ TRIGGER: Payment missed (DPD 1+)                      │  │
    │  │                                                       │  │
    │  │ RESPONSE (NOT traditional collections):               │  │
    │  │  1. Check ULI data: WHY was it missed?                │  │
    │  │     - Income drop? → Adjust schedule                  │  │
    │  │     - Environmental event? → Auto-moratorium          │  │
    │  │     - Platform issue? → Wait for resolution           │  │
    │  │     - No clear reason? → Gentle reminder call         │  │
    │  │  2. Only escalate to collections after context-aware  │  │
    │  │     intervention fails                                │  │
    │  └──────────────────────────────────────────────────────┘  │
    │                                                              │
    │  ┌──────────────────────────────────────────────────────┐  │
    │  │ TRIGGER: Positive repayment streak (6+ months clean)  │  │
    │  │                                                       │  │
    │  │ RESPONSE:                                             │  │
    │  │  1. Credit score update (shadow → formal)             │  │
    │  │  2. Rate reduction offer                              │  │
    │  │  3. Graduation: pre-approved for 2x amount at lower   │  │
    │  │     rate                                              │  │
    │  │  4. Cross-sell: insurance, savings linkage            │  │
    │  └──────────────────────────────────────────────────────┘  │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```

**Products used**: Sentinel AI (360-degree monitoring), BankConnect, DPI (continuous ULI data), MCP Protocol

**Lender metrics for this stage**:

| Metric | What It Measures | Target |
|--------|-----------------|--------|
| 0 DPD rate | % of portfolio with no payment delays | >88% |
| 30+ DPD rate | Early delinquency | <6% |
| 90+ DPD rate | Serious delinquency (approaching NPA) | <2.5% |
| NPA rate | Non-performing assets (90+ DPD) | <2% (vs. 5-8% industry) |
| Proactive intervention rate | Interventions triggered BEFORE missed payment | >60% of all interventions |
| Intervention success rate | Defaults prevented / interventions attempted | >70% |
| Moratorium utilization | % of borrowers using weather/event moratorium | Track by segment |
| Moratorium cure rate | % of moratorium borrowers who resume full payment | >90% |
| Emergency micro-loan uptake | Distress micro-loans issued / distress events | Track |
| Insurance claim success rate | Claims processed / claims filed | >85% |
| Avg. DPD before intervention | How early does the system act | <5 days (target: before DPD) |
| Collection cost per loan | Total collections spend / active loans | <INR 200 (vs. INR 2,000+ traditional) |

---

### STAGE 7: GRADUATION & CREDIT BUILDING

**What happens**: The ultimate goal is not just loan repayment -- it is building the borrower's credit identity and graduating them to larger, cheaper, more formal credit products.

```
    ┌─────────────────────────────────────────────────────────────┐
    │           GRADUATION PATHWAYS                                │
    │                                                              │
    │  TIER 1 → TIER 2 → TIER 3 → FORMAL BANKING                │
    │                                                              │
    │  ┌──────────────┐                                           │
    │  │ TIER 1       │  First loan. Smaller amount.              │
    │  │ First Credit  │  Higher rate. More data needed.           │
    │  │              │  Shadow credit file created.              │
    │  │  INR 10-50K  │  Monitored intensively.                   │
    │  │  Rate: 18-24% │                                           │
    │  └──────┬───────┘                                           │
    │         │ After successful repayment (6-15 months):         │
    │         │ ✓ Credit score established (shadow → formal)      │
    │         │ ✓ Repayment behavior verified                     │
    │         │ ✓ Income pattern confirmed over full cycle        │
    │         ▼                                                    │
    │  ┌──────────────┐                                           │
    │  │ TIER 2       │  Larger amount. Lower rate.               │
    │  │ Graduated    │  Fewer data sources needed (track         │
    │  │              │  record replaces thin-file workaround).   │
    │  │  INR 50K-2L  │  Monitoring less intensive.               │
    │  │  Rate: 14-18% │  Auto-moratorium and emergency           │
    │  │              │  features retained.                       │
    │  └──────┬───────┘                                           │
    │         │ After successful repayment (12-18 months):        │
    │         │ ✓ Bureau score now meaningful (2+ trade lines)    │
    │         │ ✓ Bank willing to co-lend at lower rate           │
    │         │ ✓ More product types available (home, education)  │
    │         ▼                                                    │
    │  ┌──────────────┐                                           │
    │  │ TIER 3       │  Near-formal credit. Bank rates.          │
    │  │ Established  │  Full bureau history. Co-lending           │
    │  │              │  structures with PSBs.                    │
    │  │  INR 2-10L   │  Monitoring agent = light touch.          │
    │  │  Rate: 10-14% │  Graduation to mainstream banking        │
    │  │              │  possible (savings account, insurance).   │
    │  └──────┬───────┘                                           │
    │         │                                                    │
    │         ▼                                                    │
    │  ┌──────────────┐                                           │
    │  │ FORMAL       │  The borrower now has a credit            │
    │  │ BANKING      │  identity that any bank recognizes.       │
    │  │              │  They can walk into a branch and          │
    │  │              │  get a loan based on bureau history.      │
    │  │              │  The platform created a customer          │
    │  │              │  that the formal system can serve.        │
    │  └──────────────┘                                           │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```

**Lender metrics for this stage**:

| Metric | What It Measures | Target |
|--------|-----------------|--------|
| Graduation rate | Borrowers moving to Tier 2+ / Tier 1 completed | >50% within 18 months |
| Repeat borrowing rate | Borrowers taking second loan / first loan completed | >60% |
| Rate improvement | Avg. rate reduction from Tier 1 to Tier 2 | >3 percentage points |
| Ticket size growth | Avg. amount increase from Tier 1 to Tier 2 | >2x |
| Bureau score creation rate | Borrowers gaining formal bureau score / total | >80% after first loan |
| Bureau score improvement | Avg. score increase after successful repayment | >30 points |
| Cross-sell conversion | Insurance/savings/investment product uptake | Track |
| Borrower lifetime value | Total revenue per borrower across all tiers | Track by segment |
| Time to graduation | Months from Tier 1 to Tier 2 entry | <18 months |

---

## PART 2: BORROWER JOURNEY MAPS -- SEGMENT BY SEGMENT

### Journey Map Template

Each segment journey follows the same 7-stage lifecycle but with segment-specific data sources, scoring models, product types, and monitoring triggers.

```
    ┌──────────────────────────────────────────────────────────────────────────────────────────────┐
    │                                    SEGMENT JOURNEY MAP                                       │
    │                                                                                              │
    │  Segment        │ Channel    │ Data Sources      │ Score Model    │ Product Type   │ Monitor │
    │  ═══════════════╪════════════╪═══════════════════╪════════════════╪════════════════╪═════════│
    │                 │            │                    │                │                │         │
    │  Dairy farmer   │ Voice      │ Cooperative,       │ DairyScore     │ Seasonal       │ Coop    │
    │                 │            │ land, satellite,   │ (pouring,      │ dynamic        │ pouring,│
    │                 │            │ bureau, bank (AA)  │ tenure, land,  │                │ weather,│
    │                 │            │                    │ bureau, bank)  │                │ bank    │
    │                 │            │                    │                │                │         │
    │  Street vendor  │ WhatsApp   │ UPI transactions,  │ VendorScore    │ Daily micro    │ UPI     │
    │                 │            │ DeviceConnect,     │ (daily txn,    │                │ daily   │
    │                 │            │ bureau (thin),     │ consistency,   │                │ collect,│
    │                 │            │ bank (AA)          │ device, bank)  │                │ bank    │
    │                 │            │                    │                │                │         │
    │  Gig worker     │ WhatsApp/  │ Platform API,      │ GigScore       │ Payout-linked  │ Platform│
    │  (delivery)     │ App        │ DeviceConnect,     │ (deliveries,   │ or daily micro │ API,    │
    │                 │            │ bureau, bank (AA)  │ rating, multi- │                │ earnings│
    │                 │            │                    │ platform, bank)│                │ trend   │
    │                 │            │                    │                │                │         │
    │  ASHA worker    │ Voice      │ DBT records,       │ DBTScore       │ Bridge         │ DBT     │
    │                 │            │ bureau, bank (AA)  │ (DBT regular,  │ (zero-interest)│ credit  │
    │                 │            │                    │ tenure, bank)  │                │ timing  │
    │                 │            │                    │                │                │         │
    │  SHG woman      │ Voice      │ SHG records,       │ SHGScore       │ Seasonal       │ Meeting │
    │                 │            │ meeting logs,      │ (attendance,   │ dynamic or     │ attend, │
    │                 │            │ cooperative,       │ savings, group │ daily micro    │ savings │
    │                 │            │ bureau, bank (AA)  │ performance)   │                │ pattern │
    │                 │            │                    │                │                │         │
    │  Fisherman      │ Voice      │ Fish catch logs,   │ FisherScore    │ Catch-linked + │ Catch   │
    │                 │            │ vessel GPS,        │ (catch volume, │ moratorium     │ volume, │
    │                 │            │ weather, bureau,   │ regularity,    │ (monsoon ban)  │ weather,│
    │                 │            │ bank (AA)          │ vessel, bank)  │                │ ban     │
    │                 │            │                    │                │                │ dates   │
    │                 │            │                    │                │                │         │
    │  Kirana (ONDC)  │ WhatsApp/  │ ONDC orders,       │ MerchantScore  │ Payout-linked  │ Order   │
    │                 │ Embedded   │ GST, bank (AA),    │ (order freq,   │                │ volume, │
    │                 │            │ DeviceConnect      │ GMV, GST,      │                │ GST     │
    │                 │            │                    │ return rate)   │                │ filings │
    │                 │            │                    │                │                │         │
    │  EV buyer       │ App/Web    │ Bureau, bank (AA), │ Standard +     │ EMI (asset-    │ Bank,   │
    │                 │ (embedded) │ DeviceConnect,     │ AssetScore     │ backed)        │ device  │
    │                 │            │ employment/gig     │ (income, asset │                │ usage   │
    │                 │            │                    │ value, bureau) │                │ pattern │
    │                 │            │                    │                │                │         │
    │  ITI student    │ App/Web    │ Course enrollment, │ SkillScore     │ Income-        │ EPFO,   │
    │                 │            │ EPFO (post-course),│ (institution,  │ contingent     │ employ- │
    │                 │            │ bureau, bank (AA)  │ course ROI,    │ (ISA-like)     │ ment    │
    │                 │            │                    │ placement rate)│                │ detect  │
    │                 │            │                    │                │                │         │
    │  Medical patient│ App/Web    │ Hospital estimate, │ MedScore       │ Staged         │ Treat-  │
    │                 │            │ insurance,         │ (procedure,    │ disbursement + │ ment    │
    │                 │            │ bureau, bank (AA), │ recovery time, │ moratorium     │ milesto-│
    │                 │            │ employment         │ income, ins)   │                │ nes     │
    │                 │            │                    │                │                │         │
    │  FPO (group)    │ Partner    │ Member records,    │ FPOScore       │ Seasonal WC    │ Aggreg- │
    │                 │ dashboard  │ aggregation data,  │ (member count, │ (group)        │ ation   │
    │                 │            │ mandi prices,      │ aggregation,   │                │ volumes,│
    │                 │            │ warehouse, bank    │ grade history) │                │ mandi   │
    │                 │            │                    │                │                │ prices  │
    │                 │            │                    │                │                │         │
    │  Domestic worker│ WhatsApp   │ UPI payments (from │ IncomeScore    │ Daily micro    │ Payment │
    │                 │            │ employers), bank   │ (multi-source, │ or monthly     │ pattern │
    │                 │            │ (AA), DeviceConnect│ tenure, device)│                │ from    │
    │                 │            │                    │                │                │ employ- │
    │                 │            │                    │                │                │ ers     │
    │                 │            │                    │                │                │         │
    └──────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## PART 3: LENDER ORGANIZATION METRICS -- THE IMPACT EVALUATION FRAMEWORK

### Tier 1: Portfolio Performance Metrics

These are the metrics that directly measure whether the lending platform is performing.

```
    ┌─────────────────────────────────────────────────────────────────────┐
    │  PORTFOLIO PERFORMANCE SCORECARD                                     │
    │                                                                      │
    │  ┌────────────────────┬──────────────┬────────────┬───────────────┐ │
    │  │ METRIC             │ TRADITIONAL  │ PLATFORM   │ IMPROVEMENT   │ │
    │  │                    │ BENCHMARK    │ TARGET     │               │ │
    │  ├────────────────────┼──────────────┼────────────┼───────────────┤ │
    │  │ Approval rate      │ 15-25%       │ 35-55%     │ +20pp         │ │
    │  │ (thin-file)        │ (bureau-only)│ (ULI data) │ more served   │ │
    │  ├────────────────────┼──────────────┼────────────┼───────────────┤ │
    │  │ NPA rate           │ 5-8%         │ 1.5-3%     │ 50-70% lower  │ │
    │  │ (underserved)      │ (static UW)  │ (dynamic)  │ defaults      │ │
    │  ├────────────────────┼──────────────┼────────────┼───────────────┤ │
    │  │ Collection         │ INR 2,000+   │ INR 150-300│ 85-90%        │ │
    │  │ cost / loan        │ (manual)     │ (AI agent) │ cost reduction│ │
    │  ├────────────────────┼──────────────┼────────────┼───────────────┤ │
    │  │ Origination        │ INR 10-15K   │ INR 100-300│ 95-98%        │ │
    │  │ cost / loan        │ (branch)     │ (agent)    │ cost reduction│ │
    │  ├────────────────────┼──────────────┼────────────┼───────────────┤ │
    │  │ End-to-end TAT     │ 5-15 days    │ 7-30 min   │ 99%+ faster   │ │
    │  │                    │ (branch)     │ (agent)    │               │ │
    │  ├────────────────────┼──────────────┼────────────┼───────────────┤ │
    │  │ 0 DPD rate         │ 78-85%       │ 88-93%     │ +8-10pp       │ │
    │  │                    │              │            │ improvement   │ │
    │  ├────────────────────┼──────────────┼────────────┼───────────────┤ │
    │  │ Borrower repeat    │ 20-30%       │ 55-70%     │ 2-3x higher   │ │
    │  │ rate               │              │            │ retention     │ │
    │  └────────────────────┴──────────────┴────────────┴───────────────┘ │
    │                                                                      │
    └─────────────────────────────────────────────────────────────────────┘
```

---

### Tier 2: Business Impact Metrics

These measure how the platform changes the lender's business outcomes.

```
    ┌─────────────────────────────────────────────────────────────────────┐
    │  BUSINESS IMPACT SCORECARD                                           │
    │                                                                      │
    │  ┌──────────────────────────────────────────────────────────────┐   │
    │  │ REVENUE IMPACT                                                │   │
    │  │                                                                │   │
    │  │ New addressable market opened:                                │   │
    │  │   INR ______ Cr (loans to segments previously unserved)       │   │
    │  │                                                                │   │
    │  │ Incremental interest income:                                   │   │
    │  │   INR ______ Cr / year (from new portfolio)                   │   │
    │  │                                                                │   │
    │  │ Processing fee income:                                        │   │
    │  │   INR ______ Cr / year (upfront fees)                         │   │
    │  │                                                                │   │
    │  │ Insurance commission:                                         │   │
    │  │   INR ______ Cr / year (from attached insurance)              │   │
    │  │                                                                │   │
    │  │ Co-lending income (for bank):                                 │   │
    │  │   INR ______ Cr / year (interest spread on capital provided)  │   │
    │  └──────────────────────────────────────────────────────────────┘   │
    │                                                                      │
    │  ┌──────────────────────────────────────────────────────────────┐   │
    │  │ COST IMPACT                                                   │   │
    │  │                                                                │   │
    │  │ Branch cost avoided:                                          │   │
    │  │   INR ______ Cr / year (no new branches needed)               │   │
    │  │                                                                │   │
    │  │ Origination cost saved:                                       │   │
    │  │   INR ______ per loan × ______ loans = INR ______ Cr         │   │
    │  │   (INR 15,000 branch → INR 200 agent)                        │   │
    │  │                                                                │   │
    │  │ Collections cost saved:                                       │   │
    │  │   INR ______ per loan × ______ loans = INR ______ Cr         │   │
    │  │   (INR 2,000 manual → INR 200 AI agent)                      │   │
    │  │                                                                │   │
    │  │ Technology cost avoided:                                      │   │
    │  │   INR ______ Cr / year (no custom ULI integration needed)     │   │
    │  │                                                                │   │
    │  │ Compliance cost saved:                                        │   │
    │  │   INR ______ Cr / year (auto-generated PSL reports,           │   │
    │  │   audit trails, explainability)                                │   │
    │  └──────────────────────────────────────────────────────────────┘   │
    │                                                                      │
    │  ┌──────────────────────────────────────────────────────────────┐   │
    │  │ RISK IMPACT                                                   │   │
    │  │                                                                │   │
    │  │ NPA reduction:                                                │   │
    │  │   From ____% to ____% = INR ______ Cr less provisioning      │   │
    │  │                                                                │   │
    │  │ Proactive intervention value:                                 │   │
    │  │   ______ defaults prevented × avg. ticket = INR ______ Cr    │   │
    │  │   in losses avoided                                           │   │
    │  │                                                                │   │
    │  │ PSL shortfall penalty avoided:                                │   │
    │  │   INR ______ Cr (penalty on unmet PSL targets)                │   │
    │  │                                                                │   │
    │  │ Fraud prevented:                                              │   │
    │  │   ______ fraudulent applications caught = INR ______ Cr      │   │
    │  │   in losses avoided                                           │   │
    │  └──────────────────────────────────────────────────────────────┘   │
    │                                                                      │
    └─────────────────────────────────────────────────────────────────────┘
```

---

### Tier 3: Strategic Metrics

These measure whether the platform is building durable competitive advantages.

```
    ┌─────────────────────────────────────────────────────────────────────┐
    │  STRATEGIC SCORECARD                                                 │
    │                                                                      │
    │  ┌──────────────────────────────────────────────────────────────┐   │
    │  │ MODEL INTELLIGENCE                                            │   │
    │  │                                                                │   │
    │  │ Scoring model Gini improvement (quarterly):                   │   │
    │  │   Baseline: ____  Current: ____  Trend: ↑/↓                  │   │
    │  │                                                                │   │
    │  │ RL loop contribution:                                         │   │
    │  │   ______ verifiable signals processed this quarter            │   │
    │  │   Model updates triggered: ______                             │   │
    │  │   Policy refinements deployed: ______                         │   │
    │  │                                                                │   │
    │  │ Prediction accuracy:                                          │   │
    │  │   Weather-moratorium trigger accuracy: ____%                  │   │
    │  │   Income change prediction accuracy: ____%                    │   │
    │  │   Default prediction accuracy (6-mo forward): ____%          │   │
    │  └──────────────────────────────────────────────────────────────┘   │
    │                                                                      │
    │  ┌──────────────────────────────────────────────────────────────┐   │
    │  │ NETWORK EFFECTS                                               │   │
    │  │                                                                │   │
    │  │ Lenders on platform:     ______ (target: 50+ by Month 24)    │   │
    │  │ Segments live:           ______ / 33                          │   │
    │  │ Languages live:          ______ / 12+                         │   │
    │  │ Geographic coverage:     ______ pincodes                      │   │
    │  │ Cumulative loans:        ______ (context moat metric)        │   │
    │  │ Unique borrowers:        ______                               │   │
    │  │ Bureau scores created:   ______ (new-to-credit served)       │   │
    │  └──────────────────────────────────────────────────────────────┘   │
    │                                                                      │
    │  ┌──────────────────────────────────────────────────────────────┐   │
    │  │ FINANCIAL INCLUSION IMPACT                                    │   │
    │  │                                                                │   │
    │  │ First-time formal credit borrowers:       ______             │   │
    │  │ Women borrowers:                          ______  (___%)     │   │
    │  │ Rural borrowers (Tier 3-6 cities):        ______  (___%)     │   │
    │  │ Borrowers below MFI income threshold:     ______  (___%)     │   │
    │  │ Borrowers graduated to Tier 2+:           ______  (___%)     │   │
    │  │ Avg. interest rate reduction T1 → T2:     ____ pp            │   │
    │  │ Avg. ticket size growth T1 → T2:          ____x              │   │
    │  │ Borrowers with formal bureau score (new): ______             │   │
    │  │                                                                │   │
    │  │ FINANCIAL INCLUSION INDEX (composite):                        │   │
    │  │ = 0.3 × (first-time borrowers / target)                      │   │
    │  │ + 0.2 × (graduation rate)                                     │   │
    │  │ + 0.2 × (women borrower %)                                    │   │
    │  │ + 0.15 × (rural %)                                            │   │
    │  │ + 0.15 × (NPA reduction vs. benchmark)                        │   │
    │  │                                                                │   │
    │  │ Target: >0.70 by Month 12, >0.85 by Month 24                 │   │
    │  └──────────────────────────────────────────────────────────────┘   │
    │                                                                      │
    └─────────────────────────────────────────────────────────────────────┘
```

---

### Tier 4: Operational Efficiency Metrics

These measure how well the platform itself is operating.

```
    ┌─────────────────────────────────────────────────────────────────────┐
    │  OPERATIONAL SCORECARD                                               │
    │                                                                      │
    │  SYSTEM PERFORMANCE                                                 │
    │  ├── API uptime:                    ___% (target: >99.9%)           │
    │  ├── Avg. decision latency (p50):   ____ seconds (target: <5s)     │
    │  ├── Avg. decision latency (p95):   ____ seconds (target: <15s)    │
    │  ├── Data fetch success rate:       ___% (target: >95%)            │
    │  ├── Disbursement success rate:     ___% (target: >99%)            │
    │  └── MCP call success rate:         ___% (target: >99.5%)          │
    │                                                                      │
    │  AGENT PERFORMANCE                                                  │
    │  ├── Voice agent call completion:   ___% (target: >85%)            │
    │  ├── WhatsApp journey completion:   ___% (target: >75%)            │
    │  ├── Avg. conversation turns to complete application: ____ (↓)     │
    │  ├── Language detection accuracy:   ___% (target: >95%)            │
    │  ├── Intent classification accuracy: ___% (target: >90%)           │
    │  ├── Human escalation rate:         ___% (target: <10%)            │
    │  └── Borrower satisfaction (NPS):   ____ (target: >50)             │
    │                                                                      │
    │  MONITORING AGENT PERFORMANCE                                       │
    │  ├── Active loans being monitored:  ______ / ______ total          │
    │  ├── ULI data streams active:       ______ / ______ expected       │
    │  ├── Avg. time to detect distress:  ____ hours (target: <24h)      │
    │  ├── Avg. time to intervene:        ____ hours after detection     │
    │  ├── False alarm rate:              ___% (target: <15%)            │
    │  └── Borrower responsiveness:       ___% answer calls/messages     │
    │                                                                      │
    │  JOURNEY STUDIO METRICS                                             │
    │  ├── Avg. journey creation time:    ____ days (target: <5)         │
    │  ├── A/B tests running:             ______                          │
    │  ├── Avg. conversion lift from A/B: ____%                          │
    │  └── Journeys live:                 ______ across ______ segments  │
    │                                                                      │
    └─────────────────────────────────────────────────────────────────────┘
```

---

## PART 4: THE COMPLETE IMPACT MAP

### How Every Layer Connects to Every Metric

```
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                      │
    │  LAYER          DRIVES THESE                MEASURED BY              │
    │  ═════          ════════════                ═══════════              │
    │                                                                      │
    │  L5: Borrower   Access & reach              Reach rate, channel      │
    │  Agents         Channel coverage            conversion, language     │
    │                 Inclusion                    coverage, TAT, NPS,     │
    │                                             cost per lead            │
    │                                                                      │
    │  L4: Segment    Scoring accuracy            Gini, KS, approval      │
    │  Intelligence   Product-market fit          rate, thin-file          │
    │                 Addressable market           conversion, acceptance  │
    │                 expansion                    rate, fraud detection   │
    │                                                                      │
    │  L3: AI         Decision quality            NPA rate, auto-approval │
    │  Decisioning    Speed                       rate, decision latency, │
    │  Core           Compliance                  override rate, model    │
    │                 Risk-based pricing           drift, audit quality    │
    │                                                                      │
    │  L2: ULI Data   Data richness               Sources per borrower,   │
    │  Orchestration  Data quality                 confidence score,       │
    │                 Coverage                     fetch latency, entity   │
    │                                             resolution rate         │
    │                                                                      │
    │  L1: Verifiable Model improvement           Gini trend, prediction  │
    │  Environment    Competitive moat            accuracy, RL signal     │
    │                 Network intelligence         volume, cumulative      │
    │                                             loans, model updates    │
    │                                                                      │
    │  LIFECYCLE      Lifecycle efficiency         0 DPD, NPA, collection │
    │  STAGES         Borrower outcomes            cost, graduation rate, │
    │  (1-7)          Unit economics               origination cost, ROA, │
    │                                             inclusion index, LTV    │
    │                                                                      │
    └─────────────────────────────────────────────────────────────────────┘
```

---

## PART 5: LENDER EVALUATION DASHBOARD -- SINGLE PAGE VIEW

```
    ┌─────────────────────────────────────────────────────────────────────┐
    │                    LENDER IMPACT DASHBOARD                           │
    │                    Period: ____________                              │
    │                                                                      │
    │  ┌─────────────────────┐  ┌─────────────────────┐                  │
    │  │ PORTFOLIO SUMMARY    │  │ UNIT ECONOMICS       │                  │
    │  │                     │  │                      │                  │
    │  │ Active loans: _____ │  │ Origination cost:    │                  │
    │  │ AUM: INR ___ Cr     │  │   INR ___/loan       │                  │
    │  │ Segments live: __/33│  │ Collection cost:     │                  │
    │  │ Languages: __/12+   │  │   INR ___/loan       │                  │
    │  │ Avg. ticket: INR ___│  │ Blended yield: ___%  │                  │
    │  │                     │  │ Credit cost:   ___%  │                  │
    │  │                     │  │ Net margin:    ___%  │                  │
    │  │                     │  │ ROA:           ___%  │                  │
    │  └─────────────────────┘  └─────────────────────┘                  │
    │                                                                      │
    │  ┌─────────────────────┐  ┌─────────────────────┐                  │
    │  │ ASSET QUALITY        │  │ COMPLIANCE           │                  │
    │  │                     │  │                      │                  │
    │  │ 0 DPD:       ___%  │  │ PSL Agri:   __/__ Cr│                  │
    │  │ 30+ DPD:     ___%  │  │ PSL MSME:   __/__ Cr│                  │
    │  │ 90+ DPD:     ___%  │  │ PSL Weaker: __/__ Cr│                  │
    │  │ NPA rate:    ___%  │  │ CLA compliant: Y/N  │                  │
    │  │ vs. industry: +/-  │  │ DPDP compliant: Y/N │                  │
    │  │                     │  │ Audit ready: Y/N     │                  │
    │  └─────────────────────┘  └─────────────────────┘                  │
    │                                                                      │
    │  ┌─────────────────────┐  ┌─────────────────────┐                  │
    │  │ MONITORING IMPACT    │  │ INCLUSION IMPACT     │                  │
    │  │                     │  │                      │                  │
    │  │ Proactive interv:   │  │ First-time credit:   │                  │
    │  │   ____ this month   │  │   _______ borrowers  │                  │
    │  │ Defaults prevented: │  │ Women: ____% of book │                  │
    │  │   ____  (__% of     │  │ Rural: ____% of book │                  │
    │  │   interventions)    │  │ Bureau scores created:│                  │
    │  │ Moratoria active:   │  │   _______             │                  │
    │  │   ____              │  │ Graduated to Tier 2+: │                  │
    │  │ Emergency loans:    │  │   _____%              │                  │
    │  │   ____              │  │ Inclusion Index: ___  │                  │
    │  └─────────────────────┘  └─────────────────────┘                  │
    │                                                                      │
    │  ┌──────────────────────────────────────────────┐                  │
    │  │ MODEL HEALTH                                  │                  │
    │  │                                                │                  │
    │  │ Gini: ___ (trend: ↑↓→)    Drift: YES/NO       │                  │
    │  │ KS:   ___ (trend: ↑↓→)    Shadow tests: ___   │                  │
    │  │ RL signals this month: _______                 │                  │
    │  │ Model updates deployed: ___                    │                  │
    │  └──────────────────────────────────────────────┘                  │
    │                                                                      │
    │  ┌──────────────────────────────────────────────┐                  │
    │  │ SEGMENT PERFORMANCE (top segments by volume)   │                  │
    │  │                                                │                  │
    │  │  Segment    │ Loans │ AUM    │ NPA  │ Grad%  │                  │
    │  │  ───────────┼───────┼────────┼──────┼────────│                  │
    │  │  Dairy      │ _____ │ ___ Cr │ ___% │ ____%  │                  │
    │  │  Vendor     │ _____ │ ___ Cr │ ___% │ ____%  │                  │
    │  │  Gig worker │ _____ │ ___ Cr │ ___% │ ____%  │                  │
    │  │  Kirana     │ _____ │ ___ Cr │ ___% │ ____%  │                  │
    │  │  SHG        │ _____ │ ___ Cr │ ___% │ ____%  │                  │
    │  │  ─── ALL ───┼───────┼────────┼──────┼────────│                  │
    │  │  TOTAL      │ _____ │ ___ Cr │ ___% │ ____%  │                  │
    │  └──────────────────────────────────────────────┘                  │
    │                                                                      │
    └─────────────────────────────────────────────────────────────────────┘
```

This dashboard gives any lender -- bank board, NBFC risk committee, fintech investor -- a single-page view of what the platform is delivering across portfolio performance, unit economics, compliance, monitoring impact, financial inclusion outcomes, model health, and segment-level breakdowns. Every number maps back to a specific stage in the 7-stage lifecycle and a specific layer in the 5-layer architecture.
