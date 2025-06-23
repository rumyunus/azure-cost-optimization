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
See diagram.png.

Repo structure
├── diagram.png            # architecture diagram
├── function/              # sample archival function
├── api_fallback/          # example fallback code  
├── README.md
Why this works
* Simple to build and maintain
* Saves money on storage and throughput
* No downtime, no data loss
* No API changes for clients

Notes
Use Blob Lifecycle rules to control long-term storage cost.
