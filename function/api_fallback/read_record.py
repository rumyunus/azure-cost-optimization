# api_fallback/read_record.py

import json
from azure.cosmos import CosmosClient, exceptions
from azure.storage.blob import BlobServiceClient

COSMOS_URL = "<YOUR_COSMOS_URL>"
COSMOS_KEY = "<YOUR_COSMOS_KEY>"
DB_NAME = "<YOUR_DB_NAME>"
CONTAINER_NAME = "<YOUR_CONTAINER_NAME>"

BLOB_CONN_STR = "<YOUR_BLOB_CONN_STR>"
BLOB_CONTAINER = "billing-archive"

cosmos_client = CosmosClient(COSMOS_URL, COSMOS_KEY)
container = cosmos_client.get_database_client(DB_NAME).get_container_client(CONTAINER_NAME)

blob_client = BlobServiceClient.from_connection_string(BLOB_CONN_STR)
archive_container = blob_client.get_container_client(BLOB_CONTAINER)

def get_billing_record(record_id, partition_key):
    try:
        item = container.read_item(record_id, partition_key)
        return item
    except exceptions.CosmosResourceNotFoundError:
        # fallback to Blob
        blob_name = f"{record_id}.json"
        blob_data = archive_container.get_blob_client(blob_name).download_blob().readall()
        return json.loads(blob_data)
