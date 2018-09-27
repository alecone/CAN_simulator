import can
from utils import *
from threading import Thread
from time import sleep
from messages_db import *


def MainMenu():
    print("c.   Press Comfort button")
    print("b.   Press Back_MainMenu")
    print("m.   Change Manettino")
    print("s.   Press Source Button")
    print("mw.  Set Driver Wish")
    print("v.   Press Voice Recognition")
    print("d.   Press Declutter")
    print("p.   Press Phone Call button")
    print('lb   Long press on Back_MainMenu')
    print("SL.  Scroll Left")
    print("SR.  Scroll Right")
    print("SU.  Scroll Up")
    print("SD.  Scroll Down")
    print("PC.  Press Center\r\n")
    print("l. Signal Listener")
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
        elif command == 'c':
            print('Pressing confort')
            comfort(bus)
        elif command == 'b':
            print('Pressing back button')
            back(bus)
        elif command == 'm':
            print('Setting Manettino')
            for i in [3,1,2,3,4,5,3]:
                manettino(bus, i)
        elif command == 's':
            print("Prssing Source Button")
            source(bus)
        elif command == 'mw':
            print('Setting manettino wish')
            for i in [0,1,2,3,4,0]:
                driver_wish(bus, i)
        elif command == 'v':
            print("Pressing voice recognition")
            voice(bus)
        elif command == 'd':
            print('Pressing declutter')
            declutter(bus)
        elif command == 'p':
            print('Pressing phone call')
            phone(bus)
        elif command == 'lb':
            print('Long press back')
            long_press_menu(bus)
        elif command == 'SL':
            print('Scroll left')
            scroll_left(bus)
        elif command == 'SR':
            print('Scroll right')
            scroll_right(bus)
        elif command == 'SU':
            scroll_up(bus)
        elif command == 'SD':
            scroll_down(bus)
        elif command == 'PC':
            press_center(bus)


        elif command == 'l':
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
