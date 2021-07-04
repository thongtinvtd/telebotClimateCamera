import requests
import lxml.html as html
from time import sleep

from config import *
from connectSQL import *
from comFunctions import *
#-------------------------------------------------------------------------------        
def get_data():
    try:           
        #thu tuc truy cap database mysql lay parameter
        # sql0="select * from climate where id=(select max(id) from climate);"
        sql0="SELECT id,time_request, \
                temperature, \
                humidity, \
                temperature_set, \
                humidity_set, \
                `Profile No.`, \
                `Profile Name`, \
                `Profile Cycles`, \
                `Active Cycles`, \
                `Total Loops`, \
                `Act Loops`, \
                `Segment`, \
                `Active Time`, \
                `Profile Time`, \
                `Total Time`, \
                `Segment Type`, \
                `Segment Total Time`, \
                `Segment Remain Time`, \
                `Status` FROM climate WHERE id=(SELECT MAX(id) FROM climate);"
        curs = conn.cursor()
        curs.execute(sql0)
        #tra ve du lieu
        data = curs.fetchone()
    except Exception as e:
        print('Error : ',e)
    # curs.close()
    return data
#------------------------------------------------------------------
def getParaFromKamera_1():
    r = requests.get(url_info) #Tao request de lay ve trang web so lieu
    #noi dung dc chua trong content_html
    tree = html.fromstring(r.content)
    # tim trong chuoi table 
    trs_odd = tree.cssselect('tr.col_odd')
    if trs_odd :
        tds_of_first_row = trs_odd[0].cssselect('td') #
        if tds_of_first_row:
            actual_temperature = tds_of_first_row[3].text
            setpoint_temperature = tds_of_first_row[4].text

    trs_even = tree.cssselect('tr.col_even')
    if trs_even :
        tds_of_second_row = trs_even[0].cssselect('td')
        if tds_of_second_row:
            actual_humidity   = tds_of_second_row[3].text
            setpoint_humidity = tds_of_second_row[4].text
    return actual_temperature,setpoint_temperature,actual_humidity, setpoint_humidity
#-------------------------------------------------------------------------------
def getParaFromKamera_2():
    BASE = "http://192.168.3.16/simpac/macros/getHMIvar.plc?plc_var_name=HMI.Prog.%s"
    urls = [
        'ProfileNo', 'ProfileName', 'ProfileCycles', 'ActiveCycles', 'TotalLoops', 
        'ActLoops', 'Segment', 'ActiveTime', 'ProfileTime', 'TotalTime',
        'SegmentType', 'SegmentTotalTime', 'SegmentRemainTime', 'Status'
    ]
    da_l = list()
    for i in urls:
        val_data = requests.get( BASE % i ).text.strip()
        da_l.append(val_data)
        sleep(0.1)
    return da_l
#-------------------------------------------------------------------------------
def checkErrorCamera():
    # get parameters in the page Error
    r = requests.get(url_warn, timeout=TIMEOUT)
    tree = html.fromstring(r.content)
    tbody = tree.cssselect('tr.col_warn_odd') #--> tbody table notification.
    if tbody :
        td1 = tbody[0].cssselect('td')  #--> row 2 has type error
        error_number = td1[0].text_content()
        error_text   = td1[1].text_content()
        error_active = td1[2].text_content()
        error_type   = td1[3].text_content()

        if error_type == '1':
            error_type = 'Alarm'
        elif error_type == '2':
            error_type = 'Warning'
        else :
            error_type = 'Info'
        print(error_text, error_number, error_type)
        return error_text, error_number, error_type

    return None

#----------------------------------------------------------------------------------  
#------------------------------------------------------------------------------------
def checkConnectKamera():
    req = None
    isSendedNotConnect = False
    # loop to check connect
    # if connected to kamera => break the loop
    while (not req) or (req.status_code != 200):
        try:
            req = requests.get(url_warn, timeout=TIMEOUT)
            print("request to camera")
        except Exception as e:
            print('Connect timeout, kamera is not working or disconnection!')
            if not isSendedNotConnect:
                send_many_message(listUserPermission(),mes_lost)
                isSendedNotConnect = True
            # Stop a bit to avoid kamera overload
            sleep(0.2)
    if isSendedNotConnect:
        send_many_message(listUserPermission(),'Connect to kamera successfully !')
        isSendedNotConnect = False


#----------------------------------------------------------------------
def saveDataToServer(isWorking,TIME_REQ):
    global type_send
    #chu ky ktra 
    TIME_REQ = float(TIME_REQ)
    # neu danh sach canh bao co ton tai it nhat 1 nguoi thi chuong trinh hoat dong con neu ko co ai thi dung hoat dong theo doi camera, 
    # Если в список есть хотя бы 1 человек
    get_list_receive_id_0 = get_list_receive_id(type_send)
    
    if get_list_receive_id_0 and isWorking :
        actual_temperature,setpoint_temperature,actual_humidity,setpoint_humidity = getParaFromKamera_1()
        sleep(TIME_REQ)
        da_l = getParaFromKamera_2()
        sleep(TIME_REQ)

        name_l = [
            'Temperature' , 'Humidity' , 'Temperature_set' , 'Humidity_set' ,
            'Profile No.' , 'Profile Name' , 'Profile Cycles' , 'Active Cycles' , 
            'Total Loops' , 'Act Loops' , 'Segment' , 'Active Time' , 'Profile Time' , 
            'Total Time' , 'Segment Type' , 'Segment Total Time' , 'Segment Remain Time' , 'Status' 
        ]

        try:
            sql1= "INSERT INTO climate(`%s`) VALUES (%s, %s, %s, %s,'%s') ;" % (
                "`,`".join(name_l), actual_temperature.strip(), actual_humidity.strip(),
                setpoint_temperature.strip(), setpoint_humidity.strip(),
                "','".join(da_l)
            )
            # print(sql1)
            curs.execute(sql1)
            conn.commit()
        except Exception as e:
            print('Error : ',e)

#--------------------------------------------------------------------------------
def p_request_para():
    isSendedError = False
    while True:
        isWorking = getStatusBot()
        TIME_CYCLE, TIME_REQ = get_time_para()
        #check connect to kamera
        checkConnectKamera()
        #check error kamera
        listNotice = listUserPermission()
        if checkErrorCamera() and (not isSendedError):
            # error_text, error_number, error_type = checkErrorCamera()
            isSendedError = True
            send_many_message(listNotice,mes_error.format(checkErrorCamera()))
        else:
            isSendedError = False
        # Write to DB
        saveDataToServer(isWorking,TIME_REQ)
        sleep(TIME_CYCLE)

p_request_para()