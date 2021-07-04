from dotenv import load_dotenv
import os

load_dotenv()
#-------------------------------------------------------------------------      
TOKEN_TL = os.getenv('TOKEN_TL')
hostDB = os.getenv('hostDB')
userDB = os.getenv('userDB')
passDB = os.getenv('passDB')
dataDB = os.getenv('dataDB')

TIME_OFFSET = 20
TIMEOUT = 10
type_send = [1,2]

url_warn = 'http://192.168.3.16/simpac/warning/c3k_warn.plc'
url_info = 'http://192.168.3.16/simpac/info/c3k_frCVMV.plc'
url_auto = 'http://192.168.3.16/simpac/auto/c3k_auto.plc'

mes_error = 'Attention !\n \
Now the climate camera has a problem :  {} \
\n  Number:  {} \
\n  Type error :  {} \
\n  Quit notification: /quit'

mes_start = "'I have already remebered you, if admin alows, I will send alerts to you when the machine has errors'"
mes_status_dis = "Sorry, kamera is not working now !"
mes_help = "I have 5 commands:\n\b\b\b/start : Add you to the alert list.\n\
\b\b\b/stop : Delete you from the alert list.\n\
\b\b\b/status : Request the status\'s climate camera.\n\
\b\b\b/ups : Information about UPS.\n\
\b\b\b/help : About commands of the bot."
mes_stop = "I have already delete you from the alert list, I will not send alerts to you when the machine has errors"
mes_not_permi = "You don't have permission to request kamera information. Please contact admin"
mes_status_para = "This is parameters at the last time I checked kamera: \n\
  - Number of checked : {} times \n\
  - Last time checked : {}\n"
mes_admin = "  There is a person, who wants to receive \
    notification from the climate camera.\n - User_name : {} \n - Id : {}."
mes_UPS = "Status UPS: \n - Voltage: {}V\n - Capacity: {}%\n - {}"
mes_UPS_low = "The voltage or the capacity of the UPS is low!\n Need to charge now!\
    \n Check server power /ups"
mes_UPS_powerOff = "Power Adapter Unplug or Power outage!\n Check server power /ups "
mes_powerOn = "Power on!"
mes_lost = 'Connect timeout, kamera is not working or disconnection!'

