#!/bin/python3
import sys
sys.path.append("/home/chip_luxury/Documents/network.py/U1/")
import chatlib

users = {}
questions = {}
logged_users = {}

def build_and_send_message(conn, code, data):
	msg = chatlib.build_message(code, data)
	print("[SERVER] ",msg)	  # Debug print
	conn.send(msg.encode())

def recv_message_and_parse(conn):
	full_msg = conn.recv(1024).decode()
	print("[CLIENT] ",full_msg)	  # Debug print	
	cmd, data = chatlib.parse_message(full_msg)
	return cmd, data

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
			"Tom"       :   {"password":"31520","score":0,"questions_asked":[]}
            }
	return users

log_msg = chatlib.build_message("LOGIN","test#test")

def handle_login_message(conn, data):
    global users
    users = load_user_database()
    global logged_users

    cmd, data = chatlib.parse_message(data)
    if cmd == "LOGIN":
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
    
handle_login_message("foo",log_msg)
