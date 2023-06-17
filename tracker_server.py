# This server will keep track of the currently connected peers in the network

import threading
import socket

# localhost
host = "127.0.0.1"
# do not take any reserved or well known ports
port = 55550

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
addresses = []
port_numbers = []


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
            break


# This is the method that runs first
def receive():
    # Accepting all the connections
    while True:
        print("receive function is running on the server!")
        # returns a tuple
        # returns the client and the address of the client
        client, address = server.accept()
        addresses.append(address)

        # you have cut down the address str type casting
        print(f"Connected with {str(address)}")

        port_name = "PORT"
        client.send(port_name.encode('ascii'))

        port_name_received = client.recv(1024).decode('ascii')

        port_numbers.append(port_name_received)
        clients.append(client)

        print("These are the available peers in the network:")
        for address in addresses:
            print(address)

        # letting know the specific client that it has connected to the server
        client.send("Connected to the server".encode('ascii'))

        print("These are the current known ports of the peers: " + str(port_numbers))

        broadcast(str(port_numbers).encode('ascii'))

        # define and run a thread
        # because we want to be able to handle multi clients same time

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()
