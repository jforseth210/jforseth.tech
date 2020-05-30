#Delete the user
user="$1"
userdel "$user"
#Delete their home folder, mailbox, and jforseth.tech userdata folder.
rm -rf /home/"$user"/
rm -f /var/mail/"$user"
rm -rf userdata/"$user"
