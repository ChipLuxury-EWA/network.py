#!/bin/python3
import socket
IP = "127.0.0.1"
PORT = 8822
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect((IP, PORT))
data = ""
while data != "Q":
    msg = input("Please enter your request: \nNAME/TIME/RAND/Q\n")
    # my_socket.send(msg.encode())
    # data = my_socket.recv(1024).decode()
    data = msg
    # print("server answer: " + data)

my_socket.close()