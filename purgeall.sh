#! /bin/sh
lxc stop --all
lxc delete `awk '{print $2}' < userlist.txt`
