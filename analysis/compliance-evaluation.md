# Compliance Evaluation

## 1. RBI Digital Lending Guidelines (Sep 2022)

| Clause | Requirement | Implementation | Status |
|--------|------------|----------------|--------|
| Para 3 | Lending through regulated entities only | Platform is intelligence layer, NOT a lender | Compliant |
| Para 4 | KYC per RBI Master Direction | Aadhaar eKYC + PAN via Finbox Superflows | Automated |
| Para 5 | Prior borrower consent for data | Explicit consent before ULI/AA fetch, recorded | Automated |
| Para 6 | Key Fact Statement mandatory | Auto-generated KFS with APR, total cost, fees | Automated |
| Para 7 | Cooling-off period (3 days) | Enforced in LOS, disbursement blocked 3 days | Automated |
| Para 8 | Disburse to borrower bank account | UPI direct to verified account only | Automated |
| Para 10 | LSP disclosure | Platform disclosed on all communications | Automated |
| Para 13 | Grievance mechanism | In-app/WhatsApp + nodal officer + ombudsman | Built |
| Para 14 | Data storage in India only | All data in India cloud region | Enforced |

## 2. CLA Directions (Jan 2026)

| Requirement | Implementation |
|------------|----------------|
| Bank holds >= 20% on books | Validated before disbursement |
| Risk sharing documented | Template generation, compliance check |
| FLDG <= 5% outstanding | Real-time monitoring, alerts at 4%, blocks at 5% |
| Bank contact disclosed | Auto-included in KFS and WhatsApp |

## 3. DPDP Act 2023

| Section | Requirement | Implementation |
|---------|------------|----------------|
| Sec 4 | Purpose limitation | Documented per data source in consent flow |
| Sec 6 | Informed consent | Granular consent per data source, voice reads notice in borrower language |
| Sec 8 | Data retention limits | Configurable retention (consent: 365d, audit: 7 years) |
| Sec 12 | Right to erasure | delete_borrower_data() clears Mem0 + Neo4j |
| Sec 16 | Cross-border restrictions | data_localization: True, all processing in India |

## 4. PSL Auto-Classification

| Category | Target (% ANBC) | Qualifying Segments |
|----------|-----------------|-------------------|
| Agriculture | 18% | dairy_farmer, crop_farmer, fisherman, warehouse, solar_pump, mandi_trader, fpo |
| Small/Marginal Farmer | 10% (of 18%) | crop_farmer (<=5 acres), dairy_farmer (<=2 cattle) |
| Micro Enterprise | 7.5% | street_vendor, delivery_worker, auto_rickshaw, beauty_salon, kirana_ondc |
| Weaker Section | 12% | asha_worker, shg_woman, domestic_worker, construction_worker |

## 5. Voice AI Specific

| Requirement | Source | Implementation |
|------------|--------|----------------|
| Recording consent | IT Act + DPDP | Verbal consent at call start, stored in audit |
| Language accessibility | RBI inclusive banking | 10 Indian languages via Cartesia |
| Call timing | TRAI | Calls only 9 AM - 9 PM borrower local time |
| DND compliance | TRAI DND | DND registry check before outbound |
| No coercive collection | RBI Fair Practices | Collection scripts reviewed, no threatening language |

## 6. Audit Trail Requirements

| Event | Retention |
|-------|----------|
| API calls (request_id, timestamp, method, lender_id) | 7 years |
| Credit decisions (decision_id, score, reasons, model_version) | 7 years |
| Data access (source, consent_id, data_fetched) | 7 years |
| Voice calls (session_id, language, duration, recording_consent) | 7 years |
| Model/policy changes (old_version, new_version, approver) | Permanent |
