#!/bin/bash
# Change password
# user:password
if [ "$#" -ne 1 ] ; then
    echo "$1:$2" | chpasswd
else
    echo "You ran this script with one or more blank arguments. That's a good way to break something."
fi