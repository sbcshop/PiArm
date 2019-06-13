#!/usr/bin/python3

'''
This file handle serial read and write
Developed by - SB Components
http://sb-components.co.uk
'''

import serial
import threading
import logging
from tkinter import messagebox

class SerialComm(object):
    """ Low level serial operations """
    log = logging.getLogger('piarm.serial.SerialComm')
    # Default timeout for serial reading(seconds)
    timeout = 5

    def __init__(self, handlerNotification=None, *args, **kwargs):
        """ Constructor """
        self.alive = False
        self.timeout = 0.01
        self._dataRecieved = False
        self._responseEvent = None
        self._expectResponse = None
        self._response = None
        self._rxData = []
        self._notification = []
        self._txLock = threading.Lock()
        self.handlerNotification = handlerNotification

    def connect(self, commPort, baud = 115200):
        """ Connects to the device """
        try:
            self.serial = serial.Serial(port=commPort,baudrate=baud,timeout=self.timeout)
            self.alive = True
            self.rxThread = threading.Thread(target=self._readLoop)
            self.rxThread.daemon = True
            self.rxThread.start()
            return True
            
        except serial.serialutil.SerialException:
            messagebox.showerror("Port Error", "Couldn't Open Port..!!")

    def disconnect(self):
        """ Stops read thread, waits for it to exit cleanly and close serial port """
        self.alive = False
        self.rxThread.join()
        self.serial.close()
        self.log.info('PiArm Disconnected Succesfully..!!')

    def _handleLineRead(self, line, checkResponse=True):
        if self._responseEvent and not self._responseEvent.is_set():
            self._response = line
            if not checkResponse:
                # End of response reached; notify waiting thread
                self.log.debug('response: %s', self._response)
                self._responseEvent.set()
        else:
            # Nothing was waiting for this - treat it as notification
            self._notification.append(line)
            if self.serial.inWaiting() == 0:
                # No more chars for this notification
                #self.log.debug('notification: %s', self._notification)
                self.log.debug('notification: Serial Device Connected')
                #self.handlerNotification(self._notification)
                self._notification = []

    def _readLoop(self):
        """ Read thread main loop """
        try:
            while self.alive:
                data = self.serial.read(1)
                if data != b'':
                    self._dataRecieved = True
                    self._rxData.append(data)
                elif data == b'' and self._dataRecieved == True:
                    self._dataRecieved = False
                    self._handleLineRead(self._rxData, checkResponse = False)
                    self._rxData = []
                            
        except serial.SerialException as err:
            self.alive = False
            try:
                self.serial.close()
            except Exception:
                pass

    def write(self, data, waitForResponse=True, timeout= 1, byteCount= 0):
        """ Write data to serial port """
        with self._txLock:
            if waitForResponse:
                self._response = []
                self._responseEvent = threading.Event()
                self.serial.write(data)
                if self._responseEvent.wait(timeout):
                    self._responseEvent = None
                    self._expectResponse = False
                    return self._response
                else:
                    self._responseEvent = None
                    self._expectResponse = False
                    # raise Timeout Exception
            else:
                self.serial.write(data)
            
            
    
        
    
