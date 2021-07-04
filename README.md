# telebotClimateCamera
## connect UPS and USB modem
## create a telegram bot and save the TOKEN
## copy all files to the server (anywhere)
## setting to enable i2c in armbian-config
## launch command:
sudo bash install.sh
## enter TOKEN, user name and password for DB MySQL (any name)
## wait for server restart and check by command:
sudo systemctl status telebot_telegram
sudo systemctl status telebot_ups
sudo systemctl status telebot_kamera
sudo systemctl status telebot_web
