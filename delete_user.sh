#/!bin/bash
# If you think this line is unecessary, you've never run this script without any arguments. 
# I assure you, it's essential.
if test "$1" != "bookboy210" && test "$1" != "justin" && if test "$#" -ne 1  ; then; then
    #Delete the user
    user="$1"
    userdel "$user"
    #Delete their home folder, mailbox, and jforseth.tech userdata folder.
    rm -rf /home/"$user"/
    rm -f /var/mail/"$user"
    rm -rf userdata/"$user"
else
    echo "You ran this script with one or more blank arguments. That's a good way to break something."
fi