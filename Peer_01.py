import threading
import socket

# localhost
host = "127.0.0.1"
# do not take any reserved or well known ports
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []
peer_ports = []


# broadcasting messages from the server to all the clients
def broadcast(message):
    # implement the filtering of the messages here
    # implement the brand analytics and tracking here

    for client in clients:
        client.send(message)


def handle(client):
    # Running an infinite loop here
    while True:
        try:
            # receiving 1024 bytes
            message = client.recv(1024)
            print(message)
            broadcast(message)

        except:
            # find out the index of the failed client from the clients list
            index = clients.index(client)
            clients.remove(client)
            client.close()
            # we also remove the nickname of the removed client
            nickname = nicknames[index]
            broadcast(f"{nickname} has left the chat!".encode('ascii'))
            nicknames.remove(nickname)
            break


# This is the method that runs first
def receive():
    # Accepting all the connections
    while True:
        print("receive function is running on the server!")
        # returns a tuple
        # returns the client and the address of the client
        client, address = server.accept()

        # you have cut down the address str type casting
        print(f"Connected with {str(address)}")

        # we need to ask the client for the nickname
        # made change here
        name = "NICKNAME"
        client.send(name.encode('ascii'))

        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")

        broadcast(f"{nickname} joined the chat".encode('ascii'))
        # letting know the specific client that it has connected to the server
        client.send("Connected to the server".encode('ascii'))

        # define and run a thread
        # because we want to be able to handle multi clients same time

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


# Client_Side for the Server:

nickname = input("Choose your nickname before joining server: ")

# defining a socket for the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# this is the ip of the server that we want to connect to
client.connect(('127.0.0.1', 55550))


def client_receive():
    # always tries to receive data from the server
    while True:
        try:
            # receiving from the server
            message = client.recv(1024).decode('ascii')
            if message == "PORT":
                client.send(port)
            else:
                print(f'This is the newly found port ----> {message}')
        except:
            (print("An error occurred!"))
            client.close()
            break


def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))


# we are running 2 threads receive thread and the write thread

# the thread for receiving for the client part
receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

# the thread for writing
write_thread = threading.Thread(target=write)
write_thread.start()

# This is the additional server thread
server_thread = threading.Thread(target=receive)
server_thread.start()

print('The Peer is Up and Running!')
