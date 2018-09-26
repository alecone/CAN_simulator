from pypl import ArtPyPlCommand
import signal, sys, time, struct
import can
# Can Database / 'name' : channel, 0xID, DLC, Paylod /
BH = {
    # Message for main node useage
    'NWM_NBC': [0x700, 6],
    # Message for button pressure form message STATUS_NVO
    'STATUS_NVO': [0x3C4, 8],
    # Message with key Status and more
    'STATUS_NBC': [0x380, 8],
    # Message with touchPad signal
    'NVO_STATUS_TOUCH': [0x21F, 8]
}

def can_pack(id, dlc, data):
    return can.Message(extended_id=False, arbitration_id=id, dlc=dlc, data=data)

def compose_STATUS_NVO(payload,
                       SourceButtonPushSts=None,
                       AudioModeCntrl=None,
                       AudioModeDownCntrl=None,
                       AudioModeUpCntrl=None,
                       VolumeButtonPushStatus=None,
                       VolumeDownStatus=None,
                       VolumeUpStatus=None,
                       HManettinoDriverWishFailSts=None,
                       HManettinoDriverWish=None,
                       VoiceRecognitionSts=None,
                       ManettinoFailSts=None,
                       ManettinoSts=None,
                       TelephoneCallSts=None,
                       ESPChangeModeReqSts=None,
                       FlashBeamSwitchSts=None,
                       FrontWindshieldWasherSwitchSts=None,
                       LdirectionSwitchSts=None,
                       RdirectionSwitchSts=None,
                       LChangeLanSts=None,
                       RChangeLanSts=None,
                       ComfortButtonSts=None,
                       Back_MainButtonSts=None,
                       VoiceRecognitionButtonSts=None,
                       DeclutterButtonSts=None,
                       RearWindowWasherSwitchSts=None,
                       RearWindowWiperSwitchSts=None,
                       FrontWindshieldWiperSwitchSts=None,
                       HighBeamSwitchSts=None,
                       ScanRotation=None,
                       VolumeRotation=None,
                       ManettinoSuspentionSts=None,
                       PhoneCallButtonSts=None,
                       VolumeDial=None,
                       ScanDial=None):
    # payload = bytearray(8)
    if type(payload) is not bytearray:
        raise TypeError('Paylod is not a bytearray')
    if SourceButtonPushSts == 1:
        payload[0] |= 0x02
    elif SourceButtonPushSts == 0:
        payload[0] &= 0xFD
    if AudioModeCntrl == 1:
        payload[0] |= 0x04
    elif AudioModeCntrl == 0:
        payload[0] &= 0xFB
    if AudioModeDownCntrl == 1:
        payload[0] |= 0x08
    elif AudioModeDownCntrl == 0:
        payload[0] &= 0xF7
    if AudioModeUpCntrl == 1:
        payload[0] |= 0x10
    elif AudioModeUpCntrl == 0:
        payload[0] &= 0xEF
    if VolumeButtonPushStatus == 1:
        payload[0] |= 0x20
    elif VolumeButtonPushStatus == 0:
        payload[0] &= 0xDF
    if VolumeDownStatus == 1:
        payload[0] |= 0x40
    elif VolumeDownStatus == 0:
        payload[0] &= 0xBF
    if VolumeUpStatus == 1:
        payload[0] |= 0x80
    elif VolumeUpStatus == 0:
        payload[0] &= 0x7F

    if HManettinoDriverWishFailSts == 1:
        payload[1] |= 0x04
    elif HManettinoDriverWishFailSts == 0:
        payload[1] &= 0xFB
    if HManettinoDriverWish == 1: # eDrive
        payload[1] |= 0x08
    elif HManettinoDriverWish == 2: # Hybrid
        payload[1] |= 0x10
    elif HManettinoDriverWish == 3: # Performance
        payload[1] |= 0x18
    elif HManettinoDriverWish == 4: # Qualifying
        payload[1] |= 0x20
    elif HManettinoDriverWish == 0:
        payload[1] &= 0xC7
    if VoiceRecognitionSts == 1:
        payload[1] |= 0x40
    elif VoiceRecognitionSts == 0:
        payload[1] &= 0xBF

    if ManettinoFailSts == 1:
        payload[2] |= 0x01
    elif ManettinoFailSts == 1:
        payload[2] &= 0xFE
    if ManettinoSts == 1:
        payload[2] |= 0x02
    elif ManettinoSts == 2:
        payload[2] |= 0x04
    elif ManettinoSts == 3:
        payload[2] |= 0x06
    elif ManettinoSts == 4:
        payload[2] |= 0x08
    elif ManettinoSts == 0:
        payload[2] &= 0xF1
    if TelephoneCallSts == 1:
        payload[2] |= 0x10
    elif TelephoneCallSts == 0:
        payload[2] &= 0xEF
    if ESPChangeModeReqSts == 1:
        payload[2] |= 0x20
    elif ESPChangeModeReqSts == 0:
        payload[2] &= 0xDF

    if FlashBeamSwitchSts == 1:
        payload[3] |= 0x01
    elif FlashBeamSwitchSts == 0:
        payload[3] &= 0xFE
    if FrontWindshieldWasherSwitchSts == 1:
        payload[3] |= 0x02
    elif FrontWindshieldWasherSwitchSts == 0:
        payload[3] &= 0xFD
    if LdirectionSwitchSts == 1:
        payload[3] |= 0x04
    elif LdirectionSwitchSts == 0:
        payload[3] &= 0xFB
    if RdirectionSwitchSts == 1:
        payload[3] |= 0x08
    elif RdirectionSwitchSts == 0:
        payload[3] &= 0xF7
    if LChangeLanSts == 1:
        payload[3] |= 0x10
    elif LChangeLanSts == 0:
        payload[3] &= 0xEF
    if RChangeLanSts == 1:
        payload[3] |= 0x20
    elif RChangeLanSts == 0:
        payload[3] &= 0xDF
    if ComfortButtonSts == 1:
        payload[3] |= 0x40
    elif ComfortButtonSts == 0:
        payload[3] &= 0xBF
    if Back_MainButtonSts == 1:
        payload[3] |= 0x80
    elif Back_MainButtonSts == 0:
        payload[3] &= 0x7F

    if VoiceRecognitionSts == 1:
        payload[4] |= 0x01
    elif VoiceRecognitionSts == 0:
        payload[4] &= 0xFE
    if DeclutterButtonSts == 1:
        payload[4] |= 0x02
    elif DeclutterButtonSts == 0:
        payload[4] &= 0xFD
    if RearWindowWasherSwitchSts == 1:
        payload[4] |= 0x04
    elif RearWindowWasherSwitchSts == 0:
        payload[4] &= 0xFB
    if RearWindowWiperSwitchSts == 1:
        payload[4] |= 0x08
    elif RearWindowWiperSwitchSts == 0:
        payload[4] &= 0xF7
    if FrontWindshieldWiperSwitchSts == 1: # Antipanic
        payload[4] |= 0x10
    elif FrontWindshieldWiperSwitchSts == 2: # First Speed
        payload[4] |= 0x20
    elif FrontWindshieldWiperSwitchSts == 3: # Second Speed
        payload[4] |= 0x30
    elif FrontWindshieldWiperSwitchSts == 4: # Auto1
        payload[4] |= 0x40
    elif FrontWindshieldWiperSwitchSts == 5: # Auto2
        payload[4] |= 0x50
    elif FrontWindshieldWiperSwitchSts == 0:
        payload[4] &= 0x8F
    if HighBeamSwitchSts == 1:
        payload[4] |= 0x80
    elif HighBeamSwitchSts == 0:
        payload[4] &= 0x7F

    if ScanRotation == 1: # ScanEncoderClockwiseRot
        payload[5] |= 0x01
    elif ScanRotation == 2: # ScanEncoderCounterClockwiseRot
        payload[5] |= 0x02
    elif ScanRotation == 0:
        payload[5] &= 0xFC
    if VolumeRotation == 1: # VolumeEncoderClockwiseRot
        payload[5] |= 0x04
    elif VolumeRotation == 2: # VolumeEncoderCounterClockwiseRot
        payload[5] |= 0x08
    elif VolumeRotation == 0:
        payload[5] &= 0xF3
    if ManettinoSuspentionSts == 1:
        payload[5] |= 0x10
    elif ManettinoSuspentionSts == 2:
        payload[5] |= 0x20
    elif ManettinoSuspentionSts == 3:
        payload[5] |= 0x30
    elif ManettinoSuspentionSts == 0:
        payload[5] &= 0x8F
    if PhoneCallButtonSts == 1:
        payload[5] |= 0x80
    elif PhoneCallButtonSts == 0:
        payload[5] &= 0x7F

    if VolumeDial:
        payload[6] = (VolumeDial)
    elif VolumeDial == 0:
        payload[6] = 0x00

    if ScanDial:
        payload[7] = (ScanDial)
    elif ScanDial == 0:
        payload[7] = 0x00
    # return can_pack(BH['STATUS_NVO'][0], BH['STATUS_NVO'][1], payload)
    return payload

def compose_STATUS_NBC(payload,
                       CeilingLightSts=None,
                       SysEOLSts=None,
                       InternalLightSts=None,
                       VehicleNotUseSignaling=None,
                       HandBrakeSts=None,
                       InternalBacklightStsKeyOff=None,
                       BrakePadWearSts=None,
                       HatchUnlockCntrl=None,
                       WishWashSts=None,
                       DriverDoorSts=None,
                       PsngrDoorSts=None,
                       LHRDoorSts=None,
                       RHRDoorSts=None,
                       RhatchSts=None,
                       BonnetSts=None,
                       ReverseGearBCSts=None,
                       RechargeSts=None,
                       KeySts=None,
                       BatteryVoltageLevel=None,
                       NBCFISSts=None,
                       FuelLevelFailSts=None,
                       LowFuelWarningSts=None,
                       AlarmSysTurnOn=None,
                       NBCRogerBeepCntrl=None,
                       FuelLevel=None,
                       IMMOCodeWarningLightSts=None,
                       VehicleProtectionFailSts=None,
                       CityModeSts=None,
                       RwiperCntrl=None,
                       Rele2Sts=None,
                       LH_Mirror_LED_Err=None,
                       RH_Mirror_LED_Err=None,
                       TurnIndicatorSts=None,
                       RainSensorFailSts=None):
    # payload = bytearray(8)
    if type(payload) is not bytearray:
        raise TypeError('Paylod is not a bytearray')
    if CeilingLightSts == 1:
        payload[0] |= 0x01
    if CeilingLightSts == 2:
        payload[0] |= 0x02
    if CeilingLightSts == 3:
        payload[0] |= 0x03
    elif CeilingLightSts == 0:
        payload[0] &= 0xFE
    if SysEOLSts == 1:
        payload[0] |= 0x04
    elif SysEOLSts == 0:
        payload[0] &= 0xFB
    if InternalLightSts == 1:
        payload[0] |= 0x08
    elif InternalLightSts == 0:
        payload[0] &= 0xF7
    if VehicleNotUseSignaling == 1:
        payload[0] |= 0x10
    elif VehicleNotUseSignaling == 0:
        payload[0] &= 0xEF
    if HandBrakeSts == 1:
        payload[0] |= 0x20
    elif HandBrakeSts == 0:
        payload[0] &= 0xDF
    if InternalBacklightStsKeyOff == 1:
        payload[0] |= 0x40
    elif InternalBacklightStsKeyOff == 0:
        payload[0] &= 0xBF
    if BrakePadWearSts == 1:
        payload[0] |= 0x80
    elif BrakePadWearSts == 0:
        payload[0] &= 0x7F

    if HatchUnlockCntrl == 1:
        payload[1] |= 0x01
    elif HatchUnlockCntrl == 0:
        payload[1] &= 0xFE
    if WishWashSts == 1:
        payload[1] |= 0x02
    elif WishWashSts == 0:
        payload[1] &= 0xFD
    if DriverDoorSts == 1:
        payload[1] |= 0x04
    elif DriverDoorSts == 0:
        payload[1] &= 0xFB
    if PsngrDoorSts == 1:
        payload[1] |= 0x08
    elif PsngrDoorSts == 0:
        payload[1] &= 0xF7
    if LHRDoorSts == 1:
        payload[1] |= 0x10
    elif LHRDoorSts == 0:
        payload[1] &= 0xEF
    if RHRDoorSts == 1:
        payload[1] |= 0x20
    elif RHRDoorSts == 0:
        payload[1] &= 0xDF
    if RhatchSts == 1:
        payload[1] |= 0x40
    elif RhatchSts == 0:
        payload[1] &= 0xBF
    if BonnetSts == 1:
        payload[1] |= 0x80
    elif BonnetSts == 0:
        payload[1] &= 0x7F

    if ReverseGearBCSts == 1:
        payload[2] |= 0x04
    elif ReverseGearBCSts == 0:
        payload[2] &= 0xFB
    if RechargeSts == 1:
        payload[2] |= 0x08
    elif RechargeSts == 0:
        payload[2] &= 0xF7
    if KeySts == 1: #STOP
        payload[2] |= 0x10
    elif KeySts == 2: #PARK
        payload[2] &= 0xEF
        payload[2] |= 0x20
    elif KeySts == 4:
        payload[2] &= 0xCF
        payload[2] |= 0x40
    elif KeySts == 0:
        payload[2] &=  0x8F

    if BatteryVoltageLevel is not None:
        if BatteryVoltageLevel < 128 and BatteryVoltageLevel > 0:
            payload[3] |= (BatteryVoltageLevel)
        elif BatteryVoltageLevel == 0:
            payload[3] &= 0x80
    if NBCFISSts == 1:
        payload[3] |= 0x80
    elif NBCFISSts == 0:
        payload[3] &= 0x7F

    if FuelLevelFailSts == 1:
        payload[4] |= 0x01
    elif FuelLevelFailSts == 0:
        payload[4] &= 0xFE
    if LowFuelWarningSts == 1:
        payload[4] |= 0x02
    elif LowFuelWarningSts == 0:
        payload[4] &= 0xFD
    if AlarmSysTurnOn is not None:
        if AlarmSysTurnOn > 3 and AlarmSysTurnOn < 128:
            payload[4] |= (AlarmSysTurnOn)
        elif AlarmSysTurnOn <= 3 or AlarmSysTurnOn >= 128:
            payload[4] &= 0x80
    if NBCRogerBeepCntrl == 1:
        payload[4] |= 0x80
    elif NBCRogerBeepCntrl == 0:
        payload[4] &= 0x7F

    if FuelLevel is not None:
        if FuelLevel > 0 and FuelLevel < 256:
            payload[5] = FuelLevel
        elif FuelLevel == 0 or FuelLevel >= 256:
            payload[5] = 0

    if IMMOCodeWarningLightSts is not None:
        if IMMOCodeWarningLightSts < 18:
            payload[6] |= (IMMOCodeWarningLightSts)
        elif IMMOCodeWarningLightSts >= 18:
            payload[6] &= 0xE0
    if VehicleProtectionFailSts == 1:
        payload[6] |= 0x80
    elif VehicleProtectionFailSts == 0:
        payload[6] &= 0x7F

    if CityModeSts == 1:
        payload[7] |= 0x01
    elif CityModeSts == 0:
        payload[7] &= 0xFE
    if RwiperCntrl == 1:
        payload[7] |= 0x02
    elif RwiperCntrl == 0:
        payload[7] &= 0xFD
    if Rele2Sts == 1:
        payload[7] |= 0x04
    elif Rele2Sts == 0:
        payload[7] &= 0xFB
    if LH_Mirror_LED_Err == 1:
        payload[7] |= 0x08
    elif LH_Mirror_LED_Err == 0:
        payload[7] &= 0xF7
    if RH_Mirror_LED_Err == 1:
        payload[7] |= 0x10
    elif RH_Mirror_LED_Err == 0:
        payload[7] &= 0xEF
    if TurnIndicatorSts == 1:
        payload[7] |= 0x20
    elif TurnIndicatorSts == 0:
        payload[7] &= 0xDF
    if RainSensorFailSts == 1:
        payload[7] |= 0x80
    elif RainSensorFailSts == 0:
        payload[7] &= 0x7F
    # return can_pack(BH['STATUS_NBC'][0], BH['STATUS_NBC'][1], payload)
    return payload

def compose_NWM_NBC(payload,
                    Zero_byte=None,
                    SystemCommand=None,
                    ActiveLoadMaster=None,
                    EOL=None,
                    GenericFailSts=None,
                    P_ES=None,
                    D_ES=None):
    # payload = bytearray(8)
    if type(payload) is not bytearray:
        raise TypeError('Paylod is not a bytearray')
    if Zero_byte == 1:
        payload[0] = (Zero_byte)
    elif Zero_byte == 0:
        payload[0] = 0x00

    if SystemCommand == 0: # WU_wake_up_request
        payload[1] |= 0x00
    elif SystemCommand == 1: # Not_used
        payload[1] |= 0x01
    elif SystemCommand == 2: # SA_system_Stay_Active_req
        payload[1] |= 0x02
    elif SystemCommand == 3: # S_sytem_go_to_Sleep_req
        payload[1] |= 0x03
    elif SystemCommand == 0:
        payload[1] &= 0xFC

    if ActiveLoadMaster == 1:
        payload[1] |= 0x04
    elif ActiveLoadMaster == 0:
        payload[1] &= 0xFB
    if EOL == 1:
        payload[1] |= 0x08
    elif EOL == 0:
        payload[1] &= 0xF7
    if GenericFailSts == 1:
        payload[1] |= 0x10
    elif GenericFailSts == 0:
        payload[1] &= 0xEF
    if P_ES == 1:
        payload[1] |= 0x20
    elif P_ES == 0:
        payload[1] &= 0xDF
    if D_ES == 1:
        payload[1] |= 0x40
    elif D_ES == 0:
        payload[1] &= 0xBF
    # return can_pack(BH['NWM_NBC'][0], BH['NWM_NBC'][1], payload)
    return payload

def compose_NVO_STATUS_TOUCHPAD(payload,
                                GestureSpeed=None,
                                Xposition=None,
                                GestureType=None,
                                Push=None,
                                FingerPresent=None,
                                Yposition=None,
                                GestureStep=None):
    # payload = bytearray(8)
    if type(payload) is not bytearray:
        raise TypeError('Paylod is not a bytearray')
    if GestureSpeed is not None:
        if GestureSpeed != 0:
            payload[0] = ((((GestureSpeed) & 0xFF00) >> 8) & 0xFF)
            payload[1] = ((GestureSpeed) & 0xFF)
        elif GestureSpeed == 0:
            payload[0] = 0x00
            payload[1] = 0x00

    if Xposition is not None:
        if Xposition < 512 and Xposition > 0:
            payload[2] |= ((Xposition//2) & 0xFF)
            payload[3] |= (((Xposition % 2) & 0xFF) << 7)
        elif Xposition == 0:
            payload[2] &= 0x00
            payload[3] &= 0x7F

    if GestureType is not None:
        if GestureType < 9 and GestureType > 0:
            payload[4] |= GestureType
        elif GestureType == 0:
            payload[4] &= 0xF0

    if Push == 1:
        payload[4] |= 0x10
    elif Push == 0:
        payload[4] &= 0xEF
    if FingerPresent == 1:
        payload[4] |= 0x20
    elif FingerPresent == 0:
        payload[4] &= 0xDF
    if Yposition is not None:
        if Yposition < 512 and Yposition > 0:
            payload[3] |= ((Yposition//4) & 0xFF)
            payload[4] |= (((Yposition % 4) & 0xFF) << 6)
        elif Yposition == 0:
            payload[3] &= 0x80
            payload[4] &= 0x3F

    if GestureStep is not None:
        if GestureStep < 32 and GestureStep > 0:
            payload[5] |= (((GestureStep % 2) & 0xFF) << 3)
            payload[5] |= (((GestureStep//2) & 0xFF) << 4)
        elif GestureStep == 0:
            payload[5] &= 0x07
    # return can_pack(BH['NVO_STATUS_TOUCH'][0], BH['NVO_STATUS_TOUCH'][1], payload)
    return payload
