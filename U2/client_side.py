#!/bin/python3
import sys
sys.path.append("/home/chip_luxury/Documents/network.py/U1/")
import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

def build_and_send_message(conn, code, data):
	msg = chatlib.build_message(code, data)
	# print("--------> debug <-------- build message: ", msg)
	conn.send(msg.encode())

def recv_message_and_parse(conn):
	full_msg = conn.recv(1024).decode()
	cmd, data = chatlib.parse_message(full_msg)
	# cmd, data = chatlib.parse_message("LOGIN           |   9|user#pass") #testing
	return cmd, data

def connect():
	# Implement Code
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect((SERVER_IP, SERVER_PORT))
	return client_socket

def error_and_exit(error_msg):
	print(error_msg)
	print("exiting....")
	exit

def login(conn):
	username = input("Please enter username: ")
	password = input("Please enter password: ")
	data = chatlib.join_data([username, password])
	# print("--------> debug <-------- data is: "data)
	build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"], data)

def logout(conn):
	build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")

def build_send_recv_parse(conn, cmd, data):
	build_and_send_message(conn, cmd, data)
	msg_data, msg_code = recv_message_and_parse(conn)
	return msg_data, msg_code

def get_score(conn):
	score = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["my_score"], "")
	print(score)
	return score

def get_highscore(conn):
	highscore = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["highscore"], "")
	print(highscore)
	return highscore


def main():
	login(connect())	# logout(my_socket)
	# my_socket.close()
if __name__ == '__main__':
	main()