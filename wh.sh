#! /bin/sh

gorogoro()
{
    u=$1
    p=$2
    echo $u and $p
}

while read n container user password sshport wwwport appport
do
    echo $n
    gorogoro $user $password
    sleep 1
done
