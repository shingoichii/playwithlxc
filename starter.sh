#! /bin/sh
#set -x

#DEBUG=True
DEBUG=False

LXC="/snap/bin/lxc"
LINUX="ubuntu:18.04"
SCRIPT="setup.sh"

SSHPORT=22
WWWPORT=80
APPPORT=4011

# python scripts
WAIT_CONTAINER="./wait_container.py"
WAIT_ADDRESS="./wait_address.py"

doit()
{
    if [ "$DEBUG" = "True" ]
    then
        echo $1
    else
        eval $1
    fi
    return 0
}

waitit()
{
    what=$1
    which=$2
    if [ "$DEBUG" = "True" ]
    then
        echo waiting $what $which
    else
	case $what in
	    "container")
		$WAIT_CONTAINER $which ;;
	    "address")
		address=`$WAIT_ADDRESS $which` ;;
	    *)
		: ;;
	esac
    fi
    return 0
}

while read n container user password sshport wwwport appport
do
    doit "$LXC launch $LINUX $container"
    waitit container $container
    doit "$LXC file push $SCRIPT ${container}/tmp/${SCRIPT}"
    doit "$LXC exec ${container} -n -- bash /tmp/${SCRIPT} $user $password"
    # -n needed for not stealing stdin
    waitit address $container
    doit "$LXC config device add $container ssh proxy listen=tcp:0.0.0.0:${sshport} connect=tcp:${address}:${SSHPORT}"
    doit "$LXC config device add $container http proxy listen=tcp:0.0.0.0:${wwwport} connect=tcp:${address}:${WWWPORT}"
    doit "$LXC config device add $container app proxy listen=tcp:0.0.0.0:${appport} connect=tcp:${address}:${APPPORT}"
done
