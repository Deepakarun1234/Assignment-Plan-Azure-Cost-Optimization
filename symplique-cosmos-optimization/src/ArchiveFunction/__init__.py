import os
import json
from datetime import datetime, timedelta
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient
import logging

def main(timer: func.TimerRequest) -> None:
    # Initialize clients
    cosmos_client = CosmosClient.from_connection_string(os.environ['COSMOS_CONNECTION_STRING'])
    blob_service = BlobServiceClient.from_connection_string(os.environ['STORAGE_CONNECTION_STRING'])
    
    database = cosmos_client.get_database_client(os.environ['COSMOS_DATABASE'])
    container = database.get_container_client(os.environ['COSMOS_CONTAINER'])
    
    # Calculate cutoff date (3 months ago)
    cutoff_date = datetime.utcnow() - timedelta(days=90)
    
    # Query for records to archive
    query = f"SELECT * FROM c WHERE c.createdDate < '{cutoff_date.isoformat()}' AND c.isArchived = false"
    
    for record in container.query_items(query=query, enable_cross_partition_query=True):
        try:
            # Upload to Blob Storage
            blob_client = blob_service.get_blob_client(
                container="archives",
                blob=f"{record['partitionKey']}/{record['id']}.json"
            )
            blob_client.upload_blob(json.dumps(record['data']), overwrite=True)
            
            # Update metadata
            record['isArchived'] = True
            record['archiveBlobUrl'] = blob_client.url
            record['archiveDate'] = datetime.utcnow().isoformat()
            del record['data']  # Remove actual data from Cosmos
            
            container.upsert_item(record)
            
        except Exception as e:
            logging.error(f"Failed to archive record {record['id']}: {str(e)}")
            continue