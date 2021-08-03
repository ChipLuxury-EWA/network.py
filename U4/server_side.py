#!/bin/python3

import select
import socket
import sys
sys.path.append("/home/chip_luxury/Documents/network.py/U1/")
import chatlib
import random

users = {}
questions = {}
logged_users = {} # a dictionary of client hostnames to usernames - will be used later


ERROR_MSG = "Error! "
SERVER_PORT = chatlib.SOCKET_PORT
SERVER_IP = chatlib.SOCKET_IP

client_sockets = []
MESSAGE_TO_SEND = []
# MESSAGE_TO_SEND = [(getpeername, message to send)]


def build_and_send_message(conn, code, data):
	global MESSAGE_TO_SEND
	msg = chatlib.build_message(code, data)
	# conn.send(msg.encode())
	MESSAGE_TO_SEND.append((conn, msg))
	print("[SERVER]{bld&snd}\t|",msg)	  # Debug print

def recv_message_and_parse(conn):
	full_msg = conn.recv(1024).decode()
	cmd, data = chatlib.parse_message(full_msg)
	print("[SERVER]{rcv&pars}\t|",full_msg)	  # Debug print
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
				1 : {"question":"Who is spider man?","answers":["Peter Parker","Bruce Win","Clark Kent","Tony Stark"],"correct":1},
				2313 : {"question":"How much is 2+2","answers":["3","4","2","1"],"correct":2},
				4122 : {"question":"What is the capital of France?","answers":["Lion","Marseille","Paris","Montpellier"],"correct":3} 
				}
	return questions

def create_random_question():
	rand_qstion_numba =random.choice(list(load_questions().keys()))
	question = load_questions()[rand_qstion_numba]["question"]
	answers = load_questions()[rand_qstion_numba]["answers"]
	data_list = [rand_qstion_numba, question]
	data_list.extend(answers)
	data = chatlib.join_data(data_list)
	return data

def load_user_database():
	"""
	Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: user dictionary
	"""
	users_data = {
			"test"		:	{"password":"test","score":0,"questions_asked":[]},
			"a"		:		{"password":"a","score":1005,"questions_asked":[]},
			"yossi"		:	{"password":"123","score":50,"questions_asked":[]},
			"abc"		:	{"password":"123","score":500,"questions_asked":[]},
			"master"	:	{"password":"master","score":200,"questions_asked":[]},
			"Tom"		:	{"password":"1245","score":1000,"questions_asked":[]}
			}
	return users_data

users = load_user_database() #loading users data in each run session of the server
							#I think this is duble code
def send_error(conn, error_msg):
	"""
	Send error message with given message
	Recieves: socket, message error string from called function
	Returns: None
	"""
	# Implement code ...
	


	
##### MESSAGE HANDLING
def handle_client_message(conn, cmd, msg_data):
	global logged_users	 # To be used later

	# print("------------debug------------\n" + cmd)
	if cmd == "LOGIN":
		handle_login_message(conn, msg_data)
	elif cmd == "LOGOUT":		#or cmd == None: #the None is for ctrl+c cases
		print("[SERVER] client logging out...")
		handle_logout_message(conn)
	elif cmd == None: # when user press ctrl+c he sends: None
		handle_logout_message(conn)
		# print("[SERVER]{hndl_clint_msg} - None")
	elif cmd == "MY_SCORE":
		handle_getscore_message(conn)
	elif cmd == "HIGH_SCORE":
		handle_highscore_message(conn)
	elif cmd == "GET_QUESTION":
		handle_question_message(conn)
	elif cmd == "SEND_ANSWER":
		handle_answer_message(conn, msg_data)
	elif cmd == "LOGGED":
		handle_logged_message(conn)
	else:
		print("[SERVER]{hndl_clint_msg} - else")
		# handle_logout_message(conn)

def handle_login_message(conn, msg):
	global logged_users	 # To be used later	
	NAME = chatlib.split_data(msg,2)[0]
	PASSWORD = chatlib.split_data(msg,2)[1]
	if NAME in users.keys():
		print(NAME, "is a registered user,")
		if PASSWORD == users[NAME]["password"]:
			print("password match.")
			# logged_users[NAME] = 1
			build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_ok_msg"], "")
			logged_users[conn.getpeername()[1]] = NAME
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
	logged_users.pop(conn.getpeername()[1])
	client_sockets.remove(conn)
	conn.close()
	print_client_sockets(client_sockets)

def handle_getscore_message(conn):
	global users
	NAME = logged_users[conn.getpeername()[1]]
	score = users[NAME]["score"]
	build_and_send_message(conn, chatlib.PROTOCOL_SERVER["ys"], score)

def handle_highscore_message(conn):
	global users
	# NAME = logged_users[conn.getpeername()[1]]
	sorted_users = sorted(users.items(), key=lambda item: item[1]["score"], reverse = True)
	msg = []
	for name, values in sorted_users:
		player_and_score = name + ":" + str(values["score"])
		msg.append(player_and_score)
	build_and_send_message(conn, chatlib.PROTOCOL_SERVER["as"] ,"\n".join(str(i) for i in msg))

def handle_logged_message(conn):
	global logged_users
	LU = ",".join(list(logged_users.values()))
	print("--------debug------\n" + LU)
	build_and_send_message(conn, chatlib.PROTOCOL_SERVER["logged_ans"], LU)

def handle_question_message(conn):
	data = create_random_question()
	build_and_send_message(conn, chatlib.PROTOCOL_SERVER["yq"], data)

def handle_answer_message(conn, data):
	global users
	global questions
	questions = load_questions()
	NAME = logged_users[conn.getpeername()[1]]
	qstn_numba = chatlib.split_data(data, 2)[0]
	player_ans = chatlib.split_data(data, 2)[1]
	currect_ans = questions[int(qstn_numba)]["correct"]
	##
	if int(player_ans) == currect_ans:
		users[NAME]["score"] += 5
		build_and_send_message(conn, chatlib.PROTOCOL_SERVER["ca"], "")
	else:
		build_and_send_message(conn, chatlib.PROTOCOL_SERVER["wa"], currect_ans)

def main():
	# Initializes global users and questions dicionaries using load functions, will be used later
	global users
	global questions
	global MESSAGE_TO_SEND

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
				print("new data from client ", client_address[1], ":") #reciving the msg from client:
				command, data = recv_message_and_parse(current_socket)
				handle_client_message(current_socket, command, data)				
				for message in MESSAGE_TO_SEND:
					current_socket, msg = message
					if current_socket in r2w:
						current_socket.send(msg.encode())
						MESSAGE_TO_SEND.remove(message)

if __name__ == '__main__':
	main()