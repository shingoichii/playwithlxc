#! /bin/sh
case $# in
2) ;;
*) echo usage $0 username password; exit 1;;
esac

USERNAME=$1
PASSWORD=$2

sed -i '/^PasswordAuthentication/s/^/#/' /etc/ssh/sshd_config

useradd -b /home -m -s /bin/bash $USERNAME
adduser $USERNAME sudo
echo ${USERNAME}:${PASSWORD} | chpasswd

service sshd restart
