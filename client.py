# Client side Chat Room
import socket
import threading

# Define constants to be used
DEST_IP = socket.gethostbyname(socket.gethostname())
DEST_PORT = 12345
ENCODER = 'utf-8'
BYTESIZE = 1024

# Get name
name = input("Enter a nickname :")
# Create a client socket , connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((DEST_IP, DEST_PORT))


def receive_message():
    while True:
        try:
            message = client_socket.recv(BYTESIZE).decode(ENCODER)
            if message == 'name':
                client_socket.send(name.encode(ENCODER))
            else:
                print(message)
        except:
            print("An error occurred")
            client_socket.close()
            break


def send_message():
    while True:
        message = f'{name}: {input("")}'
        client_socket.send(message.encode(ENCODER))


receive_thread = threading.Thread(target=receive_message)
receive_thread.start()
send_thread = threading.Thread(target=send_message)
send_thread.start()
