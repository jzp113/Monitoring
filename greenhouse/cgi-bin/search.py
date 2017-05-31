#!/usr/bin/env python

import numpy as np
import cgi, cgitb
cgitb.enable()          ## allows for debugging errors from the cgi scripts in the browser

form = cgi.FieldStorage()

## getting the data from the fields
start = form.getvalue('startdate')
end = form.getvalue('enddate')

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import MySQLdb
import pandas as pd
import matplotlib.pyplot as plt

conn = MySQLdb.connect(host="localhost", user="logger", passwd="password", db="temperatures")
cursor = conn.cursor()

query = "select dateandtime, temperature, humidity from temperaturedata WHERE dateandtime BETWEEN '%s' and '%s' ;" % (start, end)
df = pd.read_sql(query, con=conn)
conn.close()

df.index = df['dateandtime']
del df['dateandtime']

df.plot(title=start + ' - ' + end, style=['b-','r-'])
#i(style=['s-','o-','^-'],color=['b','r','y'],linewidth=[2,1,1])
#df.plot(title=start + ' - ' + end, style=['o','rx'])
table = pd.options.display.max_columns = 50
#plt.ylabel('Humidity %')
#plt.xlabel('Date')
#title = 'start
#plt.title(title)
plt.savefig('images/search.tmp.hum.png')


print("Content-type:text/html\r\n\r\n")
print("<html>")
print("<head><style></style><title>Greenhouse - Search</title><meta http-equiv='refresh' content='15'></head>")
print("<body style='background-color:#eff9e3;'><div align=center><h3>Greenhouse Temp/Humidity")
print("<table style='width:100%'><tr><th><img src='../../images/search.tmp.hum.png' alt='Temp/Humidity' height='542' width='75%'></th></tr></table>")
print("</body>")
print("</html>")
