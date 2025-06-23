import datetime
import json
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient

# ---- CONFIG ----
COSMOS_URL = "<YOUR_COSMOS_URL>"
COSMOS_KEY = "<YOUR_COSMOS_KEY>"
DB_NAME = "<YOUR_DB_NAME>"
CONTAINER_NAME = "<YOUR_CONTAINER_NAME>"

BLOB_CONN_STR = "<YOUR_BLOB_CONN_STR>"
BLOB_CONTAINER = "billing-archive"

# ---- SETUP ----
cosmos_client = CosmosClient(COSMOS_URL, COSMOS_KEY)
container = cosmos_client.get_database_client(DB_NAME).get_container_client(CONTAINER_NAME)

blob_client = BlobServiceClient.from_connection_string(BLOB_CONN_STR)
archive_container = blob_client.get_container_client(BLOB_CONTAINER)

# ---- ARCHIVAL ----
cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=90)
query = f"SELECT * FROM c WHERE c.createdAt < '{cutoff.isoformat()}'"

for item in container.query_items(query, enable_cross_partition_query=True):
    blob_name = f"{item['id']}.json"
    archive_container.upload_blob(blob_name, json.dumps(item), overwrite=True)
    container.delete_item(item, partition_key=item['partitionKey'])

print("Archival run complete.")
