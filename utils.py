import can
import threading
import logging
import time
from messages_db import *


class Listener(object):

    def __init__(self, bus, id, dlc, blocking=False, timeout=100):
        self.bus = bus
        self.id = id
        self.dlc = dlc
        self.blocking = blocking
        self.timeout = timeout
        self._running = True

        self.timer = threading.Timer(timeout, self.on_timeout)
        self.timer.start()
        if not blocking:
            self.hooker = threading.Thread(target=self._rx_thread, args=(bus,), name='CAN Listener for messages "{}"'.format(hex(id)))
            self.hooker.start()
        else:
            self._rx_thread(bus)

    def on_message_received(self, msg):
        if msg.arbitration_id == self.id and msg.dlc == self.dlc:
            if self.blocking:
                return msg
            else:
                self.result = msg
            # TODO: Check already here is payload is as wanted??
            self.timer.cancel()
            self.stop()

    def stop(self):
        self._running = False
        if not self.blocking:
            self.hooker.join()
        print('Listener for id = "{}" stopped.'.format(hex(id)))

    def _rx_thread(self, bus):
        msg = None
        try:
            while(self._running):
                if msg is not None:
                    self.on_message_received(msg)
                msg = bus.recv(.1)
                time.sleep(0.050)
        except:
            BusError('Cannot receivemessages from bus')

    def on_timeout(self):
        print('[TIMEOUT]: Waiting for id "{}"'.format(hex(self.id)))
        self.timer.cancel()
        self.stop()
        return False

    def retrieve_info(self):
        if self.result is not None:
            return self.result
        else:
            return False

''' Functions that emulate Buttons pressure'''


def press_back_main(original_payload, val=0):
    compose_STATUS_NVO(original_payload, Back_MainButtonSts=val)
    return can_pack(BH['STATUS_NVO'][0], BH['STATUS_NVO'][1], original_payload)


def change_manettino(original_payload, value=3):
    compose_STATUS_NVO(original_payload, ManettinoSts=value)
    return can_pack(BH['STATUS_NVO'][0], BH['STATUS_NVO'][1], original_payload)


def press_source_button(original_payload, val=0):
    compose_STATUS_NVO(original_payload, SourceButtonPushSts=val)
    return can_pack(BH['STATUS_NVO'][0], BH['STATUS_NVO'][1], original_payload)


def set_HManettinoDriverWish(original_payload, val=0):
    compose_STATUS_NVO(original_payload, HManettinoDriverWish=val)
    return can_pack(BH['STATUS_NVO'][0], BH['STATUS_NVO'][1], original_payload)


def press_confort_button(original_payload, val=0):
    compose_STATUS_NVO(original_payload, ComfortButtonSts=val)
    return can_pack(BH['STATUS_NVO'][0], BH['STATUS_NVO'][1], original_payload)


def press_voice_recognition(original_payload, val=0):
    compose_STATUS_NVO(original_payload, VoiceRecognitionSts=val)
    x = can_pack(BH['STATUS_NVO'][0], BH['STATUS_NVO'][1], original_payload)
    return x


def press_declatter(original_payload, val=0):
    compose_STATUS_NVO(original_payload, DeclutterButtonSts=val)
    return can_pack(BH['STATUS_NVO'][0], BH['STATUS_NVO'][1], original_payload)


def press_phone_call_button(original_payload, val=0):
    compose_STATUS_NVO(original_payload, PhoneCallButtonSts=val)
    return can_pack(BH['STATUS_NVO'][0], BH['STATUS_NVO'][1], original_payload)


''' Functions that emulate touchpad gesture'''
## TODO: try to make a function that map postion
