import socket
import threading
import signal, sys, time
import struct

from multiprocessing import Queue
from queue import LifoQueue


crc_table = [0x00000000, 0x77073096, 0xEE0E612C, 0x990951BA, 0x076DC419, 0x706AF48F, 0xE963A535, 0x9E6495A3,
    0x0EDB8832, 0x79DCB8A4, 0xE0D5E91E, 0x97D2D988, 0x09B64C2B, 0x7EB17CBD, 0xE7B82D07, 0x90BF1D91,
    0x1DB71064, 0x6AB020F2, 0xF3B97148, 0x84BE41DE, 0x1ADAD47D, 0x6DDDE4EB, 0xF4D4B551, 0x83D385C7,
    0x136C9856, 0x646BA8C0, 0xFD62F97A, 0x8A65C9EC, 0x14015C4F, 0x63066CD9, 0xFA0F3D63, 0x8D080DF5,
    0x3B6E20C8, 0x4C69105E, 0xD56041E4, 0xA2677172, 0x3C03E4D1, 0x4B04D447, 0xD20D85FD, 0xA50AB56B,
    0x35B5A8FA, 0x42B2986C, 0xDBBBC9D6, 0xACBCF940, 0x32D86CE3, 0x45DF5C75, 0xDCD60DCF, 0xABD13D59,
    0x26D930AC, 0x51DE003A, 0xC8D75180, 0xBFD06116, 0x21B4F4B5, 0x56B3C423, 0xCFBA9599, 0xB8BDA50F,
    0x2802B89E, 0x5F058808, 0xC60CD9B2, 0xB10BE924, 0x2F6F7C87, 0x58684C11, 0xC1611DAB, 0xB6662D3D,
    0x76DC4190, 0x01DB7106, 0x98D220BC, 0xEFD5102A, 0x71B18589, 0x06B6B51F, 0x9FBFE4A5, 0xE8B8D433,
    0x7807C9A2, 0x0F00F934, 0x9609A88E, 0xE10E9818, 0x7F6A0DBB, 0x086D3D2D, 0x91646C97, 0xE6635C01,
    0x6B6B51F4, 0x1C6C6162, 0x856530D8, 0xF262004E, 0x6C0695ED, 0x1B01A57B, 0x8208F4C1, 0xF50FC457,
    0x65B0D9C6, 0x12B7E950, 0x8BBEB8EA, 0xFCB9887C, 0x62DD1DDF, 0x15DA2D49, 0x8CD37CF3, 0xFBD44C65,
    0x4DB26158, 0x3AB551CE, 0xA3BC0074, 0xD4BB30E2, 0x4ADFA541, 0x3DD895D7, 0xA4D1C46D, 0xD3D6F4FB,
    0x4369E96A, 0x346ED9FC, 0xAD678846, 0xDA60B8D0, 0x44042D73, 0x33031DE5, 0xAA0A4C5F, 0xDD0D7CC9,
    0x5005713C, 0x270241AA, 0xBE0B1010, 0xC90C2086, 0x5768B525, 0x206F85B3, 0xB966D409, 0xCE61E49F,
    0x5EDEF90E, 0x29D9C998, 0xB0D09822, 0xC7D7A8B4, 0x59B33D17, 0x2EB40D81, 0xB7BD5C3B, 0xC0BA6CAD,
    0xEDB88320, 0x9ABFB3B6, 0x03B6E20C, 0x74B1D29A, 0xEAD54739, 0x9DD277AF, 0x04DB2615, 0x73DC1683,
    0xE3630B12, 0x94643B84, 0x0D6D6A3E, 0x7A6A5AA8, 0xE40ECF0B, 0x9309FF9D, 0x0A00AE27, 0x7D079EB1,
    0xF00F9344, 0x8708A3D2, 0x1E01F268, 0x6906C2FE, 0xF762575D, 0x806567CB, 0x196C3671, 0x6E6B06E7,
    0xFED41B76, 0x89D32BE0, 0x10DA7A5A, 0x67DD4ACC, 0xF9B9DF6F, 0x8EBEEFF9, 0x17B7BE43, 0x60B08ED5,
    0xD6D6A3E8, 0xA1D1937E, 0x38D8C2C4, 0x4FDFF252, 0xD1BB67F1, 0xA6BC5767, 0x3FB506DD, 0x48B2364B,
    0xD80D2BDA, 0xAF0A1B4C, 0x36034AF6, 0x41047A60, 0xDF60EFC3, 0xA867DF55, 0x316E8EEF, 0x4669BE79,
    0xCB61B38C, 0xBC66831A, 0x256FD2A0, 0x5268E236, 0xCC0C7795, 0xBB0B4703, 0x220216B9, 0x5505262F,
    0xC5BA3BBE, 0xB2BD0B28, 0x2BB45A92, 0x5CB36A04, 0xC2D7FFA7, 0xB5D0CF31, 0x2CD99E8B, 0x5BDEAE1D,
    0x9B64C2B0, 0xEC63F226, 0x756AA39C, 0x026D930A, 0x9C0906A9, 0xEB0E363F, 0x72076785, 0x05005713,
    0x95BF4A82, 0xE2B87A14, 0x7BB12BAE, 0x0CB61B38, 0x92D28E9B, 0xE5D5BE0D, 0x7CDCEFB7, 0x0BDBDF21,
    0x86D3D2D4, 0xF1D4E242, 0x68DDB3F8, 0x1FDA836E, 0x81BE16CD, 0xF6B9265B, 0x6FB077E1, 0x18B74777,
    0x88085AE6, 0xFF0F6A70, 0x66063BCA, 0x11010B5C, 0x8F659EFF, 0xF862AE69, 0x616BFFD3, 0x166CCF45,
    0xA00AE278, 0xD70DD2EE, 0x4E048354, 0x3903B3C2, 0xA7672661, 0xD06016F7, 0x4969474D, 0x3E6E77DB,
    0xAED16A4A, 0xD9D65ADC, 0x40DF0B66, 0x37D83BF0, 0xA9BCAE53, 0xDEBB9EC5, 0x47B2CF7F, 0x30B5FFE9,
    0xBDBDF21C, 0xCABAC28A, 0x53B39330, 0x24B4A3A6, 0xBAD03605, 0xCDD70693, 0x54DE5729, 0x23D967BF,
    0xB3667A2E, 0xC4614AB8, 0x5D681B02, 0x2A6F2B94, 0xB40BBE37, 0xC30C8EA1, 0x5A05DF1B, 0x2D02EF8D]


# ENUM for PACKET TYPES
class PyPlTypes:
    REQ = 0
    RESP = 1
    IND = 2
    MAX_PYPL_TYPES = 3


# ENUM for PACKET ID(depending on TYPES)
class PyPlReq:
    RASPBERRY_CONNECTED = 0
    MAX_PYPL_REQ = 1


class PyPlResp:
    ACK = 0
    NACK = 1
    MAX_PYPL_RESP = 2


class PyPlInd:
    CAN_MSG = 0
    CONFIG_MSG = 1
    CONN_STATUS = 2
    MAX_PYPL_IND = 3


# Class that create an object that represent a CAN packert
class CanMessage:
    def __init__(self, canDev=0, id=0, dlc=0, payload=bytearray(0)):
        self.canDev = canDev
        self.id = id
        self.dlc = dlc
        self.payload = payload

    def __str__(self):
        # Called by the str() built-in function and by the print statement to
        # compute the "informal" string representation of an object.
        strToPrint = ""
        strToPrint = "CanDev %d --> Message ID %s - DLC %d - PayloadLength %d\n" %(self.canDev, hex(self.id), self.dlc, len(self.payload))
        for cByte in self.payload:
            strToPrint += "%s - " %hex(cByte)
        return strToPrint

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if type(value) is int:
            self._id = value
        else:
            print("CanMessage: ID must be an integer!")

    @property
    def canDev(self):
        return self._canDev

    @canDev.setter
    def canDev(self, value):
        if type(value) is int:
            self._canDev = value
        else:
            print("CanMessage: CanDevice must be an integer!")

    @property
    def dlc(self):
        return self._dlc

    @dlc.setter
    def dlc(self, value):
        if type(value) is int:
            self._dlc = value
        else:
            print("CanMessage: dlc must be an integer!")

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, value):
        if type(value) is bytearray:
            self._payload = value
        else:
            print("CanMessage: ID must be an integer!")


class ArtPyPlCommand:
    _type = struct.pack(">B", 0)
    _id = struct.pack(">B", 0)
    _length = struct.pack(">B", 0)
    _payload = bytearray(0)    # Len 0

    def __init__(self, type=PyPlTypes.IND, id=PyPlInd.CONN_STATUS, payload=bytearray(0)):
        self.type = type
        self.id = id
        self.payload = payload
        # print("ArtPyPlCommand Type ", self.type, " ID ", self.id, "PayloadLen ", len(payload))

    def getBytes(self):
        '''
        Get bytearray of the whole packet, compliant to PyPl standard
        '''
        cPayload = bytearray(0)
        # HEADER
        cPayload.extend(struct.pack(">B", 0xA5))
        cPayload.extend(struct.pack(">B", 0x5A))
        # TYPE
        cPayload.extend(struct.pack(">B", self._type))    # Must be b'\xFF' so bytes type
        # ID
        cPayload.extend(struct.pack(">B", self._id))
        # LEN
        cPayload.extend(struct.pack(">B", len(self.payload)))
        # PAYLOAD
        cPayload.extend(self._payload)
        # CRC
        cPayload.extend(self.evalCRC(cPayload))
        return cPayload

    def getCRC(self):
        cPayload = bytearray(0)
        # HEADER
        cPayload.extend(struct.pack(">B", 0xA5))
        cPayload.extend(struct.pack(">B", 0x5A))
        # TYPE
        cPayload.extend(struct.pack(">B", self._type))    # Must be b'\xFF' so bytes type
        # ID
        cPayload.extend(struct.pack(">B", self._id))
        # LEN
        cPayload.extend(struct.pack(">B", len(self.payload)))
        # PAYLOAD
        cPayload.extend(self._payload)
        # CRC
        return struct.unpack(">I", self.evalCRC(cPayload))

    def evalCRC(self, payload):
        if type(payload) is bytearray:
            evalCRC = 0x00000000
            length = len(payload)
            idx = 0
            while( length > 0):
                evalCRC = crc_table[( (evalCRC ^ payload[idx]) & 0xFF )] ^ (evalCRC >> 8)
                length -= 1
                idx += 1
            return struct.pack(">I", evalCRC)    # Greater means big endian(MSB - LSB)
        else:
            raise AttributeError("Payload must be BYTEARRAY")

    # Property / Setter for payload and type
    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if type(value) is int or (isinstance(value, PyPlTypes)):
            self._type = int(value)
        else:
            print("TYPE must be an integer!")

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if type(value) is int:
            self._id = value
        else:
            print("ID must be an integer!")

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, value):
        if type(value) is bytearray:
            self._payload = value
            # Eval length
            self._length = len(value)
        else:
            print("PAYLOAD is expected to be a bytearray")

    # HELPERS
    def packetFromCanData(self, channel, id, dlc, payload):
        self.type = PyPlTypes.IND
        self.id = PyPlInd.CAN_MSG
        self._payload = bytearray()
        self._payload.extend(struct.pack(">B", channel))
        self._payload.extend(struct.pack(">I", id))
        self._payload.extend(struct.pack(">B", dlc))
        self._payload.extend(payload)
        self._length = struct.pack(">B", len(payload))

    # Print will call this function
    def __str__(self):
        strToPrint = ""
        strToPrint = "Packet Type %d - ID %d - Payload Length %d\n" %(self.type, self.id, len(self.payload))
        for cByte in self.payload:
            strToPrint += "%s - " %hex(cByte)
        return strToPrint


class ArtPyPlParser:
    _allowedStates = ["HEADER", "TYPE", "ID", "LEN", "PAYLOAD", "CRC"]

    def __init__(self, state):
        self.gotFirstHeader = False
        self.state = state
        self.expLen = 0
        self.tmpPayload = bytearray(0)
        self.crcByteArray = bytearray(0)
        self.packetComplete = False
        # tmpPacket
        self.tmpPacket = ArtPyPlCommand(0, 0, bytearray(0))

    def resetFSM(self, state):
        self.explen = 0
        self.gotFirstHeader = False
        self.crcByteArray = bytearray(0)
        self.tmpPayload = bytearray(0)
        self.state = state
        self.packetComplete = False

    def processByte(self, cByte):
        retVal = False
        # Analyze only bytes or integers!
        if type(cByte) is not int:
            print("processByte: expected integer! Got ", type(cByte))
            return False
        # print("processByte: state -> ", self.state, " cByte -> ", cByte)
        # Header case
        if self.state == self._allowedStates[0]:
            # Got first byte ?
            if self.gotFirstHeader is False:
                if cByte == int("A5", 16):
                    self.gotFirstHeader = True
                else:
                    self.resetFSM("HEADER")
            else:
                if cByte == int("5A", 16):
                    self.state = "TYPE"
                else:
                    self.resetFSM("HEADER")
        # TYPE
        elif self.state == self._allowedStates[1]:
            # Check if type is within allowed values
            if cByte <= 2 and cByte >= 0:
                self.tmpPacket.type = cByte
                self.state = "ID"
            else:
                self.resetFSM("HEADER")
        # ID
        elif self.state == self._allowedStates[2]:
            self.tmpPacket.id = cByte
            self.state = "LEN"
        # LEN
        elif self.state == self._allowedStates[3]:
            if cByte <= 255:
                self.expLen = cByte
                # If len is 0, skip getting payload
                if self.expLen == 0:
                    self.state = "CRC"
                else:
                    self.state = "PAYLOAD"
                    # Reset tmp packet payload
                    self.tmpPacket.payload = bytearray(0)
            else:
                self.resetFSM("HEADER")
        # Payload
        elif self.state == self._allowedStates[4]:
            self.tmpPayload.extend(struct.pack(">B", cByte))
            # Check if we got all the bytes we needed
            if len(self.tmpPayload) >= self.expLen:
                self.state = "CRC"
                self.tmpPacket.payload = self.tmpPayload
        # CRC
        elif self.state == self._allowedStates[5]:
            self.crcByteArray.extend(struct.pack(">B", cByte))
            # WE got all the bytes ?
            if len(self.crcByteArray) == 4:
                # Check if CRC matches
                if struct.unpack(">I", self.crcByteArray) == self.tmpPacket.getCRC():
                    retVal = True
                self.resetFSM("HEADER")
        else:
            self.resetFSM("HEADER")
        # Return true or false if parsing is going as expected or not
        return retVal

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if value in self._allowedStates:
            self._state = value
        else:
            print("Wrong state has been set! Resetting to HEADER")
            self._state = self._allowedStates[0]

    def __str__(self):
        strToPrint = "ArtPyPlParser: current state is %s" % self.state
        return strToPrint


# This class acts like a server to send CMDS
class ArtPyPlClient:
    def __init__(self):
        print("ArtPyPlClient: Trying to allocate socket")
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.settimeout(0.5)
        except socket.error:
            print("Could not allocate socket!")
        self._rxQueue = LifoQueue()
        self._txQueue = LifoQueue()
        # Diagnostic
        self._sentData = 0
        self._recvData = 0
        # Debug
        # threading.Timer(10.0, self.forceCloseConn).start()
        # Parsing variables
        self._parser = ArtPyPlParser("HEADER")

        print("ArtPyPlClient: Socket allocated successfully! Use connect() method")

    def __del__(self):
        self.endComm()

    def connect(self):
        print("ArtPyPlClient: Trying to connect...", end="")
        cnt = 0
        try:
            self._socket.connect(("127.0.0.1", 3456))
        except socket.error:
            print(" Connection refused!")
            return False
        # init threading
        self.enableTxLoop = True
        self.threadTx = threading.Thread(target=self.handleTxComm)
        self.enableRxLoop = True
        self.threadRx = threading.Thread(target=self.handleRxComm)
        self.threadTx.start()
        self.threadRx.start()
        print(" Connection Successful!")
        return True

    def handleTxComm(self):
        print("HandleTxComm")
        while self.enableTxLoop == True:
            cData = ""
            try:
                cData = self._txQueue.get(block=False, timeout=100)
            except:
                continue
            # Print cData then send over socket
            #print("Sending ", cData)
            # handle cData
            self._socket.send(cData)
            self._sentData += 1
        print("Exiting HandleTxComm")

    def handleRxComm(self):
        print("HandleRxComm")
        # Reset FSM
        self._parser.resetFSM("HEADER")
        cData = bytearray(0)
        while self.enableRxLoop == True:
            try:
                cData = self._socket.recv(1024)
                self._recvData += 1
                # parse. If packet is complete, pass the bytearray to self.sig_queue.put(bytes_handle, False)
                for cByte in cData:
                    # Process Byte. If following method returns true, then a message has been received!
                    if self._parser.processByte(cByte) == True:
                        # Get packet and do something with it
                        # Dispatch
                        self.dispatchPacket(self._parser.tmpPacket)
            except socket.timeout:
                cData = bytearray(0)
                continue
            except:
                # Clean cData
                cData.clear()
                print("RX COMM ERROR")
                break
        print("Exiting HandleRxComm")

    def dispatchPacket(self, tmpPacket):
        '''
        Takes a ArtPyPlCommand and dispatch according to its inner data
        '''
        # Print incoming packet
        # print("dispatchPacket: ", tmpPacket)
        if tmpPacket.type == 2 and tmpPacket.id == 0:
            newMsg = CanMessage(tmpPacket.payload[0],
                                struct.unpack(">I", tmpPacket.payload[1:1+4])[0],
                                tmpPacket.payload[5],
                                tmpPacket.payload[6:])
        # print(newMsg)
            self._rxQueue.put(newMsg)
        # self.sig_queue.put(tmpPacket.getBytes())

    def forceCloseConn(self):
        self.enableTxLoop = False
        self.enableRxLoop = False

    @property
    def isConnected(self):
        return self.enableTxLoop and self.enableRxLoop

    @isConnected.setter
    def isConnected(self, value):
        # Do Nothing
        print(end='')

    def endComm(self):
        print("endcomM CALLED")
        # Close RX thread
        if self.threadRx == None:
            print("No current communication ongoing")
        else:
            # Let last loop iteration finish
            self.enableRxLoop = False
            # Join threads on the main one
            self.threadRx.join()

        # Close TX Thread
        if self.threadTx == None:
            print("No current TX communication ongoing")
        else:
            # Close loop and join thread
            self.enableTxLoop = False
            self.threadTx.join()

    # HELPERS to simplify how to use this class!
    #
    def sendCommand(self, currCMD):
        # Is currCMD an ArtPyPlCommand ?
        if isinstance(currCMD, ArtPyPlCommand):
            self._txQueue.put(currCMD.getBytes(), False)
            # print("sendCommand: command sent!")
        else:
            print("sendCommand: expected to get an ArtPyPlCommand.", end="")
            print("Got instead", type(currCMD))

    def rxCANAvailable(self):
        return not self._rxQueue.empty()

    def getCANMessage(self):
        retData = CanMessage()
        try:
            retData = self._rxQueue.get(block=False)
        except:
            print("getCANMessage: No available CAN messages!")
        return retData


if __name__ == "__main__":
    a = ArtPyPlClient()
    # Try to connect and get an handle on the socket!
    while not a.connect():
        continue
    # Until we are connected, we will populate the queue with PyPlPackets
    while a.enableTxLoop:
        # Create packet
        cPkt = ArtPyPlCommand()
        canPayload = bytearray()
        canPayload.extend(struct.pack(">I", 0xABCDEF12))    # First 4 bytes of CAN Payload
        canPayload.extend(struct.pack(">I", 0xABCDEF12))    # Lst 4 bytes of CAN Payload
        cPkt.packetFromCanData(0, 0x7A3, 8,  canPayload)    # Populate Packet
        a.sendCommand(cPkt)
        if a.rxCANAvailable():
            print(a.getCANMessage())
    a.endComm()
