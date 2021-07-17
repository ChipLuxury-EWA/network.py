#!/bin/python3
import socket
IP = "127.0.0.1"
PORT = 8821
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect((IP, PORT))
msg = ""
while msg != "Q":
    msg = input("Please enter your message: ")
    my_socket.send(msg.encode())
    server_ans = my_socket.recv(1024).decode()
    if msg == "Q":
        print("client want to quit, client will exit")
        break
    print("server answer: " + server_ans)
my_socket.close()