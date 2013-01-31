#!/usr/bin/python

from time import clock, time, sleep
import logging as logger
import random 

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

  0F = Info request
  data = address 
"""

class Bus(object):
  #Initially add master on bus
  def __init__(self):
    self.participants = []
    self.timer = time()

  #Write a new message on bus
  #colission if messages too fast 
  def write(self,client,msg):
    if (time() - self.timer ) < 0.000007:
      logger.info(time() - self.timer)
      logger.info("collision! ")

    else:
      for p in self.participants:
        if p != client:
          p.receive(msg)
    self.timer = time()

  #connect new devices to bus
  def connect(self, client):
    self.participants.append(client)

class Master:
  def __init__(self,bus):
    self.bus = bus
    self.bus.connect(self)
    self.slaves = dict()
  def receive(self,req):
    if req[0] == 1:
      logger.info("address request from " + str(req[1]))
      res = bytearray()
      res.append(0x10)
      res.append(req[1]) #re-send identification
      res.append(random.getrandbits(8))
      self.bus.write(self,res)

class Slave:
  def __init__(self, bus):
    self.address = None
    self.id = random.getrandbits(8)
    self.bus = bus
    self.bus.connect(self)
    self.dhcprequest()
  def receive(self,msg):
    if msg[0] == 16 and msg[1] == self.id:
      logger.info("got address "+str(msg[2]))
      self.address = msg[2]
    if self.address == None:
      self.dhcprequest()
      return

      
  def dhcprequest(self):
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
m = Master(b)

for n in range(2, 10):
  Slave(m.bus)
  
while 1:
  sleep(random.random()/1000)
  b.write(None,bytes(0x00))

