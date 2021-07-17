#!/bin/python3

import socket
import select

MAX_MSG_LENGTH = 1024
SERVER_PORT = "0.0.0.0"
SERVER_IP = 8821

MESSAGE_TO_SEND = []

def print_client_sockets(client_sockets):
    for client in client_sockets:
        print("\t", client.getpeername())

def main():
    print("server is setting up")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_PORT, SERVER_IP))
    server_socket.listen()
    print("listening for a new clients")
    client_sockets = []
    while True:
        ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets, client_sockets, [])
        for current_socket in ready_to_read:
            if current_socket is server_socket:
                (client_socket, client_address) = current_socket.accept()
                print("New client joined: ", client_address)
                client_sockets.append(client_socket)
                print_client_sockets(client_sockets)
            else:
                print("new data from client ", client_address, ":")
                msg = current_socket.recv(MAX_MSG_LENGTH).decode()
                if msg == "" or msg == "Q":
                    print("Closing connection")
                    client_sockets.remove(current_socket)
                    current_socket.close()
                    print_client_sockets(client_sockets)
                else:
                    print(msg)
                    # current_socket.send(msg.encode())
                    MESSAGE_TO_SEND.append((current_socket, msg))
                    for message in MESSAGE_TO_SEND:
                        current_socket, msg = message
                        if current_socket in ready_to_write:
                            current_socket.send(msg.encode())
                            MESSAGE_TO_SEND.remove(message)
main()