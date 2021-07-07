#!/bin/python3
import socket

SERVER_IP = "0.0.0.0"
SERVER_PORT = 8821
MMS = 1024
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
(client_msg, client_address) = server_socket.recvfrom(MMS)
msg = client_msg.decode()
print("client: ", client_address, "sent this message: ", msg)
server_response = "got your message!: " + msg
server_socket.sendto(server_response.encode(), client_address)
server_socket.close()