#!/bin/python3

from chatlib import *

msg7 = "username#password"
msg8 = "test#username#pa#ssword#foo"

a = split_data(msg8 ,5)

print(a)

#b = join_data(["username" , "password"])
b = join_data(["question" , "ans1" , "ans2" , "ans3" , "ans4" , "correct", 34, 35.52, "fff", 23])

# print(b)

c = build_message("LOGIN", "user#pass")
# print(c)

d = parse_message("LOGIN           |  Z9|user#pass")
print((d))