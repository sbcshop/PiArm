#!/usr/bin/python3

'''
This file contains PiArm servo serial codes
Developed by - SB Components
http://sb-components.co.uk
'''

import re
import logging
import time
import threading
from serial_comm import SerialComm


class PiArm(SerialComm):
    """
    This is a class for handle servo command frames
    """
    STARTBYTE = 0x55
    BROADCAST = 0XFE

    SERVO_MOVE_TIME_WRITE = 0x01
    SERVO_MOVE_TIME_READ = 0x02
    SERVO_MOVE_TIME_WAIT_WRITE = 0x07
    SERVO_MOVE_TIME_WAIT_READ = 0x08
    SERVO_MOVE_START = 0x0B
    SERVO_MOVE_STOP = 0x0C
    SERVO_ID_WRITE = 0x0D
    SERVO_ID_READ = 0x0E
    SERVO_ANGLE_OFFSET_ADJUST = 0x11
    SERVO_ANGLE_OFFSET_WRITE = 0x12
    SERVO_ANGLE_OFFSET_READ = 0x13
    SERVO_ANGLE_LIMIT_WRITE = 0x14
    SERVO_ANGLE_LIMIT_READ = 0x15
    SERVO_VIN_LIMIT_WRITE = 0x16
    SERVO_VIN_LIMIT_READ = 0x17
    SERVO_TEMP_MAX_LIMIT_WRITE = 0x18
    SERVO_TEMP_MAX_LIMIT_READ = 0x19
    SERVO_TEMP_READ = 0x1A
    SERVO_VIN_READ = 0x1B
    SERVO_POS_READ = 0x1C
    SERVO_OR_MOTOR_MODE_WRITE = 0x1D
    SERVO_OR_MOTOR_MODE_READ = 0x1E
    SERVO_LOAD_OR_UNLOAD_WRITE = 0x1F
    SERVO_LOAD_OR_UNLOAD_READ = 0x20
    SERVO_LED_CTRL_WRITE = 0x21
    SERVO_LED_CTRL_READ = 0x22
    SERVO_LED_ERROR_WRITE = 0x23
    SERVO_LED_ERROR_READ = 0x24

    
    def __init__(self):
        super(PiArm, self).__init__()

    def _checksum(self, data, waitForResponse = True):
        """ calculate checksum and send data """
        c_sum = 0
        for byte in range (2,len(data)):
            c_sum += data[byte]
            
        data.append((~(c_sum)) & 0xFF)
        response = self.write(bytes(data), waitForResponse = waitForResponse)
        return response

    def connect(self, port, baudrate=115200):
        """ Open the port and connect """
        self.log.info('Connecting to PiArm on Port %s & baudrate %d..', port, baudrate)
        status = super(PiArm, self).connect(port, baudrate)
        if status == True:
            self.log.info('PiArm is Initialized')
        else:
            self.log.info('PiArm Initialization Failed..!!')

    def host2Servo(self, data):
        """ Convert 16 bit value to 8 bit values """
        servoData = [0,0]
        servoData[0] = data >> 8
        servoData[1] = data & 255
        return servoData

    def tempRead(self, ID):
        """ Read Servo Temperature """
        NOB = 3
        data = self._checksum([self.STARTBYTE, self.STARTBYTE, ID, NOB, self.SERVO_TEMP_READ])
        return data

    def voltageRead(self, ID):
        """ Read Servo Voltage """
        NOB = 3
        data = self._checksum([self.STARTBYTE, self.STARTBYTE, ID, NOB, self.SERVO_VIN_READ])
        return data

    def positionRead(self, ID):
        """ Read Servo Position """
        NOB = 3
        data = self._checksum([self.STARTBYTE, self.STARTBYTE, ID, NOB, self.SERVO_POS_READ])
        return data

    def adjustAngleOffset(self, ID=1, offset=0):
        """ Adjust angle offset to zero"""
        NOB = 4
        if offset < 0:
            offset = 256 + offset
        self._checksum([self.STARTBYTE, self.STARTBYTE, ID, NOB, self.SERVO_ANGLE_OFFSET_ADJUST, offset])

    def readAngleOffset(self, ID):
        """ Read Servo Angle Offset """
        NOB = 3
        response = self._checksum([self.STARTBYTE, self.STARTBYTE, ID, NOB, self.SERVO_ANGLE_OFFSET_READ])
        return response

    def readAngleLimit(self, ID):
        """ Read Servo Angle Limit """
        NOB = 3
        response = self._checksum([self.STARTBYTE, self.STARTBYTE, ID, NOB, self.SERVO_ANGLE_LIMIT_READ])
        return response

    def writeAngleLimit(self, ID=1, angleMin=0, angleMax=1000):
        """ Write Servo Angle Limit """
        NOB = 7
        minValue = self.host2Servo(angleMin)
        maxValue = self.host2Servo(angleMax)
        response = self._checksum([self.STARTBYTE, self.STARTBYTE, ID, NOB, self.SERVO_ANGLE_LIMIT_WRITE, minValue[1], minValue[0], maxValue[1], maxValue[0]])

    def readVolLimit(self, ID=1):
        """ Read Servo Voltage Limit """
        NOB = 3
        response = self._checksum([self.STARTBYTE, self.STARTBYTE, ID, NOB, self.SERVO_VIN_LIMIT_READ])
        return response

    def writeVolLimit(self, ID=1, voltMin=4500, voltMax=12000):
        """ Read Servo Voltage Limit """
        NOB = 7
        minValue = self.host2Servo(int(voltMin * 1000))
        maxValue = self.host2Servo(int(voltMax * 1000))
        self._checksum([self.STARTBYTE, self.STARTBYTE, ID, NOB, self.SERVO_VIN_LIMIT_WRITE, minValue[1], minValue[0], maxValue[1], maxValue[0]])

    def readTempLimit(self, ID):
        """ Read Servo Temperature Limit """
        NOB = 3
        response = self._checksum([self.STARTBYTE, self.STARTBYTE, ID, NOB, self.SERVO_TEMP_MAX_LIMIT_READ])
        return response

    def writeTempLimit(self, ID, temp):
        """ Write Servo Temperature Limit """
        NOB = 4
        self._checksum([self.STARTBYTE, self.STARTBYTE, ID, NOB, self.SERVO_TEMP_MAX_LIMIT_WRITE, temp])
        
    def torqueServo(self, ID, status):
        """ Enable/Disable Servo Torque """
        NOB = 4
        self._checksum([self.STARTBYTE, self.STARTBYTE, ID, NOB, self.SERVO_LOAD_OR_UNLOAD_WRITE, status], waitForResponse = False)

    def writeID(self, newID):
        """ Write Servo ID """
        NOB = 4
        self._checksum([self.STARTBYTE, self.STARTBYTE, self.BROADCAST, NOB, self.SERVO_ID_WRITE, newID])

    def readID(self):
        """ Read Servo ID """
        NOB = 3
        response = self._checksum([self.STARTBYTE, self.STARTBYTE, self.BROADCAST, NOB, self.SERVO_ID_READ])
        return response

    def servoWrite(self, ID=1, position=0, time=0):
        """ Write servo time and position values """
        NOB=7
        posValue = self.host2Servo(position)
        timeValue = self.host2Servo(time)
        self._checksum([self.STARTBYTE, self.STARTBYTE, ID, NOB, self.SERVO_MOVE_TIME_WRITE,
                       posValue[1], posValue[0], timeValue[1], timeValue[0]], waitForResponse = False)
        

    def ledWrite(self, ID = 1, status = 1):
        """ Write Led Status On/Off """
        NOB = 4
        self._checksum([self.STARTBYTE, self.STARTBYTE, ID, NOB, self.SERVO_LED_CTRL_WRITE, status], waitForResponse = False)

    def ledRead(self, ID = 1): 
        """ Read LED Status """
        NOB = 3
        response = self._checksum([self.STARTBYTE, self.STARTBYTE, ID, NOB, self.SERVO_LED_CTRL_READ])
        return response

    def write(self, data, waitForResponse=True,timeout=1, byteCount=0):
        """ Write Data to PiArm """
        self.log.debug('write: %s', data)
        responseLines = SerialComm.write(self, data, waitForResponse=waitForResponse,
                                                             timeout=timeout, byteCount=byteCount)
        return responseLines


        