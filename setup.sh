#! /bin/sh
case $# in
3) ;;
*) echo usage $0 username password homedir; exit 1;;
esac

USERNAME=$1
PASSWORD=$2
HOMEDIR=$3

sed -i '/^PasswordAuthentication/s/no$/yes/' /etc/ssh/sshd_config

useradd -b $HOMEDIR -m -s /bin/bash $USERNAME
adduser $USERNAME sudo
echo ${USERNAME}:${PASSWORD} | chpasswd

service sshd restart
