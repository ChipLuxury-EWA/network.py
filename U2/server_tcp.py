#!/bin/python3
import socket
import time
import random

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 8820))
server_socket.listen()
print("server is ready to your commands.")
(client_socket, client_address) = server_socket.accept()
print("client is in the matrix!")
print("client address is: " , client_address)

while True:
    data = client_socket.recv(1024).decode()
    print("client sent this: " , data)
    if daTIMEta == "Quit":
        print("closing client socket now...")
        client_socket.send("Bye".encode())
        break
    elif data == "NAME":
        msg = "The name of the server is: servo"
        client_socket.send(msg.encode())
    elif data == "TIME":
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        msg = "the time right now is: " + timestamp
        client_socket.send(msg.encode())
    elif data == "RAND":
        rand_numba = random.randint(1, 9)
        msg = "Random number is: " + str(rand_numba)
        client_socket.send(msg.encode())
    else:
        msg = "Please chose the right keyword!"
        client_socket.send(msg.encode())

client_socket.close()
server_socket.close()