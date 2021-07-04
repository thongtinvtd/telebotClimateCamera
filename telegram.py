from comFunctions import *
from time import sleep
import time
import requests
import json
import re

from connectSQL import *
from config import *
listchatid_sended = []

# --------------------------------------------------------------------------


def parse_message(message):
    if message:
        chat_id = message['message']['chat']['id']
        txt = message['message']['text']
        chat_user = message['message']['chat']['first_name']
        update_id = message['update_id']
        update_time = message['message']['date']
        # create a pattern to check message input
        pattern = r'/[a-zA-Z]{2,11}'
        ticker = re.findall(pattern, txt)
        # check pattern
        if ticker:
            command = ticker[0][1:]  # delete symbol '/'
        else:
            command = ''
        return update_id, chat_id, chat_user, command, update_time

# --------------------------------------------------------


def get_updates():
    try:
        url = f'https://api.telegram.org/bot{TOKEN_TL}/getUpdates'
        r = requests.post(url)
        r_json = json.loads(r.text)
        print(r_json)
        if r_json['result']:
            last_msg = r_json['result'][len(r_json['result'])-1]
            return last_msg
        return ""
    except Exception as e:
        print('Error get updates from telegram:',e)
        return ''
# ---------------------------Telegram API-------------------------------------
paraTable = []
# -----------------------------------------------------------------------


def p_telegram():
    # name admin  to "2" in the database
    chat_id_admin = get_list_receive_id([2,])
    print('chat_id_admin',chat_id_admin)
    update_id_readed = 0
    while True:
        # check status bot
        isWorking = getStatusBot()
        print("getstatusbot : ", isWorking)
        # print(time.time())
        # check connect
        last_msg = get_updates()
        if parse_message(last_msg):
            # get chat id, user name, command ... from last message
            update_id, chat_id, chat_user, command, update_time = parse_message(
                last_msg)
            print(parse_message(last_msg))
            chat_id = str(chat_id)
            # check time : if time of sending message does not equal real time -> not send message
            # neu thoi gian nhan tin nhan va thoi gian thuc te khong bang nhau thi khong gui tin nua
            # kiem tra so giay tu 01-01-1970 tu telegram va he thong
            ticks = round(time.time())
            if (ticks - update_time) < TIME_OFFSET:
                print(update_id_readed)
                print(time.time())

                if update_id != update_id_readed:
                    # if the message was readed -> do nothing
                    # neu message da doc roi thi ko lam gi ca
                    update_id_readed = update_id
                    # print(chat_id, chat_user, command, update_id)
                    # print(time.time())

                    list_commands = ('start', 'stop', 'help',
                                     'status', 'quit', 'ups')

                    if command not in list_commands:
                        send_message(chat_id, 'Wrong command')

                    elif not isWorking:  # if bot disable send other message
                        mes_send = mes_status_dis
                        send_message(chat_id, mes_send)

                    elif command == 'start':
                        write_user(chat_id, chat_user, 0)
                        mes_send = mes_start
                        send_message(chat_id, mes_send)
                        # message to admin to ask to add an user to list people, these  will receive notification
                        mes_send = mes_admin.format(chat_user, chat_id)
                        if chat_id_admin:
                            send_many_message(chat_id_admin, mes_send)

                    elif command == 'status':
                        # check user has permission or no
                        # check time permission
                        if checkPermissionUser(chat_id):
                            # request list value will on the message
                            l_varReq = []
                            sql0 = 'SELECT parameter,on_message FROM para_manager;'
                            rows0 = sqlselect(sql0)
                            if len(rows0) > 0:
                                for i in rows0:
                                    if i[1]:
                                        l_varReq.append(i[0])
                            # using list para to request values
                            paraTable.clear()
                            parameterList = "`,`".join(l_varReq)
                            sql2 = f"SELECT `{parameterList}` FROM climate WHERE id = (SELECT MAX(id) FROM climate);"
                            rows2 = sqlselect(sql2)
                            varPara = ''
                            if rows2:
                                for i in range(len(rows2[0])):
                                    varPara = rows2[0][i]
                                    # add symbol to temperature and humidity
                                    if l_varReq[i][:11] == 'Temperature':
                                        varPara = str(varPara) + ' *C'
                                    if l_varReq[i][:8] == 'Humidity':
                                        varPara = str(varPara) + ' %'
                                    # convert time values
                                    if l_varReq[i][-4:] == 'Time':
                                        varPara = convSec2HMS(varPara)
                                    # get status from camera
                                    if l_varReq[i] == 'Status':
                                        varPara = getProgStatus(varPara)
                                    paraTable.append(
                                        [l_varReq[i], varPara]
                                    )

                            # message for sending to user
                            mes_status_para_1 = mes_status_para.format(
                                paraTable[0][1], paraTable[1][1])
                            mes_status_para_2 = ''
                            # remove the first two parameters
                            del paraTable[0:2]
                            for i in paraTable:
                                mes_status_para_2 += '  - {} : {} \n'.format(
                                    i[0], i[1])

                            mes_status_bot = mes_status_para_1 + mes_status_para_2

                            # send_message(chat_id, mes_status_bot )
                        else:
                            mes_status_bot = mes_not_permi
                            # config.send_message(chat_id,mes_status_bot)
                        mes_send = mes_status_bot
                        send_message(chat_id, mes_send)
                    # handle command stop
                    elif command == 'stop':
                        remove_user(chat_id)
                        mes_send = mes_stop
                        send_message(chat_id, mes_send)

                    # handle command help
                    elif command == 'help':
                        mes_send = mes_help
                        send_message(chat_id, mes_send)
                        # return Response('ok', status=200)
                    elif command == 'quit':
                        send_message(chat_id, "Deleting the warning ...")
                        req = None
                        while (not req) or (req.status_code != 200):
                            try:
                                req = requests.get(
                                    "http://192.168.3.16/simpac/warning/c3k_warn.plc?tag_value=1&tag_name=HMI.MS_QuitAll")
                            except Exception as e:
                                print("Error delete warning:", e)
                                sleep(0.1)

                        send_message(
                            chat_id, 'I deleted the warning ! \nNow camera have no warning.')
                    elif command == 'ups':
                        if checkPermissionUser(chat_id):
                            voltage, capacity, onAdapter = getInfoUPSfromDB()
                            if onAdapter:
                                mes_onAdapter = "Power Adapter Plug In"
                            else:
                                mes_onAdapter = "Power Adapter Unplug"
                            mes_send = mes_UPS.format(
                                voltage, capacity, mes_onAdapter)
                        else:
                            mes_send = mes_not_permi
                        send_message(chat_id, mes_send)

        sleep(0.5)


p_telegram()
