# -*- coding: utf8 -*-

import sys
print('iij',sys.version)
from pirc522 import RFID as RFID_driver
from threading import Thread, Event
import time

class RfidReader :
    
    def __init__(self,callback) :
        
        self.rdr = RFID_driver()
        
        self.callback = callback
        self.stopFlag = Event()
        
        self.rfidThread = RfidThread(self)
        self.rfidThread.start()
        

    def waitForTag(self) :
    
        while self.stopFlag.is_set() is False :
        
            self.rdr.wait_for_tag()
            (error, tag_type) = self.rdr.request()
            if not error:
                (error, uid) = self.rdr.anticoll()
                if not error:
                    uid = int(''.join([str(i) for i in uid]))
                    break
            time.sleep(0.2)
        
        return uid
    
    
    def stopThread(self):
        self.stopFlag.set()


class RfidThread(Thread):
        
    def __init__(self,reader):
        Thread.__init__(self)
        self.reader = reader
        self.lastDetectionTime = 0
        self.lastDetectionTag = 0
        self.minDelay = 2 #sec
        
        
    def run(self):
        while self.reader.stopFlag.is_set() is False :
            tag = self.reader.waitForTag()
            if tag != self.lastDetectionTag :
                self.detection(tag)
            else :
                if (time.time() - self.lastDetectionTime) > self.minDelay :
                    self.detection(tag)
            time.sleep(0.1)
        
        
    def detection(self,tag):
        self.lastDetectionTag = tag
        self.lastDetectionTime = time.time()
        self.reader.callback(tag)
            

if __name__ == "__main__" :
    a=RfidReader()
    while True :
        print(time.time(),a.waitForTag())
