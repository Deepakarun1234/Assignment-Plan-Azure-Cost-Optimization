import os
import json
from datetime import datetime
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Get parameters
    record_id = req.params.get('id')
    partition_key = req.params.get('partitionKey')
    
    if not record_id or not partition_key:
        return func.HttpResponse("Missing parameters", status_code=400)
    
    # Initialize clients
    cosmos_client = CosmosClient.from_connection_string(os.environ['COSMOS_CONNECTION_STRING'])
    blob_service = BlobServiceClient.from_connection_string(os.environ['STORAGE_CONNECTION_STRING'])
    
    container = cosmos_client.get_database_client(os.environ['COSMOS_DATABASE']
        ).get_container_client(os.environ['COSMOS_CONTAINER'])
    
    # Get metadata
    try:
        record = container.read_item(record_id, partition_key)
    except:
        return func.HttpResponse("Record not found", status_code=404)
    
    # If archived, retrieve from Blob Storage
    if record.get('isArchived', False):
        try:
            blob_url = record['archiveBlobUrl']
            blob_client = blob_service.get_blob_client_from_url(blob_url)
            downloaded_blob = blob_client.download_blob()
            record['data'] = json.loads(downloaded_blob.readall())
            
            # Update last accessed time
            record['lastAccessed'] = datetime.utcnow().isoformat()
            container.upsert_item(record)
        except Exception as e:
            return func.HttpResponse(f"Failed to retrieve archived data: {str(e)}", status_code=500)
    
    return func.HttpResponse(json.dumps(record), mimetype="application/json")