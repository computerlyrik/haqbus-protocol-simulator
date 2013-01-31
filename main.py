#!/usr/bin/python

from time import clock, time, sleep
from thread import start_new_thread
import logging as logger
import random 
import threading
logger.basicConfig(level=logger.DEBUG)
logger.warning('Watch out!') # will print a message to the console
logger.info('I told you so') # will not print anything

""" Messages:

  1 Byte command | n bytes data | 2 Bytes CRC

  Commands:

  01 = Address Request
  data will contain random id

  10 = Address Response
  data = random id + new address

  0F = Got Address
  data = id + address
  
  F0 = Info request
  data = address 
"""

class Bus(threading.Thread):
  #Initially add master on bus
  def __init__(self):
    self.participants = []
    self.timer = time()
    threading.Thread.__init__(self)
    
  def run(self):
    while 1:
      sleep(random.random()/1000)
      self.write(None,bytes(0x00))
    
  #Write a new message on bus
  #colission if messages too fast 
  def write(self,client,msg):
    if (time() - self.timer ) < 0.00007:
      logger.info(time() - self.timer)
      logger.info("collision! " + str(msg[0]))

    else:
      for p in self.participants:
        if p != client:
          p.receive(msg)
    self.timer = time()

  #connect new devices to bus
  def connect(self, client):
    self.participants.append(client)

class Master(threading.Thread):
# table: address | slave | verified
  def __init__(self,bus):
    self.bus = bus
    self.bus.connect(self)
    self.slaves = dict()
    threading.Thread.__init__(self)
  def receive(self,req):
    if req[0] == 1:
      logger.info("address request from " + str(req[1]))
      res = bytearray()
      res.append(0x10)
      res.append(req[1]) #re-send identification
      res.append(random.getrandbits(8))
      self.bus.write(self,res)

class Slave(threading.Thread):
  def __init__(self, bus):
    self.bus = bus
    self.bus.connect(self)
    self.address = None
    self.id = random.getrandbits(8)
    threading.Thread.__init__(self)
    
  def run(self):
    for n in range(1,20):
      if self.address != None: continue
      self.dhcprequest()
      sleep(n/100)
    logger.debug("address "+str(self.address)+"--------------------")

  def receive(self,msg):
    if msg[0] == 16 and msg[1] == self.id:
      logger.info(str(self.id)+" got address "+str(msg[2]))
      self.address = msg[2]
      self.id = None #reset id to not react anymore on this

  def dhcprequest(self):
    logger.debug(str(self.id) + " sending request")
    msg = bytearray()
    msg.append(0x01)
    msg.append(self.id)
    self.bus.write(self,msg)
    
    
  def description(self):
    return "A standard slave with one input and one output"
  def inputs(self):
    return "foobar"
#address
#version
#description

b = Bus()
b.start()

m = Master(b)
m.start()

for n in range(0,10):
  s = Slave(b)
  s.start()

while 1:
   pass


