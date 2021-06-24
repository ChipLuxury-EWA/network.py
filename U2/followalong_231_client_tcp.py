#!/bin/python3
import socket
IP = "127.0.0.1"
PORT = 8820
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect((IP, PORT))
my_socket.send("stay calm and keep codingl".encode())
data = my_socket.recv(1024).decode()
print("the data is: " + data)
my_socket.close()