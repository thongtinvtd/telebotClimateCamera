#!/bin/bash
# launch this script with root privileges
echo "Install program Telegram Bot"
if [ $(id -u) != 0 ]
then
    echo "You need to excuse this script with root privileges"
    read -p "Press Enter key to exit"
    exit 1
fi
###########################
# UPDATE AND UPGRADE OS
###########################
echo '###########################'
echo '# UPDATE AND UPGRADE OS #'
echo '###########################'
sudo apt update && apt upgrade -y &&
###########################
# install python 3 & pip
###########################
echo '###########################'
echo '# INSTALL PYTHON3 & PIP #'
echo '###########################'

sudo apt install -y python3 python3-pip python3-venv  &&
# curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
# python3 get-pip.py
pip3 --version
echo "Install successful Python3 and pip"
# if [ $? ]
# then
# echo "Error install pip, you need to install 'pip' manually!"
# fi
# install requirements.txt 
pip3 install -r requirements.txt &&
# if [ $? ]
# then
# echo "Check install requirement file - may be install manually"
# fi


########################
# install Nginx
########################
echo '###########################'
echo '# INSTALL NGINX #'
echo '###########################'
sudo apt install -y nginx &&
# if [ $(systemctl status nginx) != 0 ]
# then
#     echo "S"
#     read -p "Press Enter key to exit"
#     exit 1
# fi
systemctl enable nginx &&
systemctl start nginx &&
echo "Install Nginx server successfully"

########################
# install Gunicorn
########################
echo '###########################'
echo '# INSTALL GUNICORN #'
echo '###########################'
sudo apt install -y python3-gunicorn &&
echo "Install Gunicorn successfully"

########################
# install mysql
########################

echo '###########################'
echo '# INSTALL MYSQL #'
echo '###########################'
sudo apt install -y mariadb-server &&
# config MySQL
sudo mysql_secure_installation &&
#
sudo systemctl start mysql &&
# create database
data1="data_bot"
sudo mysql -e "CREATE DATABASE $data1" &&
echo "########################"
echo "Dump database from file"
sudo mysql -p $data1 < data1.sql &&
echo "#############################"
echo "Create new user and password"
# enter name user and password
echo "Enter user name for DataBase MySQL : "
read userDB
echo "Enter password"
echo "Password must to have Upper letter, 
Lower letter, number, symbol and at least 8 characters: "
read passDB
# create user in database
sudo mysql -e "CREATE USER IF NOT EXISTS '$userDB'@'localhost' IDENTIFIED BY '$passDB'";
sudo mysql -e "GRANT ALL PRIVILEGES ON *.* TO '$userDB'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"
# sudo systemctl start mysql
# restart mysql
sudo systemctl restart mysql &&
echo "Install successful MySQL"
# write username and password to the envirement file
echo "userDB='$userDB'">>.env.tmp
echo "passDB='$passDB'">>.env.tmp
host1="localhost" &&
echo "hostDB='$host1'">>.env.tmp &&
echo "dataDB='$data1'">>.env.tmp &&
########################
# CONFIG TO USE UPS
########################
echo '###########################'
echo '# CONFIG TO USE UPS #'
echo '###########################'
sudo apt-get install smbus python3-dev &&
sudo apt-get install i2c-tools &&
# automatic launch I2C when restart
sudo echo 'i2c-dev'>>/etc/modules &&
# add user www-data to run I2C as administrator
sudo adduser www-data i2c &&
########################
# CONFIG TO USE USB MODEM
########################
echo '###########################'
echo '# CONFIG TO USE USB MODEM #'
echo '###########################'
# install driver
sudo apt-get install ppp usb-modeswitch
# add file to OS automatic recognize that usb-modem is a modem
# delete last line
sed '${/modeswitch_rules_end/d;}' /lib/udev/rules.d/40-usb_modeswitch.rules
# add in the last of the file 2 lines
echo "# Huawei E353/E3131">>/lib/udev/rules.d/40-usb_modeswitch.rules
echo "ATTR{idVendor}==\"12d1\", ATTR{idProduct}==\"1f01\", RUN +=\"usb_modeswitch '%b/%k'\"">>/lib/udev/rules.d/40-usb_modeswitch.rules
# config network
echo 'auto eth0'>>/etc/network/interfaces 
echo 'allow-hotplug eth0'>>/etc/network/interfaces 
echo 'iface eth0 inet dhcp'>>/etc/network/interfaces 
echo 'metric 500'>>/etc/network/interfaces 

sed '${/managed/d;}' /etc/NetworkManager/NetworkManager.conf 
echo 'managed=false'>>/etc/NetworkManager/NetworkManager.conf

########################
########################
# copy all file to target forder
echo "Copy file....................................."
# create folder to target /var/www
mkdir /var/www/tele_bot
#copy
cp -av . /var/www/tele_bot/ && cd /var/www/tele_bot

# require user to register a telegram bot and save the token
echo "########################################################"
echo "You need to create a new telegram bot and save the TOKEN"
echo "Please enter Telegram-bot TOKEN:"
while [ true ]
do 
read token
echo "Check TOKEN.................."
curl "https://api.telegram.org/bot$token/getUpdates" > respond
if grep -q true respond
then
echo "It is a correct Token"
echo "TOKEN_TL='$token'">>.env.tmp  &&
break
else
echo -e "\n It is not a correct Token, please enter again:"
fi
done
rm respond
rm data1.sql
# rename envirement file
rm .env &&
mv .env.tmp .env &&
rm install.sh
########################
########################
# create virtual envirement to excute nginx
python3 -m venv venv
sudo apt-get install -y libxml2-dev libxslt-dev python3-dev &&
sudo apt install python3-lxml &&
/var/www/tele_bot/venv/bin/pip install -r requirements.txt
# Configuring Nginx
# copy to folder /etc/nginx/sites-available
sudo cp -av /var/www/tele_bot/sites-available/telebot_web /etc/nginx/sites-available &&
sudo rm -r /var/www/tele_bot/sites-available &&
# Link the file to the sites-enabled directory to enable Nginx server block
sudo ln -s /etc/nginx/sites-available/telebot_web /etc/nginx/sites-enabled
#
echo "Test Nginx syntax errors............."
sudo nginx -t
# copy file from folder /systemd to /etc/systemd/system/
sudo cp -av /var/www/tele_bot/systemd/. /etc/systemd/system/ &&
sudo rm -r /var/www/tele_bot/systemd &&
# enable 4 service => auto start
sudo systemctl enable telebot_ups &&
sudo systemctl enable telebot_kamera &&
sudo systemctl enable telebot_telegram &&
sudo systemctl enable telebot_web &&
# start 4 service
# sudo systemctl start telebot_ups &&
# sudo systemctl start telebot_kamera &&
# sudo systemctl start telebot_telegram &&
# sudo systemctl start telebot_web &&
# notification success
echo "Install telegrambot for climate camera successfully, reboot now!"
sudo reboot
exit 0