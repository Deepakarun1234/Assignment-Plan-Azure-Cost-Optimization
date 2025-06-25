# Azure Cosmos DB Cost Optimization

## Solution Overview
Tiered storage solution for Azure Cosmos DB that:
- Maintains recent records in Cosmos DB
- Archives older records to Blob Storage
- Provides seamless retrieval

## Deployment

1. Clone repository
2. Set environment variables in `.env`
3. Run deployment:
```bash
./scripts/deploy.sh
```

## Testing
```bash
python -m pytest tests/
```