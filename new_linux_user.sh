#!/bin/bash
#Hash password
if [ "$#" -ne 1 ] ; then
    pass=$(perl -e 'print crypt($ARGV[0], "password")' $2)
    #Create a user with the /home/<USERNAME> home directory
    useradd -m -d /home/"$1" -p "$pass" "$1"
    #Echo the password to stdin and use it as a param for passwd command
    #echo "$2" | passwd "$1" --stdin
    #Create mail folder
    mkdir /home/"$1"/mail
    #Make it readable/writeable/executable by all users
    chmod 777 /home/"$1"/mail
else
    echo "You ran this script with one or more blank arguments. That's a good way to break something."
fi
