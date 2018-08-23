#! /bin/sh
USERNAME=${USERNAME:-ksuser}
PASSWORD=${PASSWORD:-screencast}

sed -i '/^PasswordAuthentication/s/^/#/' /etc/ssh/sshd_config

useradd -b /home -m -s /bin/bash $USERNAME
adduser $USERNAME sudo
echo ${USERNAME}:${PASSWORD} | chpasswd

service sshd restart
