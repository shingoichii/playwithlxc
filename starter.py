#! /usr/bin/env python3
# start login services

import os
import time
import random
import string
import pylxd

#DEBUG = True
DEBUG = False

LXC = "/snap/bin/lxc"
LINUX = "ubuntu:18.04"
SCRIPT = "setup.sh"
SSHPORT = 22
WWWPORT = 80
APPPORT = 4011
SSH_FORWARD_BASE = 20000 + SSHPORT
WWW_FORWARD_BASE = 20000 + WWWPORT
APP_FORWARD_BASE = 20000 + APPPORT % 100

N = 4
D = 10
alphabets = string.ascii_letters + string.digits + string.ascii_letters
# hack
alphabets = alphabets.replace('1', '0')
alphabets = alphabets.replace('l', 'L')

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

# (num, container_name, user_name, user_password)
userlist = [ [ n, "exp{:02}".format(n), "ksuser{:02}".format(n), genpw() ] for n in range(N) ]

def launch(u):
    cmd = "{} launch {} {}".format( LXC, LINUX, u[1])
    doit(cmd)

def getproxyport(id, base):
    return base + id * 100

def proxycmd(id, container, dev, proxyport, address, port):
    return "{} config device add {} {} proxy listen=tcp:0.0.0.0:{} connect=tcp:{}:{} bind=host".format(
        LXC, container, dev, proxyport, address, port)

def setup(u):
    num = u[0]
    container_name = u[1]
    user_name = u[2]
    user_password = u[3]
    #cmd = "{0} file push {1} {2}/tmp/{1} --mode 0744".format( LXC, SCRIPT, container_name )
    cmd = "{0} file push {1} {2}/tmp/{1}".format( LXC, SCRIPT, container_name )
    doit(cmd)
    #cmd = "{0} exec {1} /tmp/{2} {3} {4}".format( LXC, container_name, SCRIPT, user_name, user_password )
    cmd = "{0} exec {1} bash /tmp/{2} {3} {4}".format( LXC, container_name, SCRIPT, user_name, user_password )
    doit(cmd)
    #os.system("lxc list")
    client = pylxd.Client()
    # the following should work, but it generates an error (https://github.com/lxc/pylxd/issues/301)
    #c = client.containers.get(container_name)
    # inefficient workaround below instead
    for c in client.containers.all():
        #print(c.name)
        if c.name == container_name:
            break
    #print(container_name)
    #print(c.state().network['eth0']['addresses'])
    for a in c.state().network['eth0']['addresses']:
        #print(a['family'])
        if a['family'] == 'inet':
            container_address = a['address']
            break
    #print(container_address)
    proxyport = getproxyport(num, SSH_FORWARD_BASE)
    cmd = proxycmd(num, container_name, "ssh", proxyport, container_address, SSHPORT)
    doit(cmd)
    u.append(proxyport)
    proxyport = getproxyport(num, WWW_FORWARD_BASE)
    cmd = proxycmd(num, container_name, "http", proxyport, container_address, WWWPORT)
    doit(cmd)
    u.append(proxyport)
    proxyport = getproxyport(num, APP_FORWARD_BASE)
    cmd = proxycmd(num, container_name, "app", proxyport, container_address, APPPORT)
    doit(cmd)
    u.append(proxyport)

def printuserlist():
    for t in userlist:
        num, container, user, pw, ssh, www, app = t
        print(num, container, user, pw, ssh, www, app)

def main():
    for u in userlist:
        launch(u)
        time.sleep(5)
        setup(u)
    printuserlist()

if __name__ == '__main__':
    main()
