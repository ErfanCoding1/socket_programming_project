import socket
import threading


def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode("utf-8")
            if not data:
                break
            print(f"Received: {data}")
        except:
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 5555))
    
  
    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.start()
    
    while True:
        command = input("Enter command (request_data, show_data , request_ids , disconnect): ")
        
        if command == "disconnect":
            print("Disconnecting from server.")
            break
        elif command not in ["request_data", "request_ids","show_data"]:
            print("Please enter a valid option.")
            continue
        
        client.send(command.encode("utf-8"))
        
    client.close()

if __name__ == "__main__":
    main()
