#!/bin/bash

# Set up Cosmos DB alerts
az monitor metrics alert create \
  --name "HighRUConsumption" \
  --resource-group $RESOURCE_GROUP \
  --scopes $COSMOS_ID \
  --condition "avg requestUnits > 800" \
  --description "High RU consumption detected"

# Set up Function alerts
az monitor metrics alert create \
  --name "FunctionErrors" \
  --resource-group $RESOURCE_GROUP \
  --scopes $FUNCTION_ID \
  --condition "count failures > 0" \
  --description "Function errors detected"