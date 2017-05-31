#!/usr/bin/env python

import sqlite3
import time
from time import sleep       
import RPi.GPIO as GPIO     

time.sleep(20)
GPIO.setmode(GPIO.BCM)     
GPIO.setup(17, GPIO.IN)
GPIO.setup(4, GPIO.OUT)

conn = sqlite3.connect('/root/auto.db')
c = conn.cursor()

timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

i = GPIO.input(17)
if i == 0:
    print timestamp + ' normal'
else:
    print timestamp + ' water on'
    c.execute("insert into events (Date,Water) values (?, ?)", (timestamp, 1))    
    conn.commit() 
    GPIO.output(4, 0)
    time.sleep(850)
    c.execute("insert into events (Date,Water) values (?, ?)", (timestamp, 0))
    conn.commit()
    GPIO.output(4, 1)
    print timestamp + ' water off'
GPIO.cleanup()
conn.commit()
conn.close()
