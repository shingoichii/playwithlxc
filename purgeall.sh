#! /bin/sh
lxc stop --all

#lxc delete `awk '{print $2}' < userlist.txt`
lxc delete `lxc list | grep exp | awk '{print $2}'`
