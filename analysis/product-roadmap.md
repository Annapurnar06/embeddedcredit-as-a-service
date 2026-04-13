# Product Development Roadmap

## Phase 0: PoC Sprint (Weeks 0-4)
**Goal**: Prove voice-to-loan works for 1 segment + 1 lender

| Week | Engineering | Lender | Borrower |
|------|-----------|--------|----------|
| 1 | Cartesia voice (Gujarati), FastAPI scaffold, Mem0 | LOI signed | 10 test calls |
| 2 | ULI simulator for dairy cooperative, DairyScore v0.1 | Shadow plan shared | 25 farmers onboarded |
| 3 | Underwriting + manual review queue, compliance audit trail | Shadow mode running | 50 applications |
| 4 | Dynamic seasonal product, UPI disbursement, monitoring v0.1 | First 10-20 loans | First loans received |

**Team**: 3-4 | **Metrics**: >60% call completion, >40% application completion, <10 min decision

## Phase 1: MVP (Months 1-3)
**Segments**: Dairy farmer (Gujarat), Street vendor (UP/Bihar), ASHA worker (Jharkhand)

| Month | Backend | Intelligence | Agents |
|-------|---------|-------------|--------|
| 1 | ULI connector (5 sources), BankConnect, LOS v0.1 | DairyScore v1.0, VendorScore v0.1, Data quality v0.1 | Voice Hindi+Gujarati, WhatsApp vendors |
| 2 | Sentinel MCP client, compliance engine, Neo4j | VendorScore v1.0, DBTScore v0.1, 3 product types | Monitoring v0.1, WhatsApp buttons |
| 3 | Multi-lender, API keys, dashboard v0.1 | Shadow testing framework, champion/challenger | Tamil prep, memory-aware conversations |

**Team**: 8-10 | **Target**: 500-1,000 loans, 3 lenders, first EMI data

## Phase 2: Multi-Segment (Months 3-6)
**New segments**: Delivery worker, Crop farmer, SHG woman, Kirana ONDC, Fisherman

| Area | Deliverables |
|------|-------------|
| Intelligence | GigScore, CropScore, SHGScore, MerchantScore, FisherScore; RL reward v0.1; Graph memory |
| Agents | +Telugu, Kannada, Tamil, Malayalam; weather triggers; proactive outreach |
| Platform | Journey Studio v0.1; Co-lending (CLA); ONDC SDK v0.1; Dashboard v1.0 |

**Team**: 15-20 | **Target**: 2,000-5,000 loans/mo, 5+ lenders, NPA <5%

## Phase 3: Full Platform (Months 6-12)
All 33 segments, all 8 products, co-lending, ONDC embedding, graph fraud detection, RL loop v1.0, 99.9% uptime SLA, SOC 2 prep.

**Target**: 10,000-25,000 loans/mo, 12-20 lenders, NPA <4%

## Phase 4: Scale (Months 12-24)
Pan-India, 50K+ loans/mo, insurance integration, federated fraud detection, government scheme auto-routing, API marketplace.

---

## Agent Development Lifecycle

| Phase | Activities |
|-------|-----------|
| **Build** | Define persona per segment, intent taxonomy per language, conversation state machines, Cartesia voice selection, Mem0 memory schema |
| **Test** | 50+ utterances per intent per language, end-to-end flow tests, adversarial tests, rural accent recordings, latency tests (<2s response) |
| **Evaluate** | Intent accuracy, call/journey completion, weekly 50-call human review, borrower NPS, outcome tracking, bias detection |
| **Deploy** | Shadow mode -> 5% canary -> 25% -> 100%, circuit breaker (>5% error -> human fallback), real-time dashboard |
| **Improve** | Every call outcome is training signal, monthly intent retrain, quarterly conversation flow updates, A/B testing always |
