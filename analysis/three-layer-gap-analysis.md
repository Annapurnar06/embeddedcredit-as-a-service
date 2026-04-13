# Three-Layer Gap Analysis

```
Layer 3: LAST MILE — Voice AI + WhatsApp + Monitoring Agents (built by us)
Layer 2: LENDING INTELLIGENCE — MCP + Scoring + Products (built by us on Finbox)
Layer 1: EXISTING LENDER SYSTEMS — CBS + LOS + Risk + Ops (owned by lender)
```

## Layer 1: Existing Lender Systems in India

| Lender Type | CBS | LOS | Risk Models | Digital | Integration Effort |
|------------|-----|-----|------------|---------|-------------------|
| PSB (SBI, PNB) | Finacle/BaNCS (mature) | Custom/vendor (medium) | Bureau-based (low) | App+web (medium) | Medium (4-8 weeks) |
| NBFC (Bajaj, Shriram) | Mix custom (medium) | Lentra/FinnOne (high) | ML models (high) | API-first (high) | Low (2-4 weeks) |
| SFB (AU, Equitas) | Cloud-native (high) | API-first (high) | Mandate-driven (high) | Strong (high) | Low (2-4 weeks) |
| MFI (Bandhan, CreditAccess) | Mifos/basic (low) | Paper to basic digital (low) | Group-based (low) | Limited (low) | High (8-16 weeks) |
| Platform (Swiggy, ONDC) | None | None | None (rich user data) | Native (high) | Low (embedded SDK) |

### Three Lender Personas
1. **Advanced** (SFB, large NBFC, fintech): Has cloud + APIs. Needs segment intelligence + agents. Integration: 2-4 weeks.
2. **Evolving** (PSB, mid NBFC, large MFI): Has basic digital + legacy CBS. Needs full origination + intelligence + compliance. Integration: 4-8 weeks.
3. **Basic** (RRB, coop bank, small MFI): Manual processes. Needs entire hosted digital stack. Integration: 12-16 weeks.

## Layer 2: Lending Intelligence — Finbox Dependency Analysis

| Finbox Product | Dependency | Alternative If Unavailable |
|---------------|------------|---------------------------|
| **Sentinel AI** | Critical | Build own rule engine + ML scoring (6-12 months) |
| **BankConnect** | High | Perfios/Karza or build parser (3-6 months) |
| **DeviceConnect** | High | CredoLab/Tookitaki alternative SDKs |
| **DPI** | Critical | Direct ULI integration (3-6 months, RBIH onboarding) |
| **Superflows KYC** | Medium | Digio/Signzy for Aadhaar+PAN |
| **Multi AA** | Medium | Setu AA / Onemoney direct |
| **LOS/Journey Studio/Prism** | Low | Build own or manual initially |

### What We Build ON TOP of Finbox
| Component | Why Finbox Doesn't Have It |
|-----------|--------------------------|
| 15+ segment scoring models | Finbox has engine but not DairyScore/FisherScore/SHGScore models |
| Data Quality Engine | No quality layer between raw ULI and credit decision |
| Dynamic Product Engine (8 types) | No product adjusts EMI to milk pouring seasons |
| Graph Memory (Neo4j) | Finbox doesn't maintain cross-lender longitudinal graph |
| Borrower Memory (Mem0) | No lending platform remembers context across voice calls |
| Monitoring Agent | Sentinel monitors portfolio; we monitor individual borrower life signals |
| Compliance Automation | No auto PSL classification, DPDP deletion, CLA checking |

## Layer 3: Last Mile — Critical Gaps

| Requirement | Cartesia | Gap | Solution |
|------------|---------|-----|---------|
| Text-to-Speech (10 langs) | 10 Indian languages | None | Direct use |
| **Speech-to-Text (ASR)** | **NOT provided** | **Critical** | **Deepgram ($0.004/min) + Google ($0.024/min) + Bhashini (free) fallback chain** |
| Rural accent handling | N/A (TTS only) | ASR accuracy | Fine-tune ASR; human escalation fallback |
| Emotional tone detection | Not provided | Medium | Separate emotion model on audio |

## Build vs Buy Matrix

| Component | Recommendation | Reason |
|-----------|---------------|--------|
| Voice TTS | **Buy** (Cartesia) | 12+ months to build |
| Voice ASR | **Buy** (multi-provider) | Deepgram+Google+Bhashini |
| Borrower memory | **Buy** (Mem0) | $0-249/mo vs 3 months build |
| Bank statement analysis | **Buy** (Finbox BankConnect) | Deep domain, 6 months build |
| ULI data orchestration | **Buy** initially (Finbox DPI) | Build parallel over time |
| **Segment scoring models** | **Build** (core IP) | This is the moat |
| **Dynamic product engine** | **Build** (core IP) | No existing solution |
| **Data quality layer** | **Build** (core IP) | Critical middleware |
| **Monitoring agent** | **Build** (differentiator) | Continuous ULI signals |
| **Compliance automation** | **Build** (core value) | Lender retention driver |
| **Graph memory** | **Build** (moat) | Cross-lender, longitudinal |
