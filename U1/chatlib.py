#!/bin/python3
# changes made by chip_luxury.

# Protocol Constants
CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
# Max size of data field according to protocol
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message
ERROR_RETURN = None  # What is returned in case of an error

# Protocol Messages
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
    "login_msg": "LOGIN",
    "logout_msg": "LOGOUT",
    "log_state": "LOGGED",
    "get_quetion": "GET_QUESTION",
    "send_ans": "SEND_ANSWER",
    "my_score": "MY_SCORE",
    "highscore": "HIGHSCORE"
}  # .. Add more commands if needed

PROTOCOL_SERVER = {
    "login_ok_msg": "LOGIN_OK",
    "login_failed_msg": "ERROR",
    "logged_ans": "LOGGED_ANSWER",
    "your_question": "YOUR_QUESTION",
    "correct_ans": "CORRECT_ANSWER",
    "wrong_ans": "WRONG_ANSWER",
    "your_score": "YOUR_SCORE",
    "all_score": "ALL_SCORE",
    "no_question": "NO_QUESTIONS"
}  # ..  Add more commands if needed

def build_message(cmd, data):  # creating a msg from cmd string and data string
    if cmd in PROTOCOL_SERVER.values() or cmd in PROTOCOL_CLIENT.values():
        return cmd.ljust(CMD_FIELD_LENGTH) + DELIMITER + str(len(data)).zfill(4) + DELIMITER + data
    else:
        return ERROR_RETURN

def parse_message(data):  # extract cmd and data from a message
    cmd = data.split(DELIMITER, 3)[0].strip()
    msg_len = data.split(DELIMITER, 3)[1].strip()
    msg = data.split(DELIMITER, 3)[2].strip()
    if (data.count("|") == 2 and
        msg_len.isnumeric() and
            int(msg_len) == len(msg)):
        return cmd, msg
    else:
        return ERROR_RETURN

def split_data(msg, expected_fields):  # split the parameters from the data string
    if msg.count("#") == expected_fields - 1:
        return msg.split(DATA_DELIMITER, expected_fields - 1)
    else:
        return ERROR_RETURN

def join_data(msg_fields):  # join parameters from list to data message
    return DATA_DELIMITER.join(str(i) for i in msg_fields)