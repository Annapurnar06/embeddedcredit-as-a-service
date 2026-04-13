# Cost Analysis

## 1. API Costs

### Cartesia Voice AI
| Tier | Price (USD) | Minutes | Cost/Min |
|------|-------------|---------|----------|
| Free | $0 | ~50 | $0 |
| Pro | $99/mo | ~10,000 | $0.010 |
| Growth | $239/mo | ~50,000 | $0.005 |
| Enterprise | Custom | Unlimited | ~$0.003 |

### Mem0 Memory
| Tier | Ops/Month | Price |
|------|-----------|-------|
| Free | 10,000 | $0 |
| Pro | 100,000 | $249/mo |
| Enterprise | Unlimited | Custom |

### Finbox APIs (INR, estimated enterprise rates)
| Product | Per-Call | 5K/mo Volume | Monthly |
|---------|---------|-------------|---------|
| BankConnect | INR 25-50 | 5,000 | INR 1.25-2.5L |
| DeviceConnect | INR 10-20 | 5,000 | INR 0.5-1L |
| KYC (Aadhaar+PAN) | INR 5-15 | 5,000 | INR 0.25-0.75L |
| Sentinel AI | INR 20-50 | 5,000 | INR 1-2.5L |
| DPI/ULI | INR 10-30 | 5,000 | INR 0.5-1.5L |
| **Total Finbox** | | | **INR 3.5-8.25L/mo** |

### Other APIs
| Service | Cost | Monthly at Growth |
|---------|------|------------------|
| Credit Bureau (CIBIL etc.) | INR 25-40/pull | INR 1.25-2L |
| WhatsApp Business | INR 0.50-1.50/conversation | INR 0.25-0.75L |
| Account Aggregator | INR 10-25/fetch | INR 0.5-1.25L |
| ULI services | INR 5-15/service | INR 1.25-3.75L |

## 2. Infrastructure (AWS/GCP)

| Component | PoC | MVP | Growth | Scale |
|-----------|-----|-----|--------|-------|
| Compute | $50 | $200 | $600 | $2,000 |
| PostgreSQL | $30 | $100 | $300 | $800 |
| Redis | $15 | $50 | $100 | $200 |
| Neo4j | $0 | $65 | $200 | $500 |
| Storage/CDN/Monitoring | $15 | $100 | $280 | $750 |
| **Total** | **$110** | **$515** | **$1,480** | **$4,250** |

## 3. Team (Monthly, INR Lakhs)

| Role | PoC (3-4) | MVP (8-10) | Growth (15-20) | Scale (30-40) |
|------|-----------|-----------|---------------|---------------|
| Backend Engineers | 2L | 6L | 15L | 30L |
| ML/Voice Engineers | 2.5L | 5L | 10L | 20L |
| Frontend/QA | - | 3.5L | 7L | 14L |
| Product/Design | 1.5L | 3L | 6L | 12L |
| Domain/Sales | 1.5L | 3L | 9L | 18L |
| Compliance/Ops | - | 0.75L | 3L | 9L |
| **Total** | **7.5L** | **21.25L** | **50L** | **103L** |

## 4. Total Monthly Burn

| Category | PoC | MVP | Growth | Scale |
|----------|-----|-----|--------|-------|
| Team | 7.5L | 21.25L | 50L | 103L |
| APIs | 0.1L | 3L | 10L | 25L |
| Infra | 0.09L | 0.43L | 1.23L | 3.5L |
| Misc | 0.5L | 1L | 3L | 7L |
| **Total** | **8.2L** | **25.7L** | **64.2L** | **138.5L** |

## 5. Revenue & Break-Even

| Stream | Per Unit | Growth (5K loans) | Scale (25K loans) |
|--------|---------|-------------------|-------------------|
| Per-loan fee | INR 300 | 15L | 75L |
| SaaS (per lender) | INR 2L | 16L (8 lenders) | 60L (30 lenders) |
| NPA savings share | 10% | 5L | 25L |
| PSL premium | INR 100/loan | 3L | 15L |
| **Total** | | **39L** | **175L** |

**Break-even**: ~Month 18-20 at 12K loans/month with 15 lenders.

## 6. Funding Requirements

| Stage | Burn | Raise Target | Use |
|-------|------|-------------|-----|
| Pre-seed (4 mo) | 33L | **50-75L** | PoC, first lender |
| Seed (8 mo) | 206L | **3-4 Cr** | MVP, 5 lenders, team to 10 |
| Series A (12 mo) | 770L | **10-15 Cr** | 20 lenders, 20 segments, pan-India |
