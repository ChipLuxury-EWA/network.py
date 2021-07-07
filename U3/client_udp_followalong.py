#!/bin/python3
import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8821
MMS = 1024

my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    send_msg = input("write your message: ")
    my_socket.sendto(send_msg.encode(), (SERVER_IP, SERVER_PORT))
    (msg, remote_address) = my_socket.recvfrom(MMS)
    print("[SERVER] - response: ", msg.decode())
    
    if send_msg == "EXIT":
        break

my_socket.close()
