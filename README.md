haqbus-protocol-simulator
=========================

script for simulating a message bus in python

* 9N1
* 9nth bit is 1 if address

Packet Layout
-------------

```
------------------------------------------------------------------------
| address (16 bit) | data_len (8bit) | data (0-255 byte) | CRC (8 bit) |
------------------------------------------------------------------------
```

0x00 - 0x0F magic addresses

Address Discovery
=================

Requirements:
- Master and bus must be up and running

```
(User)      Plugs new device
(Device)    sends AddressRequestPackage
address : 0x00 0x00 //magic address
data_len: 0x08
data: id(8bytes)

(Master)    answers with address
address: 0x00 0x01
data_len: 0x0C
data: id (8 bytes) address (2bytes) master_address (2bytes)


(Device) sends ack
address: master_address
data_len: 0x0A
data: id(8bytes) address(2bytes)

```

Device retries if:
* no answert after sending AddressRequestPackage (timedelta needs to be randomized)

Master ensures silence if:
* dectectes more collisions than usual

Master resends answer if:
* no ack has been recieved from client


