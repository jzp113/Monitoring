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

select_sql = "SELECT marketcurrency FROM ccex"
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
r = requests.get('https://c-cex.com/t/api_pub.html?a=getmarkets')
json_obj = json.loads(r.text)

for i in (json_obj['result']):
    marketcurrency = (i['MarketCurrency'])
# Only making a list of coins trading in BTC for now
    if (i['MarketCurrency']) in known_coins or ((i['BaseCurrency']) != 'BTC') :
        pass
    else:
        print(marketcurrency + ' nope')
        basecurrency = (i['BaseCurrency'])
        created = (i['Created'])
        isactive = (i['IsActive'])
        name = (i['MarketCurrencyLong'])
        # Exchange column 
        marketcurrency = (i['MarketCurrency']) 
        mysql_select = "insert into ccex (marketcurrency, basecurrency, created, status, name, exchange, discovered) values(%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(mysql_select, (i['MarketCurrency'], i['BaseCurrency'], i['Created'], i['IsActive'], name, 'ccex', datetime.utcnow()))
    db.commit()        
db.close()