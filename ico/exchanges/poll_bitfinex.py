#!/usr/bin/python3
import pymysql
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import json
from urllib.parse import urlparse
from datetime import datetime

# db
db = pymysql.connect("localhost","test","test","ico")
cursor = db.cursor()

select_sql = "SELECT symbol FROM ico.coins where exchange like 'bitfinex'"
cursor.execute(select_sql)
results = cursor.fetchall()

# Make list of coins in the db
known_coins = []
for row in results:
    coin = row[0] 
    known_coins.append(coin)
# Remove duplicates
uniq_list = set(known_coins)
known_coins = uniq_list
print(len(known_coins))

# Get coins to compare with known_coins
r = requests.get('https://api.bitfinex.com/v1/symbols')
json_obj = json.loads(r.text)
print(r.text)
add_list = ""
for i in (json_obj):
    print(i)
    symbol = str(i).replace("btc","").replace("eth","").replace("usd","")
    if (symbol in known_coins or symbol in add_list):
        pass
    else:
        name = (symbol)
        print(name)
        mysql_select = "insert into coins (symbol, name, exchange, discovered, new) values(%s, %s, %s, %s, %s)"
        cursor.execute(mysql_select, (symbol, name, 'bitfinex', datetime.utcnow(), '1'))
        add_list =  add_list + symbol
    db.commit()        
db.close()