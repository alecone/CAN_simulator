from pypl import ArtPyPlCommand, ArtPyPlClient, CanMessage

import threading
import signal, sys, time, struct

import datetime     # Used for time e date


# CUSTOM ROUTINES
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


if __name__ == "__main__":
    # Create an instance of the Client, in order to connect to the ArtCanalyzer(acting as a server in our case)
    a = ArtPyPlClient()
    # Try to connect
    while not a.connect():
        # Rest one second then try again!
        time.sleep(1)
        continue
    # At this point, we got a connection!
    # Following line will call the forceCloseConn method to close the connection after 10 seconds.
    threading.Timer(100.0, a.forceCloseConn).start()
    # Until we are connected, let's do something
    while a.isConnected:
        # Create packet. It could contain some arguments, but its not important right now.
        cPkt = ArtPyPlCommand()
        # Populate Payload of the CAN message
        canPayload = datePayloadTIME_E_DATE()
        # Create PyPlCommand from CAN data
        cPkt.packetFromCanData(1, 0x683, 6,  canPayload)
        # Send Packet!
        a.sendCommand(cPkt)
        # Lets see if we got some packets back from ArtCanalyzer!
        if a.rxCANAvailable():
            # We got a pending message. Print it into shell
            print(a.getCANMessage())
        # Rest for one second
        time.sleep(1)
    a.endComm()
