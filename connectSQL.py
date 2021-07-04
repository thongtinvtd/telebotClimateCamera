import mysql.connector
from datetime import datetime
import requests
from time import sleep

from config import *
#------------connect to DB-----------------------------------
conn = mysql.connector.connect(
    host=hostDB,
    user=userDB,
    password=passDB,
    database=dataDB
)
curs = conn.cursor()
conn.time_zone = "+03:00"
print("Connect DB successful!")
# --------------------------------------------------------------


def get_list_receive_id(type_user):
    try:
        type_user_permission = ''
        for i in type_user:
            type_user_permission += f'"{i}",'
        type_user_permission = type_user_permission[:-1]
        sql3 = f"SELECT user_id FROM alert_list WHERE permission IN ({type_user_permission});"
        rows = sqlselect(sql3)
        listchatid = []
        # rows = (('1029731812',), ('251290036',), ('1343733841',), ('325253745',))
        # using function for to get the element
        if len(rows):
            for i in rows:
                listchatid.append(i[0])
        return listchatid
    except Exception as e:
        print('Error get list id: ', e)
        return ''
# --------------------------------------------------------------


def sqlselect(sql=str):
    global conn
    try:
        conn = mysql.connector.connect(
            host=hostDB,
            user=userDB,
            password=passDB,
            database=dataDB
            )
        conn.time_zone = "+03:00"
        curs = conn.cursor()
        curs.execute(sql)
        rows = curs.fetchall()
        # print(rows)
        return rows
    except Exception as e:
        print("Error sqlselect: ", sql)
        return ''
# ----------------------get status bot -------------------


def getStatusBot():
    try:
        sql_dis = "SELECT status FROM admin_manager WHERE user_name = 'admin' ;"
        rows_status = sqlselect(sql_dis)
        if rows_status:
            if rows_status[0][0]:
                return True
            else:
                return False
    except Exception as e:
        print("Get status failed", e)
        return ''

def write_user(chat_id, chat_user, permission):
    try:
        sql2 = "SELECT COUNT(*) FROM alert_list WHERE user_id={};".format(chat_id)
        curs = conn.cursor()
        curs.execute(sql2)
        rows = curs.fetchone()
        if rows and rows[0] > 0:
            print("User has already existed !")
        else:
            sql1 = "INSERT INTO alert_list(user_id, user_name, permission, expiration) VALUES ({0},\'{1}\',\'{2}\',current_timestamp());".format(
                chat_id, chat_user, permission
            )
            # print(sql1)
            curs.execute(sql1)
            conn.commit()
    except Exception as e:
        print('Error write user: ', e)
        return ''
# ----------------------------------------------------------------------


def remove_user(chat_id):
    global conn
    try:
        conn = mysql.connector.connect(
            host=hostDB,
            user=userDB,
            password=passDB,
            database=dataDB
            )
        sql1 = "DELETE FROM alert_list WHERE user_id={};".format(chat_id)
        curs = conn.cursor()
        curs.execute(sql1)
        conn.commit()
    except Exception as e:
        print('Error remove user: ', e)
        return ''
# -----------------------------------------------------------------
# --------------------------------------------------------------------


def check_time_permission(chat_id):
    try:
        sql_checktime = "SELECT expiration FROM alert_list WHERE user_id ={};".format(
            chat_id)
        rows = sqlselect(sql_checktime)
        # print("rows: -------- ", rows[0][0])
        if len(rows):
            if rows[0][0] > datetime.now():
                return True
            else:
                return False
    except Exception as e:
        print("Check time permission failed - ", e)
        return ''
# --------------------------------------------------------------------------------------


def get_time_para():
    try:
        global conn
        sql0 = "SELECT * FROM para_manager WHERE parameter in ('Time_cycle', 'Time_req') ;"
        curs = conn.cursor()
        curs.execute(sql0)
        rows = curs.fetchall()
        TIME_CYCLE = 0
        TIME_REQ = 0
        if len(rows) > 0:
            # time between two circles
            TIME_CYCLE = rows[0][3]
            # time between two requests to web server kamera
            TIME_REQ = rows[1][3]
        TIME_CYCLE = float(TIME_CYCLE)
        TIME_REQ = float(TIME_REQ)
        return TIME_CYCLE, TIME_REQ
    except Exception as e:
        print("Error get time para: ", e)
        return ''
# ---------------------------------------------------------------------------


def getInfoUPSfromDB():
    try:
        sqlUPS = 'SELECT * FROM power_record WHERE id = (SELECT MAX(id) FROM power_record);'
        dataUPS = sqlselect(sqlUPS)
        if len(dataUPS[0]):
            voltage = dataUPS[0][2]
            capacity = dataUPS[0][3]
            status = dataUPS[0][4]
            return voltage, capacity, status
        return None
    except Exception as e:
        print('Error get Info UPS from DB:', e)
        return ''
#-------------------------------------------------------------------
def checkPermissionUser(chat_id):
    #check permission #check time
    if chat_id in listUserPermission():
        return True
    else:
        return False
#----------------------------------------------------------------------
def listUserPermission():
    global type_send
    list_user = get_list_receive_id(type_send)
    list_user_permission=[]
    for i in list_user:
        if check_time_permission(i):
            list_user_permission.append(i)
    return list_user_permission

# ------------------------------------------------------------------
def send_message(chat_id,text='hello'):
    url = f"https://api.telegram.org/bot{TOKEN_TL}/sendMessage"
    payload = {'chat_id':chat_id,'text':text}
    r = requests.post(url,json=payload)
    return r
#---------------------------------------------------------------------------------
def send_many_message(list_user = [], mess='') : 
    # listchatid = get_list_receive_id(list_user_type)
    list_user_sended = []
    for chat_id in list_user:
        send_message(chat_id, mess) #--> gui message cho ng dung
        list_user_sended.append(chat_id)
        sleep(0.1)
    print(list_user_sended)
#------------------------------------------------------------------------
