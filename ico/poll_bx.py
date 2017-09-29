#!/usr/bin/python3
import pymysql
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import json
from urllib.parse import urlparse
from datetime import datetime
import pprint

# db
db = pymysql.connect("localhost","test","test","ico")
cursor = db.cursor()

select_sql = "SELECT symbol FROM ico.coins where exchange like 'bx'"
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
print("------")
        
# Get coins from bx
r = requests.get('https://bx.in.th/api/pairing/')
json_obj = json.loads(r.text)
add_list = "ETH "
pairing_ids = []
for item in json_obj:
    id = item
    #print(id)
    pairing_ids.append(id)
    
# Remove duplicates
uniq_ids = set(pairing_ids)
#print(len(uniq_ids))
    
for pairing_id in uniq_ids:
    print(pairing_id)
    symbol = (json_obj[pairing_id]['secondary_currency'])
    name = symbol
    if (symbol in known_coins or symbol in add_list):
        print(symbol)
        pass
    else:
        name = symbol
        mysql_select = "insert into ico.coins (symbol, name, exchange, discovered, new) values(%s, %s, %s, %s, %s)"
        cursor.execute(mysql_select, (symbol, name, 'bx', datetime.utcnow(), '1'))
        add_list = add_list + " " + (symbol)
    db.commit() 
db.close()

