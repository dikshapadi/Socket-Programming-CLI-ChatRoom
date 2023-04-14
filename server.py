# Server side Chat Room
import socket
import threading

# Define the constants to be used
HOST_IP = socket.gethostbyname(socket.gethostname())
HOST_PORT = 12345
ENCODER = 'utf-8'
BYTESIZE = 1024

# Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST_IP, HOST_PORT))
server_socket.listen()

# Create two blank lists to store connected client sockets and their names
client_socket_list = []
client_name_list = []


def broadcast_message(message):
    """Send a message to all clients connected to the server"""
    for client in client_socket_list:
        client.send(message)


def receive_message(client_socket):
    """Receive message from any client and forward the message to be broadcast"""
    while True:
        try:
            message = client_socket.recv(BYTESIZE)
            broadcast_message(message)
        except:
            index = client_socket_list.index(client_socket)
            client_socket_list.remove(client_socket)
            client_socket.close()

            name = client_name_list[index]
            broadcast_message(f"{name} left the chat".encode(ENCODER))
            client_name_list.remove(name)
            break


def connect_client():
    """Connect incoming client to the server"""
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connect with {str(client_address)}")

        # Get name of the client
        client_socket.send('name'.encode(ENCODER))
        name = client_socket.recv(BYTESIZE).decode(ENCODER)

        # Append client to lists
        client_name_list.append(name)
        client_socket_list.append(client_socket)

        print(f"Name of client is {name}")
        broadcast_message(f"{name} joined the chat".encode(ENCODER))
        client_socket.send("Connected to the server".encode(ENCODER))

        thread = threading.Thread(target=receive_message, args=(client_socket,))
        thread.start()


print("Server is listening...")
connect_client()
