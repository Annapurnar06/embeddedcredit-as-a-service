# Product-Market Fit Analysis: Embedded Credit-as-a-Service

## 1. Core PMF Thesis

**The insight**: India has 300M+ economically active adults who are credit-invisible not because they lack creditworthiness, but because existing lending infrastructure cannot read their economic signals. ULI now makes 136 data services available. The missing layer is intelligence that converts non-traditional data into credit decisions and delivers them through channels these borrowers actually use (voice, WhatsApp in local language).

**The wedge**: Dairy farmers in Gujarat. Single segment, single lender, single product, voice agent in Gujarati. Prove the model, then expand.

---

## 2. PMF Signals to Watch (YC Framework)

### Leading Indicators (Weeks 1-12)

| Signal | Target | Measurement |
|--------|--------|-------------|
| Lender LOI signed | 1-2 | Direct count |
| Borrower calls completed | 500+ | Voice agent logs |
| Loan applications via voice | 100+ | Pipeline conversion |
| Borrower call-back rate | >30% | Memory/CRM data |
| Lender requesting 2nd segment | 1 | Qualitative |
| Time-to-decision | <5 min | System metrics |
| Agent NPS (borrower) | >40 | Post-call survey |

### Lagging Indicators (Months 3-12)

| Signal | Target | Measurement |
|--------|--------|-------------|
| First EMI on-time rate | >90% | LOS data |
| 90-day DPD rate | <5% | Portfolio monitoring |
| Repeat borrower rate | >25% | Memory/CRM |
| Lender renewal/expansion | 100% | Contract |
| Cost per acquisition | <INR 200 | Unit economics |
| Word-of-mouth referrals | >10% | Attribution |

### "Hair on Fire" Test
- **Dairy farmer**: Needs INR 50-95K for animal purchase. Nearest branch: 12km. Can't fill English forms. Gets rejected because bureau score is thin. Current options: local moneylender at 36-60% APR. Our voice agent approves in 5 min at 15% APR using milk pouring data. **This is a hair-on-fire problem.**
- **ASHA worker**: DBT delayed 2-3 months. Needs INR 12K bridge loan. Zero options in formal system. Our bridge loan auto-repays when DBT credits. **Hair on fire.**
- **Street vendor**: PM SVANidhi caps at INR 50K but process is 2-3 weeks. Vendor needs working capital tomorrow. **Hair on fire.**

---

## 3. YC Advice Alignment

### "Do Things That Don't Scale"
- **First 50 loans**: Founder personally calls each dairy farmer, records the conversation, manually verifies cooperative data, hand-approves loans. This builds ground truth for the DairyScore model.
- **Cooperative visits**: Physically visit Amul/GCMMF cooperatives, meet pouring supervisors, understand data formats.
- **Lender hand-holding**: Sit in the first lender's office, watch their credit team, understand their exact workflow, objections, and compliance requirements.

### "Talk to Users"
- Weekly calls with 10 borrowers (via voice agent or direct)
- Monthly field visits to 3 villages
- Bi-weekly lender credit team meetings
- Track every borrower complaint verbatim in Mem0

### "Launch Fast"
- **Week 1**: Voice agent greeting + Aadhaar OTP in Gujarati (Cartesia)
- **Week 2**: Dairy cooperative data fetch (simulated, then real)
- **Week 3**: DairyScore v0.1 + manual underwriting
- **Week 4**: First loan disbursed through partner lender

---

## 4. PMF Experiments (First 90 Days)

### Experiment 1: Dairy Voice Agent (Weeks 1-4)
- **Hypothesis**: Dairy farmers in Anand/Kheda will complete loan applications via Gujarati voice at >40% conversion
- **Success metric**: >40 completed applications, >80% call completion, >50 NPS
- **Kill metric**: <15% call completion or >50% drop at Aadhaar OTP step

### Experiment 2: Cooperative Data -> Credit Score (Weeks 2-6)
- **Hypothesis**: 6-month milk pouring history + land record predicts repayment better than bureau alone
- **Success metric**: DairyScore Gini > 0.35 vs bureau-only Gini < 0.20 for this segment
- **Kill metric**: No meaningful separation between good/bad borrowers

### Experiment 3: Lender Shadow Mode (Weeks 4-8)
- **Hypothesis**: Lender will accept our credit decisions after 4-week shadow testing
- **Success metric**: >70% agreement rate, our approve-only pool has lower DPD
- **Kill metric**: <50% agreement or our recommendations show higher risk

### Experiment 4: Dynamic Product Acceptance (Weeks 6-10)
- **Hypothesis**: Seasonal dynamic EMI reduces DPD vs fixed EMI
- **Method**: Split 100 loans: 50 fixed EMI, 50 seasonal dynamic
- **Success metric**: >30% reduction in DPD for seasonal product

### Experiment 5: Post-Disbursement Monitoring (Weeks 8-12)
- **Hypothesis**: Proactive intervention (call when milk pouring drops >30%) prevents defaults
- **Success metric**: >40% reduction in 60-DPD for monitored group

---

## 5. Competitive Analysis

| Capability | Traditional MFI | Finbox Standalone | Bureau-Only | ECaaS Platform |
|-----------|----------------|-------------------|-------------|----------------|
| Thin-file scoring | No | Partial (DeviceConnect) | No | Yes (33+ segment models) |
| Voice in local language | No | No | No | Yes (10 languages) |
| Dynamic products | No (fixed EMI) | No | N/A | Yes (8 product types) |
| Post-disbursement monitoring | Manual calls | BankConnect alerts | No | Continuous ULI signals |
| PSL auto-classification | Manual | No | No | Automated |
| Borrower memory | None | None | None | Mem0 cross-session |
| Last-mile delivery | Branch/field agent | API-only | N/A | Voice + WhatsApp |
| Cost per loan | INR 3,000-15,000 | INR 500-1,500 (tech only) | INR 50-200 | INR 150-400 |

### Why Finbox Alone Isn't Enough
Finbox provides excellent infrastructure (BankConnect, DeviceConnect, Sentinel AI, DPI) but:
1. No last-mile borrower agent (voice/WhatsApp in local language)
2. No segment-specific intelligence layer (DairyScore, FisherScore, etc.)
3. No persistent borrower memory across interactions
4. No dynamic product design engine
5. No continuous post-disbursement monitoring with auto-intervention
6. No PSL auto-classification

**We build ON Finbox, not against Finbox.** Finbox is Layer 2-3 infrastructure. We are Layer 4-5 intelligence + agents.

---

## 6. Defensibility (Moat Analysis)

### Sovereign Context Moat (Primary)
Every loan processed creates segment-specific credit signal data, borrower behavior patterns in Mem0, graph relationships in Neo4j, and RL training data. **After 100K loans, no competitor can replicate this dataset.**

### Network Effects
More lenders -> better risk distribution -> lower rates -> more borrowers -> more data -> better models -> more lenders.

### Switching Costs
Lenders integrate once, get compliance automation, PSL reporting, monitoring dashboard. Borrower memory accumulates -- a borrower with 3 successful loans gets instant approval next time.

---

## 7. Traction Milestones

| Stage | Lenders | Monthly Loans | NPA Rate | MRR (INR) | Team | Timeline |
|-------|---------|---------------|----------|-----------|------|----------|
| Pre-seed PoC | 1 | 50-100 | <8% | 0 (pilot) | 3-4 | Month 0-3 |
| Seed | 3-5 | 500-1,000 | <5% | 3-5L | 8-10 | Month 3-9 |
| Series A ready | 8-12 | 5,000-10,000 | <4% | 25-50L | 15-20 | Month 9-18 |
| Series A growth | 20-30 | 25,000-50,000 | <3.5% | 1-3Cr | 30-40 | Month 18-30 |

---

## 8. Unit Economics by Segment

| Segment | Avg Ticket | Revenue/Loan | Cost/Loan | Margin/Loan | Breakeven Loans |
|---------|-----------|-------------|-----------|-------------|-----------------|
| Dairy farmer | INR 75K | INR 450 | INR 250 | INR 200 | 5,000 |
| Street vendor | INR 30K | INR 250 | INR 180 | INR 70 | 15,000 |
| Delivery worker | INR 50K | INR 350 | INR 200 | INR 150 | 7,000 |
| ASHA bridge | INR 12K | INR 80 | INR 120 | -INR 40 | N/A (subsidy) |
| Kirana ONDC | INR 100K | INR 600 | INR 280 | INR 320 | 3,200 |
| Crop farmer (KCC) | INR 150K | INR 700 | INR 300 | INR 400 | 2,500 |
| SHG woman | INR 25K | INR 200 | INR 150 | INR 50 | 20,000 |

Revenue model: Platform fee per loan (INR 200-700) + monthly SaaS per lender (INR 50K-5L) + revenue share on NPA reduction savings.

**Key insight**: High-ticket segments (crop farmer, kirana) subsidize social impact segments (ASHA, SHG). This is exactly what lenders need for PSL compliance.
