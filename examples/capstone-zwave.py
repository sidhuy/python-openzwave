#Name: Yuvraj Singh Sidhu
#File: capstone-zwave.py
#Purpose: Take a command from the user to turn on/off a zwave compatible bulb.  This project to be completed for Fall 2016 Wireless Assisitive Technology ZWave subsystem.


import logging
import sys, os

#logging.getLogger('openzwave').addHandler(logging.NullHandler())
#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('openzwave')

import openzwave
from openzwave.node import ZWaveNode
from openzwave.command import ZWaveNodeSwitch
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
import time

device="/dev/ttyACM0"
log="None"
sniff=300.0

#Configure ZWave Manager options (taken from /examples/hello_world.py)
options = ZWaveOption(device, \
  config_path="../openzwave/config", \
  user_path=".", cmd_line="")
options.set_log_file("OZW_Log.log")
options.set_append_log_file(False)
options.set_console_output(False)
options.set_save_log_level(log)
options.set_logging(True)
options.lock()

#Use network class to create an object
network = ZWaveNetwork(options, autostart=False)
command = ZWaveNodeSwitch()

network.start()
        
#Start up the ZWave network (taken from /examples/hello_world.py)
print("Network to start ")
for i in range(0,90):
    if network.state>=network.STATE_READY:
        print("ZWave Network Ready")
        break
    else:
        sys.stdout.write("*")
        sys.stdout.flush()
        time.sleep(0.5)

tmp_off = 0
tmp_on = 0
flag = True

while(flag):
    cmd = raw_input("Please enter command. \n")
    cmd = cmd.upper()
    cmd = cmd.replace('"', "")
    if (cmd == "ON" and tmp_on == 0):#command.get_switch_all_state(1) == False):
        print("Turn bulb on")
        network.switch_all(True)
        tmp_on = 1
        tmp_off = 0
    elif(cmd == "OFF" and tmp_off == 0):#command.get_switch_state(2) == True):
        print("Turn bulb off")
        network.switch_all(False)
        tmp_off = 1
        tmp_on = 0
    elif(cmd =="ON" and tmp_on > 0):#command.get_switch_state(2) == True):
        print("Bulb is already on")
        tmp_on = 0
    elif(cmd =="OFF" and tmp_off > 0):#command.get_switch_state(2) == False):
        print("Bulb is already off")
        tmp_off = 0
    elif(cmd == "CTRL-C"):
        flag = False
    else:
        print("Unknown Command")

print("Network to end")
network.stop()
