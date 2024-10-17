This project involves a server that distributes a dataset (containing ID, name, email, and city) among multiple clients. The goal is to ensure each client receives a unique set of records, and no two clients share the same data. Clients connect to the server to request data or disconnect, and the server dynamically manages the distribution of records as follows:

Data Distribution: Upon connection, the server assigns a random subset of data to the client (as long as non-duplicate data is available).
Client Requests: Clients can request the data assigned to them, or ask for a list of client IDs with the data they currently hold.
Client Disconnection: When a client disconnects, the server redistributes that client's data to other connected clients.
Server-Client Interaction: All data exchanges between clients are mediated by the server; clients have no direct communication with each other.
