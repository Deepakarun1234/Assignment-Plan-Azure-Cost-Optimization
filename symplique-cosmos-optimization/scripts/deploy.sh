#!/bin/bash

# Validate environment
if [ -z "$RESOURCE_GROUP" ]; then
    echo "RESOURCE_GROUP not set"
    exit 1
fi

# Deploy infrastructure
echo "Deploying infrastructure..."
az deployment group create \
  --resource-group $RESOURCE_GROUP \
  --template-file infrastructure/main.bicep \
  --parameters infrastructure/parameters.json

# Deploy functions
echo "Deploying functions..."
func azure functionapp publish $(az deployment group show \
  -g $RESOURCE_GROUP \
  -n main \
  --query properties.outputs.functionAppName.value \
  -o tsv)

echo "Deployment complete"