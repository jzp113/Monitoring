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

select_sql = "SELECT marketcurrency FROM cryptopia"
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
        
# Get coins from cryptopia
r = requests.get('https://www.cryptopia.co.nz/api/GetCurrencies')
json_obj = json.loads(r.text)

for item in json_obj['Data']:
    marketcurrency = item['Symbol']
    if (marketcurrency) in known_coins:
        pass
    else:
        name = (item['Name'])
        status = (item['Status'])
        mysql_select = "insert into cryptopia (marketcurrency, basecurrency, created, status, name, exchange, discovered) values(%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(mysql_select, (marketcurrency, 'na', '2014-01-01 00:00:00', status, name, 'cryptopia', datetime.utcnow()))
    db.commit()        
db.close()