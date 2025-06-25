# Cost Analysis

## Current Costs (Before Optimization)

| Component          | Calculation                     | Monthly Cost |
|--------------------|---------------------------------|-------------:|
| Cosmos DB Storage  | 2M records × 300KB = 600GB     | $150        |
| Cosmos DB RUs      | Estimated 10,000 RU/s          | $600        |
| **Total**          |                                 | **$750**    |

## Projected Costs (After Optimization)

| Component          | Calculation                     | Monthly Cost |
|--------------------|---------------------------------|-------------:|
| Cosmos DB Storage  | 500K records × 300KB = 150GB   | $37.50      |
| Cosmos DB RUs      | Reduced to 5,000 RU/s          | $300        |
| Blob Storage       | 1.5M records × 300KB = 450GB   | $9          |
| **Total**          |                                 | **$346.50** |

## Savings

- **Monthly Savings:** $403.50 (53.8% reduction)
- **Annual Savings:** $4,842
