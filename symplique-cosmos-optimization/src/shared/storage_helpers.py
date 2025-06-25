from azure.storage.blob import BlobServiceClient
import os
import json

def get_blob_service():
    return BlobServiceClient.from_connection_string(
        os.environ['STORAGE_CONNECTION_STRING'])

def upload_to_blob(container, blob_name, data):
    blob_service = get_blob_service()
    blob_client = blob_service.get_blob_client(
        container=container,
        blob=blob_name)
    blob_client.upload_blob(
        json.dumps(data),
        overwrite=True)
    return blob_client.url

def download_from_blob(blob_url):
    blob_service = get_blob_service()
    blob_client = blob_service.get_blob_client_from_url(blob_url)
    return json.loads(blob_client.download_blob().readall())