::Push to github
git push
::Pull changes and reload apache:
::On prod server
plink.exe -ssh bookboy210@jforseth.tech -pw %bookboy210@jforseth.tech_password% -batch -t "cd /var/www/html;git pull;echo -e "%bookboy210@jforseth.tech_password%"\\n | sudo -S service apache2 reload"> prod_deploy_log.txt
::On backup server
plink.exe -ssh justin@localhost -P 2522 -pw %justin@localhost_password% -batch -t "cd /var/www/html;git pull;echo -e "%justin@localhost_password%"\\n | sudo -S service apache2 reload" > backup_deploy_log.txt
