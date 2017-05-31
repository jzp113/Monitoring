#!/usr/bin/env python

import sqlite3
import smbus
import datetime

bus = smbus.SMBus(1)
address = 0x68

def getTemp(address):
   byte_tmsb = bus.read_byte_data(address,0x11)
   byte_tlsb = bin(bus.read_byte_data(address,0x12))[2:].zfill(8)
   return byte_tmsb+int(byte_tlsb[0])*2**(-1)+int(byte_tlsb[1])*2**(-2)

tempC = getTemp(address)
date_time = datetime.datetime.now()

conn = sqlite3.connect('tele.db')
c = conn.cursor()

c.execute("insert into temp (timestamp, temp) values (?, ?)", (date_time, tempC))
conn.commit()

conn.close()
