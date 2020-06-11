# -*- coding: utf8 -*-

from pirc522 import RFID as RFID_driver
from threading import Thread, Event
import time

class RfidReader(Thread) :
    
    def __init__(self) :
        
        Thread.__init__(self)
        
        self.rdr = RFID_driver()
        
        self.signal = None
        self.callback = None
        
        self.stop_flag = Event()
        
        self.identical_tag_delay = 2 #s
        
        self.last_detection_tag = None
        self.last_detection_tag = time.time()

        
        
 
    
    def run(self):
        
        while self.stop_flag.is_set() is False :
                
            # Wait for tag
            self.rdr.wait_for_tag()
            
            # Analyse tag
            valid_tag = False
            (error, tag_type) = self.rdr.request()
            if not error:
                (error, tag) = self.rdr.anticoll()
                if not error:
                    tag = int(''.join([str(i) for i in tag]))
                    print(tag)
                    if tag != self.last_detection_tag :
                        valid_tag = True
                    else : 
                        if ( time.time() - self.last_detection_time ) > self.identical_tag_delay :
                            valid_tag = True
                
            # Action
            if valid_tag is True : 
                self.last_detection_tag = tag
                self.last_detection_time = time.time()
                if self.callback is not None : self.callback(tag)
                if self.signal is not None : self.signal.emit(tag)
            else :
                time.sleep(0.2)
                
                
    def stop(self):
        
        self.stop_flag.set()

            

if __name__ == "__main__" :
    
    a=RfidReader()
    a.callback = print
    a.start()
    import time
    while True : 
        time.sleep(1)
