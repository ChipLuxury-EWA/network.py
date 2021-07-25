#!/bin/python3
import select
import socket
import sys
sys.path.append("/home/chip_luxury/Documents/network.py/U1/")
import chatlib

# GLOBALS
users = {}
questions = {}
logged_users = {} # a dictionary of client hostnames to usernames - will be used later
client_sockets = []

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"
MESSAGE_TO_SEND = []

def build_and_send_message(conn, code, data):
	msg = chatlib.build_message(code, data)
	print("[SERVER] ",msg)	  # Debug print
	conn.send(msg.encode())

def recv_message_and_parse(conn):
	full_msg = conn.recv(1024).decode()
	print("[CLIENT] ",full_msg)	  # Debug print	
	cmd, data = chatlib.parse_message(full_msg)
	return cmd, data

def print_client_sockets(client_sockets):
    print("[SERVER]")
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
			"master"	:	{"password":"master","score":200,"questions_asked":[]},
			"Tom"       :   {"password":"123456","score":0,"questions_asked":[]}
			}
	return users

def setup_socket():
	print("Setting up the server")
	sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sockt.bind((SERVER_IP, SERVER_PORT))
	sockt.listen()
	print("listening for a new clients")
	return sockt

def send_error(conn, error_msg):
	conn.send(error_msg.encode())

##### MESSAGE HANDLING
def handle_getscore_message(conn, username):
	global users
	# Implement this in later chapters

def handle_login_message(conn, data):
    global users
    users = load_user_database()
    global logged_users
    cmd, data = chatlib.parse_message(data)
    if cmd == "LOGIN": #move this to client message handle
        print("Logging new user:")
    NAME = chatlib.split_data(data,2)[0]
    PASSWORD = chatlib.split_data(data,2)[1]
    if NAME in users.keys():
        print(NAME, "is a registered user,")
        if PASSWORD == users[NAME]["password"]:
            print("password match.")
            conn.send(chatlib.PROTOCOL_SERVER["login_ok_msg"].encode())
        else:
            print("password did not match, try again")
            conn.send(chatlib.PROTOCOL_SERVER["login_failed_msg"].encode())
    else:
        print("Sorry but", NAME, "is not registered.\nplease speak with your DevOps team!")
        conn.send(chatlib.PROTOCOL_SERVER["login_failed_msg"].encode())

def handle_logout_message(conn):
	global logged_users
	print("closing conecttion")
	client_sockets.remove(conn)
	conn.close()
	print_client_sockets(client_sockets)

def handle_client_message(conn, cmd, data):
	global logged_users	 # To be used later
	handle_login_message(conn, data)
	handle_logout_message(conn)
	
def main():
	# Initializes global users and questions dicionaries using load functions, will be used later
	global users
	global questions
	print("Welcome to Trivia Server!")

	server_socket = setup_socket()
	msg = server_socket.recv(1024).decode()

	handle_client_message(server_socket, data)

if __name__ == '__main__':
	main()