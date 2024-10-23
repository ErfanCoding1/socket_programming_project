This project involves a server that distributes a dataset (containing ID, name, email, and city) among multiple clients. The goal is to ensure each client receives a unique set of records, and no two clients share the same data. Clients connect to the server to request data or disconnect, and the server dynamically manages the distribution of records as follows:

Data Distribution: Upon connection, the server assigns a random subset of data to the client (as long as non-duplicate data is available).
Client Requests: Clients can request the data assigned to them, or ask for a list of client IDs with the data they currently hold.
Client Disconnection: When a client disconnects, the server redistributes that client's data to other connected clients.
Server-Client Interaction: All data exchanges between clients are mediated by the server; clients have no direct communication with each other.


update 1.1

Project Update Report

Data Tracking for Clients
Each time a client connects to the server, the data assigned to that client is saved into a CSV file. This file helps track which data belongs to each client, ensuring better management and traceability of distributed data.

Unique Data Count Notification
Upon every connect or disconnect event, the server now prints the number of unique records available to the terminal. This real-time feedback keeps us informed of the remaining unique data records.

Requesting Client Data by IDs
When a client sends a request_ids command, it now provides a list of IDs as input. The server checks which client owns the requested IDs and returns the results, fulfilling the requirement for targeted data requests.

Data Distribution Upon Connection
Data distribution has been enhanced to allocate records to clients immediately upon connection. The server now assigns a random number of records to the client, rather than distributing records one by one. This improves efficiency and aligns with the intended project design
