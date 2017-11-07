#!/usr/bin/python3
import pymysql
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import json
from urllib.parse import urlparse
from datetime import datetime

db = pymysql.connect("localhost","test","test","ico")
cursor = db.cursor()

r = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=ALL')
json_obj = json.loads(r.text)

for i in (json_obj):
    mysql_select = "insert into tickers (id, name, symbol, rank, price_usd, price_btc, 24h_volume_usd, market_cap_usd, available_supply, total_supply, percent_change_1h, percent_change_24h, percent_change_7d, last_updated, logged) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(mysql_select, (i['id'], i['name'], i['symbol'], i['rank'], i['price_usd'], i['price_btc'], i['24h_volume_usd'], i['market_cap_usd'], i['available_supply'], i['total_supply'], i['percent_change_1h'], i['percent_change_24h'], i['percent_change_7d'], i['last_updated'], datetime.utcnow()))
    db.commit()        
db.close()