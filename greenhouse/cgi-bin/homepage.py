#!/usr/bin/env python

import MySQLdb
import pandas as pd

conn = MySQLdb.connect(host="localhost", user="logger", passwd="password", db="temperatures")
cursor = conn.cursor()
cursor.execute('select dateandtime, temperature, humidity from temperaturedata order by dateandtime desc limit 1;');
rows = cursor.fetchall()
cursor.close()
conn.close()
for row in rows:
    current = row
#create web page
f = open("/var/www/html/index.html", 'w')
message = """<html>
<head>
<script>
function startTime() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('txt').innerHTML =
    h + ':' + m + ':' + s;
    var t = setTimeout(startTime, 500);
}
function checkTime(i) {
    if (i < 10) {i = '0' + i};  // add zero in front of numbers < 10
    return i;
}
</script>
<style>
</style>
<title>Greenhouse</title><meta http-equiv="refresh" content="15">
</head>

<body style="background-color:#eff9e3;" onload="startTime()">

<div align=left><h3>Temperature & Humidity</h3></div></div>
    <div style="text-align:left;">
        <form action="/cgi-bin/search.py" method="get">
            Start:  <input type="date" name="startdate" style="text-align:center;">
            End:  <input type="date" name="enddate" style="text-align:center;">
            <input type="submit" value="Search">
        </form>
<form action="index.html">
    <input type="submit" value="Clear" />
</form>
    </div>
<div id="txt"></div>
</body>

</html>"""
f.write("<h2>")
f.write(message)
f.write("</h2>")
f.write("\n")
f.write(str(current))
f.write("\n")
f.truncate()
