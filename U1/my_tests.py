#!/bin/python3

from chatlib import split_data
from chatlib import join_data


msg7 = "username#password"
msg8 = "test#username#pa#ssword#foo"

a = split_data(msg7 ,3)

# print(a)

#b = join_data(["username" , "password"])
b = join_data(["question" , "ans1" , "ans2" , "ans3" , "ans4" , "correct", 34, 35.52, "fff", 23])

print(b)
