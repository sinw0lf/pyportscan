#!/usr/bin/python 

# does a portscan of the entire port range using threads and netcat

import logging
import random
import threading
import time
import subprocess
import re
import sys


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )

class ActivePool(object):
    def __init__(self):
        super(ActivePool, self).__init__()
        self.active = []
        self.lock = threading.Lock()
    def makeActive(self, name):
        with self.lock:
            self.active.append(name)
            #logging.debug('Running: %s', self.active)
    def makeInactive(self, name):
        with self.lock:
            self.active.remove(name)
            #logging.debug('Running: %s', self.active)

def scanner(s, pool ,ip, port):
    #logging.debug('Waiting to join the pool')
    with s:
        name = threading.currentThread().getName()
        pool.makeActive(name)
        pingcommand = "nc -nvv -w 1 -z "+ip+" "+port
        #print pingcommand
        check=subprocess.Popen(pingcommand,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).communicate()

        output1=str(check)
        if "open" in output1 :
            print ip+" port "+port+" is open"
        #time.sleep(0.1)
        pool.makeInactive(name)



if len(sys.argv) <> 2:
    print "Please supply an ip e.g. ./pyportscan x.x.x.x" 

else :
    starttime=time.time()
    ip = str(sys.argv[1])
    #ip ="10.11.1.220"
    pool = ActivePool()
    s = threading.Semaphore(10) #set thread max limit here
    for i in range(1,65535):
        port = str(i)
        #print port
        t = threading.Thread(target=scanner, name=str(i), args=(s, pool, ip, port))
        time.sleep(0.1)
        t.start()
    endtime=time.time()
    print ((endtime-starttime)*60)+" minutes"
print "done"




