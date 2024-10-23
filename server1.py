import os
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
    """Distribute data from the queue to a random active client."""
    while to_distribute:
        record = to_distribute.popleft()
        with lock:
            if clients:
                random_client_id = random.choice(list(clients.keys()))  
                try:
                    clients[random_client_id].send(str(record).encode("utf-8"))  
                    save_client_data(random_client_id, [record])  
                except Exception as e:
                    print(f"Error sending data to client {random_client_id}: {e}")
                    
           


def save_client_data(client_id, assigned_records):
    try:
        df = pd.DataFrame(assigned_records)
        df['client_id'] = client_id

        directory = 'client_data'
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, f'client_{client_id}_data.csv')

        if os.path.exists(file_path):
            df.to_csv(file_path, mode='a', header=False, index=False)
        else:
            df.to_csv(file_path, mode='w', header=True, index=False)

        print(f"Data saved for client {client_id}.")
    except Exception as e:
        print(f"Error saving data for client {client_id}: {e}")
        
def delete_client_data(client_id):
    """Delete the client's data CSV file."""
    directory = 'client_data'
    file_path = os.path.join(directory, f'client_{client_id}_data.csv')
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted data file for client {client_id}.")
    else:
        print(f"No data file found for client {client_id}.")
                


def handle_client(client_socket, client_id):
    global clients, active_clients, data
    assigned_data = []

    try:
        num_records = random.randint(1, 20)

        with lock:
            assigned_records = random.sample(data, min(num_records, len(data)))
            for record in assigned_records:
                data.remove(record)

            assigned_data.extend(assigned_records)

        client_socket.send(str(assigned_records).encode("utf-8"))

        save_client_data(client_id, assigned_records)

    except Exception as e:
        print(f"Error: {e}")
        
    print(f"Unique records available after connecting client {client_id}: {len(data)}")    

    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")

            if not message:  
                print(f"Client {client_id} disconnected unexpectedly.")
                break

            if message.startswith("request_ids:"):
                ids_list = eval(message.split(":")[1])

                with lock:
                    result = {}
                    for cid in clients.keys():
                        if cid in ids_list:
                            result[cid] = clients[cid]

                try:
                    client_socket.send(str(result).encode("utf-8"))
                except Exception as e:
                    print(f"Error sending data to client {client_id}: {e}")
                    break

            elif message == "show_data":
                with lock:
                    try:
                        client_socket.send(str(assigned_data).encode("utf-8"))
                    except Exception as e:
                        print(f"Error sending data to client {client_id}: {e}")
                        break
            elif message == "disconnect":
                print(f"Client {client_id} requested to disconnect.")
                break
        except Exception as e:
            print(f"Error: {e}")
            break

    with lock:
        to_distribute.extend(assigned_data)
        
    delete_client_data(client_id)    
       
        

    client_socket.close()
    del clients[client_id]
    active_clients -= 1

    print(f"Client[{client_id}] disconnected. Active clients: {active_clients}")
    
    print(f"Unique records available after disconnecting client {client_id}: {len(data)}")

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
    global active_clients, client_count

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
