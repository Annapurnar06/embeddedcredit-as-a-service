# Risk Management Framework

## 1. Risk Register

### Technical Risks
| ID | Risk | Prob | Impact | Mitigation |
|----|------|------|--------|------------|
| T1 | Cartesia API downtime | Med | High | WhatsApp text fallback; TTS cache; multi-provider (ElevenLabs backup) |
| T2 | Mem0 failure | Low | Med | Redis cache for active sessions; async writes; agent works without history |
| T3 | Finbox/Sentinel unavailable | Low | Critical | Request queue + retry; manual underwriting fallback; SLA with Finbox |
| T4 | ULI data source unreliable | High | High | Graceful degradation; score with available data; DeviceConnect fallback |
| T5 | Voice ASR inaccuracy (rural accents) | High | Med | Human escalation; multiple ASR providers; DTMF/text fallback |
| T6 | Model drift | Med | High | PSI/KS monitoring; drift detection; champion/challenger; monthly retrain |

### Credit Risks
| ID | Risk | Prob | Impact | Mitigation |
|----|------|------|--------|------------|
| C1 | High NPA in new segments | High | Critical | Shadow test first; FLDG; 500 loan cap per new segment; 90-day observe |
| C2 | Identity fraud | Med | High | BankConnect fraud + DeviceConnect + graph duplicate detection |
| C3 | Fraud rings | Low | Critical | Neo4j shared-attribute clustering; BankConnect cluster intelligence |
| C4 | Concentration risk | Med | High | Max 20% AUM per segment; geographic diversification; lender-level caps |
| C5 | Weather/climate mass default | Med | Critical | Auto-moratorium; PMFBY insurance; CGTMSE guarantee; diversification |

### Business Risks
| ID | Risk | Prob | Impact | Mitigation |
|----|------|------|--------|------------|
| B1 | Finbox builds intelligence layer | Med | Critical | Build sovereign context moat fast (100K+ loans); patent key innovations |
| B2 | Lender churn after pilot | High | High | Make switching costly (data + compliance); measurable NPA reduction |
| B3 | Cooperative data access revoked | Med | High | Multiple cooperatives; AA/ULI as fallback; DeviceConnect backup |

## 2. Incident Response (Top 5)

### Mass Default (30-DPD > 15% for any segment)
1. Pause origination for segment -> 2. Activate monitoring for all active loans -> 3. Analyze root cause -> 4. Auto-moratorium if weather -> 5. Lender communication within 4 hours -> 6. FLDG utilization plan

### Fraud Ring Detected (5+ apps sharing 3+ attributes)
1. Flag all cluster apps for manual review -> 2. Block devices/phones in cluster -> 3. BankConnect transaction analysis -> 4. Notify lenders within 2 hours -> 5. Report to bureaus -> 6. Update rules

### Voice Agent Wrong Loan Terms
1. Pull recording -> 2. If confirmed: honor communicated terms -> 3. Root cause fix -> 4. Audit similar calls last 7 days

### Data Breach Suspected
1. Rotate all API keys -> 2. Isolate systems -> 3. Notify CERT-In within 6 hours -> 4. Notify borrowers within 72 hours -> 5. Forensic team -> 6. Report within 7 days

### Borrower Distress on Voice Call
1. Immediate human escalation (30 seconds) -> 2. Do NOT discuss debt -> 3. Provide helpline numbers -> 4. Pause all collection 30 days -> 5. Flag for empathetic handling

## 3. Risk Appetite by Lender Type

| Dimension | PSB | NBFC | MFI | Fintech |
|-----------|-----|------|-----|---------|
| Max NPA tolerance | 3-5% | 5-8% | 2-4% | 5-10% (FLDG) |
| Auto-approve threshold | >700 score | >650 | >680 | >600 |
| Shadow test duration | 60-90 days | 30-45 days | 45-60 days | 14-30 days |
| Human review | Referred + 10% random | Referred | Referred + compliance | Referred only |
