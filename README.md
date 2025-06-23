Azure Billing Cost Optimization

Problem:
Our Cosmos DB is growing fast because we store millions of billing records, but most of them (older than 3 months) are rarely read. This increases storage and RU costs unnecessarily.

Goal
Reduce costs without losing any data, breaking APIs, or causing downtime.

Solution
Hot data (recent 3 months) stays in Cosmos DB for fast access.

Cold data (older than 3 months) is moved to Azure Blob Storage (Cool or Archive tier).

If someone requests an old record, the system fetches it from Blob — transparently.

How it works
Archival Function:

Runs daily (or weekly).

Finds old records in Cosmos DB.

Saves them to Blob Storage.

Deletes them from Cosmos after verifying the upload.

API:

When reading, it tries Cosmos first.

If not found, it checks Blob and returns the result.

Clients don’t see any difference.

Diagram
Pls refer diagram.png for a simple data flow understanding

Why this works
* Simple to build and maintain
* Saves money on storage and throughput
* No downtime, no data loss
* No API changes for clients

Notes
Use Blob Lifecycle rules to control long-term storage cost.

Additional workarounds:
1. we can also use ADF pipeline for data transfer. 
2. we can use Azure data lake gen2 instead of Azure storage accounts.
3. Lifecycle policies on Archival data also in storage account.
