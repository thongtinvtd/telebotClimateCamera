#!/usr/bin/env python
# sudo apt-get update
# sudo apt-get install python-dev git
# git clone https://github.com/Jeremie-C/OrangePi.GPIO
# cd /OrangePi.GPIO
# sudo python setup.py install
import struct
import smbus
import sys
import OPi.GPIO as GPIO
from time import sleep

from comFunctions import *
from config import *
from connectSQL import *
def readVoltage(bus):
    # "This function returns as float the voltage from the Raspi UPS Hat via the
    # provided SMBus object"
    address = 0x36
    read = bus.read_word_data(address, 0X02)
    swapped = struct.unpack("<H", struct.pack(">H", read))[0]
    voltage = swapped * 1.25/1000/16
    return voltage

def readCapacity(bus):
# "This function returns as a float the remaining capacity of the battery connected
# to the Raspi UPS Hat via the provided SMBus object"
    address = 0x36
    read = bus.read_word_data(address, 0X04)
    swapped = struct.unpack("<H", struct.pack(">H", read))[0]
    capacity = swapped/256
    return capacity

def QuickStart(bus):
    address = 0x36
    bus.write_word_data(address, 0x06,0x4000)

def PowerOnReset(bus):
    address = 0x36
    bus.write_word_data(address, 0xfe,0x0054)

def initUPS():
    GPIO.setboard(GPIO.PCPCPLUS)    # Orange Pi PC board
    GPIO.setmode(GPIO.BOARD)        # set up BOARD BCM numbering
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(4,GPIO.IN)
    bus = smbus.SMBus(0) # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

    PowerOnReset(bus)
    QuickStart(bus)
    return bus

bus = initUPS()
#------------------------------------------------------------
def checkAdapter():
    if (GPIO.input(4) == GPIO.HIGH):
        return True
    else:
        return False
#----------------------------------------------------------------
def getInfoUPS(bus):
    voltageUPS = readVoltage(bus)
    voltageUPS = round(voltageUPS,2)
    capacityUPS = readCapacity(bus)
    capacityUPS = round(capacityUPS,1)
    onAdapter = checkAdapter()
    return voltageUPS,capacityUPS,onAdapter

#----------------------------------------------------------------
def writeUPS_DB(voltage,capacity,onAdapter):
    try:
        sql_power = 'INSERT INTO power_record(voltage,capacity,status) VALUES ({},{},{});'
        curs.execute(sql_power.format(voltage,capacity,onAdapter))
        conn.commit()
    except Exception as e:
        print('Error write to power_record:',e)
    return 0
#----------------------------------------------------------------------
def checkUPS():
    #check UPS
    # low battery => send 
    # power outage => send
    # global bus
    # TIME_CHECK_UPS = 0.5
    # voltage,capacity,onAdapter = getInfoUPS(bus)
    # writeUPS_DB(voltage,capacity,onAdapter)
    # if not onAdapter:
    #     return 1 # power off
    #     # pause to avoid flicker when connect to source
    #     sleep(1)
    #     # print(mes_UPS_powerOff,"+",isSended)
    #     if capacity < 10 :
    #         return 2 # power low
    #         print('Power low')
    # elif onAdapter :
    #     print("Power on!")
    #     return 0
    
    #check UPS
    # low battery => send 
    # power outage => send
    isSended = False
    TIME_CHECK_UPS = 0.5
    while True:
        voltage,capacity,onAdapter = getInfoUPS(bus)
        writeUPS_DB(voltage,capacity,onAdapter)
        listUser = listUserPermission()
        if (not onAdapter) and (not isSended):
            send_many_message(listUser, mes_UPS_powerOff)
            isSended = True
            # pause to avoid flicker when connect to source
            sleep(1)
            # print(mes_UPS_powerOff,"+",isSended)
            if capacity < 10 :
                send_many_message(listUser, mes_UPS_low)
                print(mes_UPS_low)
        elif onAdapter :
            print("Power on!")
            if isSended:
                send_many_message(listUser, mes_powerOn)
            isSended = False
        sleep(TIME_CHECK_UPS)

checkUPS()