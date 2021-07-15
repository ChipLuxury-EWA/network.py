#!/bin/python3

import socket
import select

MAX_MSG_LENGTH = 1024
SERVER_PORT = "0.0.0.0"
SERVER_IP = 8822


def main():
    print("server is setting up")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_PORT, SERVER_IP))
    server_socket.listen()
    print("listening for a new clients")
    client_sockets = []
    while True:
        ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets, [], [])
        for current_socket in ready_to_read:
            if current_socket is server_socket:
                (client_socket, client_address) = current_socket.accept()
                print("New client joined: ", client_address)
                client_sockets.append(client_socket)
            else:
                print("new data from client__: ")
main()