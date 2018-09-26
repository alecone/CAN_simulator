from pypl import ArtPyPlCommand, ArtPyPlClient, CanMessage
from threading import Thread
import signal, sys, time, struct
from time import sleep
import datetime     # Used for time e date
from messages_db import *

def convertToBCD(value):
    cnt = 0
    bcdValue = 0
    for digit in str(value)[::-1]:
            bcdValue += (int(digit) << (cnt*4)) & 0xFFFF
            cnt += 1
    return bcdValue


def datePayloadTIME_E_DATE():
    # get actual time
    now = datetime.datetime.now()
    payload = bytearray(0)

    # Convert to BCD
    hour = convertToBCD(now.hour)   # Raw conversion to BCD
    minute = convertToBCD(now.minute)   # Raw conversion to BCD
    day = convertToBCD(now.day)   # Raw conversion to BCD
    month = convertToBCD(now.month)   # Raw conversion to BCD
    year = convertToBCD(now.year)   # Raw conversion to BCD
    payload.extend(struct.pack(">B", hour))
    payload.extend(struct.pack(">B", minute))
    payload.extend(struct.pack(">B", day))
    payload.extend(struct.pack(">B", month))
    payload.extend(struct.pack(">B", ((year&0xFF00) >> 8) & 0xFF))
    payload.extend(struct.pack(">B", (year & 0xFF)))

    # print("TIME E DATE",payload)
    return payload

def set_manubrio(ArtPyPlClient):
    key = compose_STATUS_NBC(KeySts=4)
    stay_active = compose_NWM_NBC(SystemCommand=2)
    while GO_thread:
        ArtPyPlClient.sendCommand(key)
        sleep(0.250)
        ArtPyPlClient.sendCommand(key)
        sleep(0.250)
        ArtPyPlClient.sendCommand(key)
        sleep(0.250)
        ArtPyPlClient.sendCommand(key)
        sleep(0.250)
        ArtPyPlClient.sendCommand(stay_active)

def MainMenu():
    print("1. Test a signal")
    print("q. Quit")

if __name__ == "__main__":
    GO_thread = True
    # Create an instance of the Client, in order to connect to the ArtCanalyzer(acting as a server in our case)
    a = ArtPyPlClient()
    # Create thread for letting manubrio ON
    manubrioThread = Thread(target=set_manubrio, args=(a,))
    # Try to connect
    while not a.connect():
        # Rest one second then try again!
        time.sleep(1)
        continue
    # At this point, we got a connection!
    # Launch manubrioThread
    # manubrioThread.start()
    # sleep(2)
    # Until we are connected, let's do something
    while True:
        MainMenu()
        command = input(" >")
        if command == 'q':
            print('Exit...')
            break
        elif command == '1':
            gest = compose_NVO_STATUS_TOUCHPAD(GestureType=3, FingerPresent=1, GestureStep=5)
            for i in range(10):
                a.sendCommand(gest)
                sleep(1)
            print(gest)
            sleep(5)
            print('Scroll Left')
            gest = compose_NVO_STATUS_TOUCHPAD(GestureType=4, FingerPresent=1, GestureStep=5)
            for i in range(10):
                a.sendCommand(gest)
                sleep(1)
            print(gest)
            sleep(5)
            print('Scroll Right')
        else:
            print('Unknown command')
    GO_thread = False
    # manubrioThread.join()
    a.forceCloseConn()
    a.endComm()

    # while a.isConnected:
    #     if a.rxCANAvailable():
    #         # We got a pending message. Print it into shell
    #         print(a.getCANMessage())
    #     # Rest for one second
    #     time.sleep(1)
    # a.endComm()
