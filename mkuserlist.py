#! /usr/bin/env python3
# make user list
# 0   1                        2        3        4       5       6
# num container_name(hostname) username password sshport wwwport appport

import random
import string

N = 40 # number of users; 1 <= N <= 99
D = 12 # password length

SSHPORT = 22
WWWPORT = 80
APPPORT = 4011
BASE = 20000

alphabets = string.ascii_letters + string.digits + string.ascii_letters
# hack
alphabets = alphabets.replace('1', '0')
alphabets = alphabets.replace('l', 'L')

def genpw():
    word = ""
    for k in range(D):
        word += alphabets[ random.randint(0, len(alphabets) - 1) ]
    return word

def genport(num, port):
    return BASE + port % 100 + num * 100

userlist = [ ("{:02}".format(n), "exp{:02}".format(n), "ksuser{:02}".format(n), genpw(),
                genport(n, SSHPORT), genport(n, WWWPORT), genport(n, APPPORT)) for n in range(N) ]

for t in userlist:
    num, container, user, pw, ssh, www, app = t
    print(num, container, user, pw, ssh, www, app)
