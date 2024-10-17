import socket
import threading
import pandas as pd
import random
from collections import deque


def load_data(file_path):
    df = pd.read_csv(file_path)
    return df.to_dict(orient='records')



data = load_data("RandomData.csv") 
clients = {}
client_count = 0
active_clients = 0
lock = threading.Lock()
to_distribute = deque()

def distribute_data():
    """Distribute data from the queue to active clients."""
    while to_distribute:
        record = to_distribute.popleft()  
        with lock:
            if clients:  
                random_client_id = random.choice(list(clients.keys()))
                clients[random_client_id].send(str(record).encode("utf-8"))
            
            
            
def handle_client(client_socket, client_id):
    global clients , active_clients , data
    assigned_data = [] 
    

    
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message == "request_data":
                if len(data) > 0:
                    with lock:
                        assigned_record = random.choice(data)
                        data.remove(assigned_record)  
                        assigned_data.append(assigned_record)
                        client_socket.send(str(assigned_record).encode("utf-8"))  
                else:
                    client_socket.send(b"No more unique data available.")
            elif message == "request_ids":
                with lock:
                    ids_info = {client_id: clients[client_id] for client_id in clients}
                    client_socket.send(str(ids_info).encode("utf-8"))        
            elif message == "show_data":
                with lock:
                    client_socket.send(str(assigned_data).encode("utf-8"))  
            elif message == "disconnect":
                client_socket.send(f"Client {client_id} disconnected.".encode('utf-8'))
                break
        except Exception as e:
            print(f"Error: {e}")
            break


    with lock:
        to_distribute.extend(assigned_data)
             
    client_socket.close()
    del clients[client_id]
    active_clients -= 1  
    
    print(f"Client[{client_id}] disconnected. Active clients: {active_clients}")
    
    distribute_data()
    
    if active_clients == 0:
        print("No active clients left. Closing server.")
        shutdown_server()


def shutdown_server():
    for client_socket in clients.values():
        client_socket.close()
    print("Server socket closed.")
    exit(0)



def main():
    
    global active_clients,client_count
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5555))
    server.listen(5)
    print("Server listening on port 5555")

    while True:
        client_socket, addr = server.accept()
        client_count += 1
        client_id = client_count
        clients[client_id] = client_socket
        active_clients += 1  

        print(f"Accepted connection from {addr}, assigned client ID: {client_id}")
        thread = threading.Thread(target=handle_client, args=(client_socket, client_id))
        thread.start()

if __name__ == "__main__":
    main()
