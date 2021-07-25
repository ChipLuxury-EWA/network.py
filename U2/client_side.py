#!/bin/python3
import sys
sys.path.append("/home/chip_luxury/Documents/network.py/U1/")
import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

#############################################################
def build_and_send_message(conn, code, data):
	msg = chatlib.build_message(code, data)
	conn.send(msg.encode())

def recv_message_and_parse(conn):
	full_msg = conn.recv(1024).decode()
	cmd, data = chatlib.parse_message(full_msg)
	return cmd, data

def build_send_recv_parse(conn, cmd, data):
	build_and_send_message(conn, cmd, data)
	msg_data, msg_code = recv_message_and_parse(conn)
	return msg_data, msg_code
#############################################################

def connect():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((SERVER_IP, SERVER_PORT))
	return sock

def error_and_exit(error_msg):
	print(error_msg)
	print("exiting....")
	exit

def login(conn):
	cmd = ""
	while cmd != "LOGIN_OK":
		username = input("Please enter username: ")
		password = input("Please enter password: ")
		data = chatlib.join_data([username, password])
		build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"], data)
		cmd, data = recv_message_and_parse(conn)
		print("[CLIENT] srv send: ", cmd)
	return

def logout(conn):
	build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")
	print("Logged out...")
	return

def get_score(conn):
	cmd, score = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["ms"], "")
	if cmd != "YOUR_SCORE":
		print("error in get_score function")
		error_and_exit()
	print("[CLIENT] your score is: ", score)
	return score

def get_highscore(conn):
	cmd, highscore = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["highscore"], "")
	if cmd != "ALL_SCORE":
		print("[CLIENT] error in get_highscore function")
		error_and_exit()
	print("[CLIENT]:\n",highscore)
	return highscore



def main():
	## SETUP:
	client_socket = connect()
	login(client_socket)

	## LOOP:
	print("""please choose option:
	GS - get your score
	HS - get high score
	LO - logout from server
	""")
	opt = ""
	while opt != "LO":
		opt = input("please select option: ")
		if opt == "GS":
			get_score(client_socket)
		elif opt == "HS":
			get_highscore(client_socket)
		elif opt == "LO":
			logout(client_socket)
		else:
			print("else - please choose right ans")


if __name__ == '__main__':
	main()