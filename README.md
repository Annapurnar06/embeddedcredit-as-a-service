# Embedded Credit-as-a-Service: ULI-Enabled Agentic Lending Architecture

A comprehensive solution architecture for serving India's 300 million underserved borrowers through AI-native, DPI-enabled embedded credit infrastructure.

## Overview

This project documents the design of a 5-layer lending stack that combines India's Unified Lending Interface (ULI) with agentic AI to deliver personalized, inclusive credit to 33 underserved borrower segments -- from dairy farmers and street vendors to gig workers and ASHA workers.

The core thesis: **lending becomes an intelligence problem, not an infrastructure problem**, when you combine ULI's 136 data services with AI decisioning, segment-specific models, and multi-channel borrower agents.

## Repository Structure

```
.
├── README.md                                  # This file
├── architecture/
│   └── system-architecture.md                 # Complete 5-layer technical architecture
│                                              #   - 7 diagrams with explanations
│                                              #   - 40 indexed references
│                                              #   - MCP protocol architecture
│                                              #   - RL training loop design
│                                              #   - Segment-to-lender routing
│                                              #   - Graph memory architecture
│                                              #   - Implementation roadmap
└── deck/
    └── transformation-story.md                # Narrative storytelling deck
                                               #   - Why 300M Indians are excluded
                                               #   - How ULI changes the data layer
                                               #   - Layer-by-layer transformation
                                               #   - 3 borrower journey stories
                                               #   - Gaps solved, outcomes unlocked
```

## The 5-Layer Stack

| Layer | Name | Purpose |
|-------|------|---------|
| 5 | Borrower Interface Agents | Voice, WhatsApp, app, partner, monitoring agents in 12+ languages |
| 4 | Segment-Specific Intelligence | 7 specialized modules converting raw ULI data to credit signals |
| 3 | AI Decisioning Core | Sentinel AI + MCP protocol for dynamic credit decisions |
| 2 | ULI Data Orchestration | Parallel fetch from 136 data services with quality layer |
| 1 | Verifiable Environment | RL reward surface where every loan improves the system |

## 33 Borrower Segments

**Agricultural** (8): Dairy farmer, crop farmer, fisherman, warehouse, solar pump, mandi trader, FPO, community solar

**Informal Economy** (8): Street vendor, domestic worker, beauty salon, handloom weaver, potter, private teacher, ASHA worker, SHG women

**Gig/Platform** (7): Delivery worker, auto-rickshaw, Urban Company, Ola/Uber driver, social reseller, kirana (ONDC), EV buyer

**Lifecycle/Other** (10): Medical patient, IVF borrower, ITI student, upskilling, rental deposit, home builder, wedding, death bridge, maternity, construction worker

## 8 Dynamic Product Types

1. **Seasonal Dynamic** -- EMI follows earning seasons (dairy, crop)
2. **Daily Micro** -- tiny daily deductions from earnings (vendor, gig)
3. **Catch/Sale-Linked** -- repay when revenue lands (fisherman, weaver)
4. **Income-Contingent** -- pay % of income, not fixed EMI (student)
5. **Moratorium-with-Trigger** -- auto-pause on weather/health events
6. **Bridge (Zero-Interest)** -- short-term gap funding (ASHA DBT delay)
7. **Staged Disbursement** -- release funds at milestones (medical, home)
8. **Payout-Linked** -- auto-deduct from platform payouts (ONDC, gig)

## Key References

- [ULI / RBIH](https://rbihub.in) -- Unified Lending Interface
- [Sentinel AI MCP](https://www.finbox.in/blog/credit-decisions-through-chat-sentinel-ai-is-now-mcp-ready) -- Agentic credit decisioning
- [McKinsey: The Future is Agentic](https://www.mckinsey.com/capabilities/risk-and-resilience/our-insights/the-future-is-agentic) -- Agentic AI in credit
- [FinRegLab: The Next Wave Arrives](https://finreglab.org/wp-content/uploads/2025/09/FinRegLab_09-04-2025_The-Next-Wave-Arrives.pdf) -- Agentic AI market scan

Full reference index (40 sources) available in `architecture/system-architecture.md`.

## License

This is a research and design document. Not affiliated with any specific platform or institution.
