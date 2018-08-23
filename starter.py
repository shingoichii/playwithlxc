#! /usr/bin/env python3
# start login services

import os
import random
import string

DEBUG = True
#DEBUG = False

LXC = "/snap/bin/lxc"
LINUX = "ubuntu:18.04"
SCRIPT = "setup.sh"

N = 40
D = 10
alphabets = string.ascii_letters + string.digits + string.punctuation + string.ascii_letters
# hack
alphabets = alphabets.replace('1', '0')
alphabets = alphabets.replace('l', 'L')
alphabets = alphabets.replace('$', '%')
alphabets = alphabets.replace(':', ';')
alphabets = alphabets.replace('\'', '?')

def doit(cmd):
    if DEBUG:
        print(cmd)
    else:
        os.system(cmd)

def genpw():
    word = ""
    for k in range(D):
        word += alphabets[ random.randint(0, len(alphabets) - 1) ]
    return word

userlist = [ ( n, "exp{:02}".format(n), "ksuser{:02}".format(n), genpw() ) for n in range(N) ]

def launch(u):
    cmd = "{} launch {} {}".format( LXC, LINUX, u[1])
    doit(cmd)

def setup(u):
    cmd = "{} file push {} {}/tmp/{} --mode 0744".format( LXC, SCRIPT, u[1], SCRIPT )
    doit(cmd)
    cmd = "{} exec {} USERNAME={} PASSWORD='{}' /tmp/{}".format ( LXC, u[1], u[2], u[3], SCRIPT )
    doit(cmd)

def printuserlist():
    for t in userlist:
        num, container, user, pw = t;
        print(num, container, user, pw)

def main():
    for u in userlist:
        launch(u)
        setup(u)
    printuserlist()

if __name__ == '__main__':
    main()