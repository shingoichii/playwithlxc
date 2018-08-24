#! /usr/bin/env python3
# start login services

import os
import random
import string
import pylxd

DEBUG = True
#DEBUG = False

LXC = "/snap/bin/lxc"
LINUX = "ubuntu:18.04"
SCRIPT = "setup.sh"
SSHPORT = 22
WWWPORT = 80
APPPORT = 4011
SSH_FORWARD_BASE = 20000 + SSHPORT
WWW_FORWARD_BASE = 20000 + WWWPORT
APP_FORWARD_BASE = 20000 + APPPORT % 100

N = 40
D = 10
alphabets = string.ascii_letters + string.digits + string.punctuation + string.ascii_letters
# hack
alphabets = alphabets.replace('1', '0')
alphabets = alphabets.replace('l', 'L')
alphabets = alphabets.replace('$', '%')
alphabets = alphabets.replace('"', '=')
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

def proxycmd(id, container, dev, base, address, port):
    address = "1.1.1.1"
    return "{} config device add {} {} proxy listen=tcp:0.0.0.0:{} connect=tcp:{}:{} bind=host".format(
        LXC, container, dev, base + id * 100, address, port)

def setup_network():
    client = pylxd.Client()
    for c in client.containers.all():
        container_name = c.name
        container_address = c.state().network['eth0']['addresses'][0]['address']
        cmd = proxycmd(u[0], u[1], "ssh", SSH_FORWARD_BASE, container_address, SSHPORT)
        doit(cmd)
        cmd = proxycmd(u[0], u[1], "http", WWW_FORWARD_BASE,
                       container_address, WWWPORT)
        doit(cmd)
        cmd = proxycmd(u[0], u[1], "app", APP_FORWARD_BASE,
                       container_address, APPPORT)
        doit(cmd)

def setup(u):
    cmd = "{} file push {} {}/tmp/{} --mode 0744".format( LXC, SCRIPT, u[1], SCRIPT )
    doit(cmd)
    cmd = "{} exec {} USERNAME={} PASSWORD='{}' /tmp/{}".format( LXC, u[1], u[2], u[3], SCRIPT )
    doit(cmd)
    setup_network()

def printuserlist():
    for t in userlist:
        num, container, user, pw = t
        print(num, container, user, pw)

def main():
    for u in userlist:
        launch(u)
        setup(u)
    printuserlist()

if __name__ == '__main__':
    main()
