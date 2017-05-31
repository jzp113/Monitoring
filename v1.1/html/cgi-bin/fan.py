#!/usr/bin/env python

#If 3 out of 5 most recent polls return over 23C - fans on 

import sqlite3
import time
import RPi.GPIO as GPIO

time.sleep(10)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

conn = sqlite3.connect('/root/auto.db')
c = conn.cursor()

timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

c.execute("select Temp from events where temp <> '25.432' order by Date desc limit 5" )
conn.commit()

rows = c.fetchall()

count = 0;
for row in rows:
    if row[0] > 28:
        print timestamp + ' ' + str(row[0]) + ' ' + 'fan_on'
        count = count + 1
    else:
        print str(row[0]) + ' ' + 'fan_off'
if count > 3:
    c.execute("INSERT into events (Date,Fan) values (?, ?)", (timestamp, 25.4321))
#    conn.commit()
    GPIO.output(18, GPIO.LOW)
    time.sleep(850)
    c.execute("insert into events (Date,Fan) values (?, ?)", (timestamp, 0))
else:
    c.execute("insert into events (Date,Fan) values (?, ?)", (timestamp, 0))
#    conn.commit()

GPIO.output(18, GPIO.HIGH)
print timestamp + ' fan_off'
GPIO.cleanup()
conn.commit() 
conn.close()
