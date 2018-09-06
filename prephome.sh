#! /bin/sh

HOMETOP=/home/prj
USERLIST=userlist.txt
KSUSER=ksuser
uid=$(id -u $KSUSER)
gid=$(id -g $KSUSER)

for d in `awk '{print $1}' $USERLIST`
do
    DIR=$HOMETOP/$d
    mkdir $DIR
    chown $uid:$gid $DIR
done
