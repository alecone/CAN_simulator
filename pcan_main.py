import can
from can import Message
from utils import *
from pypl import ArtPyPlCommand, ArtPyPlClient, CanMessage
from threading import Thread, Lock
import signal, sys, time, struct
from time import sleep
import datetime     # Used for time e date
from messages_db import *

##
## TODO: Implement the notifier in order to connect all received signals to propper actions
##       Further we can also use can.recv(timeout=None) in order to block and get first packets
##

##
## TODO: Implement Listeners if needed
##

# Filters
filters = [{"can_id": 0x021F, "can_mask": 0xFFFF, "extended": False},{"can_id": 0x03C4, "can_mask": 0xFFFF, "extended": False}]

def MainMenu():
    print("1. Test a signal")
    print("2. Map signal")
    print("q. Quit")

def set_manubrio(can_bus):
    payload_NBC = bytearray(8)
    compose_STATUS_NBC(payload_NBC, CeilingLightSts=2, InternalLightSts=1, InternalBacklightStsKeyOff=1, KeySts=key_sts)
    key = can_pack(BH['STATUS_NBC'][0], BH['STATUS_NBC'][1], payload_NBC)
    payload_NWM_NBC = bytearray(6)
    compose_NWM_NBC(payload_NWM_NBC, SystemCommand=2, ActiveLoadMaster=1)
    stay_active = can_pack(BH['NWM_NBC'][0], BH['NWM_NBC'][1], payload_NWM_NBC)
    while  GO_thread:
        if change_key_sts:
            compose_STATUS_NBC(payload_NBC, KeySts=key_sts)
            key = can_pack(BH['STATUS_NBC'][0], BH['STATUS_NBC'][1], payload_NBC)
        can_bus.send(key)
        can_bus.send(stay_active)
        sleep(1)


if __name__ == "__main__":
    lock = Lock()
    payload_STATUS_NVO = bytearray(8)
    timeout_STATUS_NVO = 1
    payload_TOUCHPAD = bytearray(8)
    timeout_TOUCHPAD = 0.050
    GO_thread = True
    change_key_sts = False
    key_sts = 4 # ON
    # Try to connect
    try:
        ch = can.util.channel2int('PCAN_USBBUS1')
    except:
        raise ValueError('Channel specified Unknown')

    bus = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate='125000')
    manubrioThread = Thread(target=set_manubrio, args=(bus,))

    # Launch manubrioThread
    manubrioThread.start()
    sleep(2)
    # Until we are connected, let's do something
    while True:
        MainMenu()
        command = input(" >")
        if command == 'q':
            print('Exit...')
            break
        elif command == '1':
            print('Press confort')
            for i in [0, 1, 0]:
                pack = press_confort_button(payload_STATUS_NVO, i)
                bus.send(pack)
                print(pack)
                sleep(timeout_STATUS_NVO)
        elif command =='2':
            print('Monitor')
            # listner_buttons = Listener(bus, id=0x3C4, dlc=8)
            listener_touchpad= Listener(bus, id=0x21F, dlc=8)
            sleep(2)
            print('Swipe left')
            sleep(5)
            print('Swipe right')
            sleep(5)
            listener_touchpad.stop()
        else:
            print('Unknown command')
    GO_thread = False
    manubrioThread.join()
    bus.shutdown()
