#!/bin/python3

import select
import socket
import sys
sys.path.append("/home/chip_luxury/Documents/network.py/U1/")
import chatlib

users = {}
questions = {}
logged_users = {} # a dictionary of client hostnames to usernames - will be used later

ERROR_MSG = "Error! "
SERVER_PORT = chatlib.SOCKET_PORT
SERVER_IP = chatlib.SOCKET_IP
# SERVER_PORT = 5678
# SERVER_IP = "127.0.0.1"

client_sockets = []
MESSAGE_TO_SEND = []


def build_and_send_message(conn, code, data):
	msg = chatlib.build_message(code, data)
	conn.send(msg.encode())
	print("[SERVER]{bld&snd}",msg)	  # Debug print

def recv_message_and_parse(conn):
	full_msg = conn.recv(1024).decode()
	cmd, data = chatlib.parse_message(full_msg)
	print("[SERVER]{rcv&pars}",full_msg)	  # Debug print
	return cmd, data

def setup_socket():
	print("Setting up the server")
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((SERVER_IP, SERVER_PORT))
	sock.listen()
	print("listening for a new clients")
	return sock

def print_client_sockets(client_sockets):
    for client in client_sockets:
        print("\t", client.getpeername())
# Data Loaders #

def load_questions():
	"""
	Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: questions dictionary
	"""
	questions = {
				2313 : {"question":"How much is 2+2","answers":["3","4","2","1"],"correct":2},
				4122 : {"question":"What is the capital of France?","answers":["Lion","Marseille","Paris","Montpellier"],"correct":3} 
				}
	
	return questions

def load_user_database():
	"""
	Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: user dictionary
	"""
	users = {
			"test"		:	{"password":"test","score":0,"questions_asked":[]},
			"yossi"		:	{"password":"123","score":50,"questions_asked":[]},
			"abc"		:	{"password":"123","score":500,"questions_asked":[]},
			"master"	:	{"password":"master","score":200,"questions_asked":[]},
			"Tom"		:	{"password":"1245","score":1000,"questions_asked":[]}
			}
	return users

def send_error(conn, error_msg):
	"""
	Send error message with given message
	Recieves: socket, message error string from called function
	Returns: None
	"""
	# Implement code ...
	


	
##### MESSAGE HANDLING
def handle_client_message(conn, cmd, data):
	global logged_users	 # To be used later
	if cmd == "LOGIN":
		handle_login_message(conn, data)
	elif cmd == "LOGOUT" or cmd == None: #the None is for ctrl+c cases
		print("[SERVER] client logging out...")
		handle_logout_message(conn)
	# elif cmd == None:
	# 	print("[SERVER]{hndl_clint_msg}_")
	else:
		print("[SERVER]{hndl_clint_msg} else")
		# handle_logout_message(conn)

def handle_login_message(conn, msg):
	global users  # This is needed to access the same users dictionary from all functions
	users = load_user_database()
	global logged_users	 # To be used later
	
	NAME = chatlib.split_data(msg,2)[0]
	PASSWORD = chatlib.split_data(msg,2)[1]
	if NAME in users.keys():
		print(NAME, "is a registered user,")
		if PASSWORD == users[NAME]["password"]:
			print("password match.")
			# logged_users[NAME] = 1
			build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_ok_msg"], "")
			# MESSAGE_TO_SEND.append((conn,))
		else:
			print("password did not match, try again")
			build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_failed_msg"], "")
	else:
		print("Sorry but", NAME, "is not registered.\nplease speak with your DevOps team!")
		build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_failed_msg"], "")

def handle_logout_message(conn):
	global logged_users
	print("removing player from the metrix...")
	client_sockets.remove(conn)
	conn.close()
	print_client_sockets(client_sockets)

def handle_getscore_message(conn, username):
	global users
	# Implement this in later chapters


def main():
	# Initializes global users and questions dicionaries using load functions, will be used later
	global users
	global questions
	print("Welcome to Trivia Server!")
	server_socket = setup_socket()
	
	while True:
		r2r, r2w, in_err = select.select([server_socket] + client_sockets, client_sockets, [])
		for current_socket in r2r:
			if current_socket is server_socket:
				(client_socket, client_address) = current_socket.accept()
				print("new client joined: ", client_address)
				client_sockets.append(client_socket)
				print_client_sockets(client_sockets)
			else:			#this is the "main" section 
				print("new data from client ", client_address, ":") #reciving the msg from client:
				command, data = recv_message_and_parse(current_socket)
				handle_client_message(current_socket, command, data)

if __name__ == '__main__':
	main()