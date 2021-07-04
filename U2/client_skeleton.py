#!/bin/python3
import sys
sys.path.append("/home/chip_luxury/Documents/network.py/U1/")
import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

def build_and_send_message(conn, code, data):
	msg = chatlib.build_message(code, data)
	print("debug build message: ", msg)
	conn.send(msg.encode())

def recv_message_and_parse(conn):
	full_msg = conn.recv(1024).decode()
	cmd, data = chatlib.parse_message(full_msg)
	# cmd, data = chatlib.parse_message("LOGIN           |   9|user#pass") #testing
	return cmd, data

def connect():
	# Implement Code
	trivia_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	trivia_socket.connect((SERVER_IP, SERVER_PORT))
	return trivia_socket

def error_and_exit(error_msg):
	print(error_msg)
	print("exiting....")
	exit

def login(conn):
	username = input("Please enter username: ")
	password = input("please enter password: ")
	data = chatlib.join_data([username, password])
	# Implement code
	build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"], data)

def logout(conn):
	build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")

def main():
	my_socket = connect()
	login(my_socket)
	# logout(my_socket)
	# my_socket.close()
if __name__ == '__main__':
	main()