from azure.cosmos import CosmosClient
import os

def get_cosmos_client():
    return CosmosClient.from_connection_string(os.environ['COSMOS_CONNECTION_STRING'])

def get_container():
    client = get_cosmos_client()
    return client.get_database_client(os.environ['COSMOS_DATABASE']
        ).get_container_client(os.environ['COSMOS_CONTAINER'])

def create_record(record_data):
    container = get_container()
    record = {
        'id': record_data['id'],
        'partitionKey': record_data['partitionKey'],
        'createdDate': datetime.utcnow().isoformat(),
        'isArchived': False,
        'data': record_data
    }
    return container.create_item(record)