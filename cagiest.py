
#changed to include the two devices on the 1st Nov 2018
from time import sleep
from widgetlords.pi_spi import *
from widgetlords import *
import time
import sys
import datetime
import time
import serial
import requests
import json
import string
#import pymodbus3
#from pymodbus3.client.sync import ModbusSerialClient as ModbusClient #initialize a serial RTU client instance
import struct
import RPi.GPIO as GPIO
import os
#from pymodbus.constants import Defaults
#GPIO.cleanup()

#GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
PMP1=5
PMP2=6
PMP3=13
PMP4=19
FTPST=26
SPST=16
HGH1=20
HGH2=21

GPIO.setup(PMP1,GPIO.IN)
GPIO.setup(PMP2,GPIO.IN)
GPIO.setup(PMP3,GPIO.IN)
GPIO.setup(PMP4,GPIO.IN)
GPIO.setup(FTPST,GPIO.IN)
GPIO.setup(SPST,GPIO.IN)
GPIO.setup(HGH1,GPIO.IN)
GPIO.setup(HGH2,GPIO.IN)

with open('/home/arkbg/dev/config/BG_Config.json', 'r') as config_file:
    # Convert JSON to DICT
    config = json.load(config_file)
print (config['DEVICE_ID'])
# Build destination server path
SERVER_PATH = "http://" + config['SERVER_ADDR'] + config['SERVER_PATH']
print (SERVER_PATH)
payload = {}
index = 1
tofile=[]

fieldname = ["Station_ID",
             "Time",
             "level",
             "allpstop",
             "fpst",
             "spst",
             "thpst",
             "frpst",
             "fpsr",
             "spsr",
             "thpsr",
             "frpsr",
             "highl1",
             "rawval"]

payload[fieldname[0]] = config['DEVICE_ID']
print(datetime.datetime.now())
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y  %H:%M:%S')
payload[fieldname[1]] =st

init()
inputs = Mod8AI()

while True:
    for x in range(0, 1):
        adc=0
#        for y in range (0,100):
#         adc=adc+(inputs.read_single(0))
        adc=(inputs.read_single(0))
#        print(adc)
#        adc=adc/100
        print (adc)
        payload[fieldname[13]]=adc
        print ("next")
        print('{:.2f}'.format(adc))
        print (int(adc))
        curr = counts_to_value(adc,745,3723,4,20)
        print('{:.2f}'.format(curr))
        depth = float(((curr-4)/16)*6.9)
        depths=6.95-depth
        print(('{:.3f}'.format(depths)), "m")
        payload[fieldname[2]]=('{:.3f}'.format(depths))
        print(datetime.datetime.now())
        p1=GPIO.input(PMP1)
        p2=GPIO.input(PMP2)
        p3=GPIO.input(PMP3)
        p4=GPIO.input(PMP4)
        allstp=p1 | p2 | p3 | p4
#        print (allstp)
#Reading Pump 1
        fpst=0
        spst=0
        thpst=0
        ftpst=0
        fpsr=0
        spsr=0
        hgh1=0
        hgh2=0
        thpsr=0
        ftpsr=0

        adc=(inputs.read_single(1))
        print("First Pump Stop:",adc)
        if (adc>500):
          fpst=1

        adc=(inputs.read_single(2))
        print("Second Pump Stop:",adc)
        if (adc>500):
          spst=1

        adc=(inputs.read_single(3))
        print("Third Pump Stop:",adc)
        if (adc>500):
          thpst=1

        adc=(inputs.read_single(4))
        print("Fourth Pump Stop:",adc)
        if (adc>500):
          ftpst=1

        adc=(inputs.read_single(5))
        print("First Pump Start :",adc)
        if (adc>500):
          fpsr=1

        adc=(inputs.read_single(6))
        print("Second Pump Start:",adc)
        if (adc>500):
          spsr=1

        adc=(inputs.read_single(7))
        print("Third Pump:",adc)
        if (adc>500):
          thpsr=1

        ftpsr1=GPIO.input(FTPST)
        print("Fourth pump:",ftpsr1)
        if (ftpsr1):
          ftpsr=1 

        allstp=not (fpst|spst|thpst|ftpst)
        allstps=str(allstp)
        payload[fieldname[3]]=allstps
        payload[fieldname[4]]=fpst
        payload[fieldname[5]]=spst
        payload[fieldname[6]]=thpst
        payload[fieldname[7]]=ftpst
        payload[fieldname[8]]=fpsr
        payload[fieldname[9]]=spsr
        payload[fieldname[10]]=thpsr
        payload[fieldname[11]]=ftpsr

        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y  %H:%M:%S')
        payload[fieldname[1]] =st
        sleep(5)

    dev_json= json.dumps(payload, sort_keys=True)
    print (dev_json)

    tofile.append(payload)
    dir_name= "/home/arkbg/dev/data/"
    try:
        os.makedirs(dir_name)
    except OSError:
        if os.path.exists(dir_name):
                print (": Already directory exists")
        else:
                print (": Some system Error in creating directory")
    try:
        base_filename=time.strftime("%d%m%Y")
        abs_file_name=os.path.join(dir_name, base_filename + "." + "txt")
        f = open(abs_file_name, 'a')
        print(json.dumps(payload), end="", file=f)
        f.close()
    except Exception as e:
        print("type error: " + str(e))
        print("Error : File not written")
        pass

    try:
# Send JSON to server
        print ("Nothing")
        r1 = requests.put(SERVER_PATH, data=dev_json, timeout=1)
        print (r1.status_code)
    except Exception as e:
        print("type error: " + str(e))
        print("Server Comms Error")
        try:
                base_filename=time.strftime("%d%m%Y")
                abs_file_name=os.path.join(dir_name, base_filename + "ns." + "dat")
                f = open(abs_file_name, 'a')
                print(json.dumps(tofile), end="", file=f)
                f.close()
        except Exception as e:
                print("type error: " + str(e))
                print("Error : NS File not written")
                pass
        pass
    del tofile[:]



