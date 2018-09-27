import can
import threading
import logging
from time import sleep
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
                sleep(0.050)
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

def set_touchpad(original_payload, xval=0, yval=0, push=0, gesture_step=0, gest_type=0):
    compose_NVO_STATUS_TOUCHPAD(original_payload, Xposition=0, Yposition=0, FingerPresent=1, GestureType=0)
    compose_NVO_STATUS_TOUCHPAD(original_payload, Xposition=xval, Yposition=yval, FingerPresent=1, GestureStep=gesture_step, Push=push, GestureType=gest_type)
    return can_pack(BH['NVO_STATUS_TOUCH'][0], BH['NVO_STATUS_TOUCH'][1], original_payload)

'''      FUNCTIONS THAT HAVE TO BE CALLED FOR GESTURES      '''

def comfort(can_bus):
    payload_STATUS_NVO = bytearray(8)
    timeout_STATUS_NVO = 1
    for i in [0, 1, 0]:
        pack = press_confort_button(payload_STATUS_NVO, i)
        can_bus.send(pack)
        sleep(timeout_STATUS_NVO)

def back(can_bus):
    payload_STATUS_NVO = bytearray(8)
    timeout_STATUS_NVO = 1
    for i in [0, 1, 0]:
        pack = press_back_main(payload_STATUS_NVO, i)
        can_bus.send(pack)
        sleep(timeout_STATUS_NVO)

def manettino(can_bus, val):
    payload_STATUS_NVO = bytearray(8)
    timeout_STATUS_NVO = 1
    pack = change_manettino(payload_STATUS_NVO, i)
    can_bus.send(pack)
    sleep(timeout_STATUS_NVO)

def source(can_bus):
    payload_STATUS_NVO = bytearray(8)
    timeout_STATUS_NVO = 1
    for i in [0, 1, 0]:
        pack = press_source_button(payload_STATUS_NVO, i)
        can_bus.send(pack)
        sleep(timeout_STATUS_NVO)

def driver_wish(can_bus, val):
    payload_STATUS_NVO = bytearray(8)
    timeout_STATUS_NVO = 1
    pack = set_HManettinoDriverWish(payload_STATUS_NVO, i)
    can_bus.send(pack)
    sleep(timeout_STATUS_NVO)

def voice(can_bus):
    payload_STATUS_NVO = bytearray(8)
    timeout_STATUS_NVO = 1
    for i in [0, 1, 0]:
        pack = press_voice_recognition(payload_STATUS_NVO, i)
        can_bus.send(pack)
        sleep(timeout_STATUS_NVO)

def declutter(can_bus):
    payload_STATUS_NVO = bytearray(8)
    timeout_STATUS_NVO = 1
    for i in [0, 1, 0]:
        pack = press_declatter(payload_STATUS_NVO, i)
        can_bus.send(pack)
        sleep(timeout_STATUS_NVO)

def phone(can_bus):
    payload_STATUS_NVO = bytearray(8)
    timeout_STATUS_NVO = 1
    for i in [0, 1, 0]:
        pack = press_phone_call_button(payload_STATUS_NVO, i)
        can_bus.send(pack)
        sleep(timeout_STATUS_NVO)

def long_press_menu(can_bus):
    payload_STATUS_NVO = bytearray(8)
    timeout_STATUS_NVO = 1
    for i in [0, 1, 1, 1, 1, 1, 0]:
        pack = press_back_main(payload_STATUS_NVO, i)
        can_bus.send(pack)
        sleep(timeout_STATUS_NVO)

def scroll_left(can_bus):
    payload_TOUCHPAD = bytearray(8)
    timeout_TOUCHPAD = 0.050
    x_tick = int(512/10)
    y_const = int(512/2)
    g_type = 0
    g_step = 0
    for i in [10,9,8,7,6,5,4,3,2,1]:
        if i == 6:
            g_type = 3
            g_step = 1
        pack = set_touchpad(payload_TOUCHPAD, xval=x_tick*i, yval=y_const, push=0, gesture_step=g_step, gest_type=g_type)
        can_bus.send(pack)
        sleep(timeout_TOUCHPAD)

def scroll_right(can_bus):
    payload_TOUCHPAD = bytearray(8)
    timeout_TOUCHPAD = 0.050
    x_tick = int(512/10)
    y_const = int(512/2)
    g_type = 0
    g_step = 0
    for i in [1,2,3,4,5,6,7,8,9,10]:
        if i == 5:
            g_type = 4
            g_step = 1
        pack = set_touchpad(payload_TOUCHPAD, xval=x_tick*i, yval=y_const, push=0, gesture_step=g_step, gest_type=g_type)
        can_bus.send(pack)
        sleep(timeout_TOUCHPAD)

def scroll_up(can_bus):
    payload_TOUCHPAD = bytearray(8)
    timeout_TOUCHPAD = 0.050
    y_tick = int(512/10)
    x_const = int(512/2)
    g_type = 0
    g_step = 0
    for i in [1,2,3,4,5,6,7,8,9,10]:
        if i == 5:
            g_type = 1
            g_step = 1
        pack = set_touchpad(payload_TOUCHPAD, xval=x_const, yval=y_tick*i, push=0, gesture_step=g_step, gest_type=g_type)
        can_bus.send(pack)
        sleep(timeout_TOUCHPAD)

def scroll_down(can_bus):
    payload_TOUCHPAD = bytearray(8)
    timeout_TOUCHPAD = 0.050
    y_tick = int(512/10)
    x_const = int(512/2)
    g_type = 0
    g_step = 0
    for i in [10,9,8,7,6,5,4,3,2,1]:
        if i == 6:
            g_type = 2
            g_step = 1
        pack = set_touchpad(payload_TOUCHPAD, xval=x_const, yval=y_tick*i, push=0, gesture_step=g_step, gest_type=g_type)
        can_bus.send(pack)
        sleep(timeout_TOUCHPAD)

def press_center(can_bus):
    payload_TOUCHPAD = bytearray(8)
    timeout_TOUCHPAD = 0.050
    y_const = int(512/2)
    x_const = int(512/2)
    for i in range(10):
        pack = set_touchpad(payload_TOUCHPAD, xval=x_const, yval=y_const, push=1, gesture_step=0, gest_type=0)
        can_bus.send(pack)
        sleep(timeout_TOUCHPAD)
