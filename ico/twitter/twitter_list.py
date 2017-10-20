#!/usr/bin/python3
import pymysql
import json
from subprocess import call
import os
import fileinput

# db
db = pymysql.connect("localhost","test","test","ico")
cursor = db.cursor()	

# only new - no btc/eth/$$$$ - don't want them in the filters
select_sql = """SELECT lower(symbol) FROM ico.coins where (
symbol not like '300' and symbol  not like '$$$' and symbol not like 'btc' and symbol not like 'ltc' and 
symbol not like 'eth' and symbol not like '0x%' and new = 1 and active = 1);"""
cursor.execute(select_sql)
results = cursor.fetchall()

# Make list of coins in the db
known_coins = []
for row in results:
    coin = "$" + row[0] + " "
    known_coins.append(coin)

# Remove duplicates
uniq_list = set(known_coins)
known_coins = (uniq_list)
print(len(uniq_list))

add_list = list(uniq_list)

print(add_list[0:400])
