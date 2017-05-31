#!/usr/bin/env python

#If 3 out of 5 most recent polls return over 25C - fans on 

import MySQLdb
import time

conn = MySQLdb.connect(host="localhost", user="logger", passwd="password", db="temperatures")
cursor = conn.cursor()
cursor.execute('select temperature,dateandtime from temperaturedata order by dateandtime desc limit 5;')

rows = cursor.fetchall()

timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
temps = [];
c = 0;
for row in rows:
    #print row[0]
    if row[0] > 22.2:
        print str(row[0]) + ' ' + 'fan_on'
        c = c + 1
    else:
        print str(row[0]) + ' ' + 'fan_off'
if c > 3:
    print 'fan is going on for 30 min'
    status = 'fan_on'
    print timestamp
    print status
    #cursor.execute("INSERT INTO temperaturedata(sensor) VALUES('no_fan')")
    cursor.execute('INSERT into temperaturedata (dateandtime, sensor) values (%s, %s)', (timestamp, status))
    conn.commit()
cursor.close()
conn.close()
