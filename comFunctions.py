from config import *

# convert format time and status in the values from kamera
def convSec2HMS(secondVar):
    # if int(secondVar) is int :
    h = (int(float(secondVar) // 3600))
    m = int(float(secondVar)) - h*3600
    m = m // 60
    s = int(float(secondVar)) - h*3600 - m * 60
    timeStr = str(h) + 'h  ' + str(m) + 'm  ' + str(s) + 's '
    return timeStr
#--------------------------------------------------------------
def getProgStatus(val_Status):
    status_str = ''
    try:
        pgst = int(val_Status[3:],16)
    except Exception as e:
        print('Error:',e)
        return 'Error!'
    if pgst & 1 :
        status_str = 'running'
    if pgst & 2 :
        status_str = 'paused'
    if pgst & 4 :
        status_str = 'waiting'
    if pgst & 16 :
        status_str = 'waiting to start'
    return status_str
#-----------------------------------
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
