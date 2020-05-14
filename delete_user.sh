user=$1
userdel $user
rm -rf /home/$user/
rm -f /var/mail/$user
rm -rf userdata/$user
