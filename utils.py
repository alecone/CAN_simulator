import can
import threading
import logging
import time
from messages_db import *

class Listener(object):

    def __init__(self, bus, id, dlc):
        self.id = id
        self.dlc = dlc
        self.bus = bus
        self.old_msg = can_pack(id=self.id, dlc=self.dlc, data=bytearray(8))
        self._running = True

        # Filter the bus
        self.bus.set_filters([{"can_id": self.id, "can_mask": 0xFFFF, "extended": False}])
        # self.hooker = threading.Thread(target=self._rx_thread, args=(self.bus,), name='CAN Listener for messages "{}"'.format(hex(id)))
        # self.hooker.start()
        self._rx_thread(self.bus)

    def on_message_received(self, msg):
        if msg.arbitration_id == self.old_msg.arbitration_id:
            if msg.data != self.old_msg.data:
                print(msg)
                self.old_msg.data = msg.data


    def stop(self):
        self._running = False
        # self.hooker.join()
        print('Listener for id = "{}" stopped.'.format(hex(id)))

    def _rx_thread(self, bus):
        msg = None
        try:
            while(self._running):
                if msg is not None:
                    self.on_message_received(msg)
                msg = bus.recv(1)
                time.sleep(0.050)
        except:
            BusError('Cannot receivemessages from bus')

''' Functions that emulate the manubrio gesture. They return a CAN packet or a list of CAN packets'''

def press_back_main(original_payload):
    packs = []
    compose_STATUS_NVO(original_payload, Back_MainButtonSts=0)
    x = can_pack(BH['STATUS_NVO'][0], BH['STATUS_NVO'][1], original_payload)
    packs.append(x)
    compose_STATUS_NVO(original_payload, Back_MainButtonSts=1)
    x = can_pack(BH['STATUS_NVO'][0], BH['STATUS_NVO'][1], original_payload)
    packs.append(x)
    compose_STATUS_NVO(original_payload, Back_MainButtonSts=0)
    x = can_pack(BH['STATUS_NVO'][0], BH['STATUS_NVO'][1], original_payload)
    packs.append(x)
    return packs

def change_manettino(original_payload, value=3):
    compose_STATUS_NVO(original_payload, ManettinoSts=value)
    return can_pack(BH['STATUS_NVO'][0], BH['STATUS_NVO'][1], original_payload)

def press_source_button(original_payload):
    packs = []
    compose_STATUS_NVO(original_payload, SourceButtonPushSts=0)
    x = can_pack(BH['STATUS_NVO'][0], BH['STATUS_NVO'][1], original_payload)
    packs.append(x)
    compose_STATUS_NVO(original_payload, SourceButtonPushSts=1)
    x = can_pack(BH['STATUS_NVO'][0], BH['STATUS_NVO'][1], original_payload)
    packs.append(x)
    compose_STATUS_NVO(original_payload, SourceButtonPushSts=0)
    x = can_pack(BH['STATUS_NVO'][0], BH['STATUS_NVO'][1], original_payload)
    packs.append(x)
    return packs

def set_HManettinoDriverWish(original_payload, val):
    packs = []
    compose_STATUS_NVO(original_payload, HManettinoDriverWish=0)
    x = can_pack(BH['STATUS_NVO'][0], BH['STATUS_NVO'][1], original_payload)
    packs.append(x)
    compose_STATUS_NVO(original_payload, HManettinoDriverWish=val)
    x = can_pack(BH['STATUS_NVO'][0], BH['STATUS_NVO'][1], original_payload)
    packs.append(x)
    compose_STATUS_NVO(original_payload, HManettinoDriverWish=0)
    x = can_pack(BH['STATUS_NVO'][0], BH['STATUS_NVO'][1], original_payload)
    packs.append(x)
    return packs

def press_confort_button(original_payload, val=0):
    compose_STATUS_NVO(original_payload, ComfortButtonSts=val)
    x = can_pack(BH['STATUS_NVO'][0], BH['STATUS_NVO'][1], original_payload)
    return x

def press_voice_recognition(original_payload, val=0):
    compose_STATUS_NVO(original_payload, VoiceRecognitionSts=val)
    x = can_pack(BH['STATUS_NVO'][0], BH['STATUS_NVO'][1], original_payload)
    return x

def press_declatter(original_payload):
    packs = []
    compose_STATUS_NVO(original_payload, DeclutterButtonSts=0)
    x = can_pack(BH['STATUS_NVO'][0], BH['STATUS_NVO'][1], original_payload)
    packs.append(x)
    compose_STATUS_NVO(original_payload, DeclutterButtonSts=1)
    x = can_pack(BH['STATUS_NVO'][0], BH['STATUS_NVO'][1], original_payload)
    packs.append(x)
    compose_STATUS_NVO(original_payload, DeclutterButtonSts=0)
    x = can_pack(BH['STATUS_NVO'][0], BH['STATUS_NVO'][1], original_payload)
    packs.append(x)
    return packs

def press_phone_call_button(original_payload):
    packs = []
    compose_STATUS_NVO(original_payload, PhoneCallButtonSts=0)
    x = can_pack(BH['STATUS_NVO'][0], BH['STATUS_NVO'][1], original_payload)
    packs.append(x)
    compose_STATUS_NVO(original_payload, PhoneCallButtonSts=1)
    x = can_pack(BH['STATUS_NVO'][0], BH['STATUS_NVO'][1], original_payload)
    packs.append(x)
    compose_STATUS_NVO(original_payload, PhoneCallButtonSts=0)
    x = can_pack(BH['STATUS_NVO'][0], BH['STATUS_NVO'][1], original_payload)
    packs.append(x)
    return packs
