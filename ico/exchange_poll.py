#!/usr/bin/python3
import pymysql
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import json

#db
db = pymysql.connect("localhost","test","test","ico")
cursor = db.cursor()
select_sql = "SELECT marketcurrency FROM coins"
cursor.execute(select_sql)
results = cursor.fetchall()

# Make list of coins in the db
known_coins = []
for row in results:
    coin = row[0] 
    known_coins.append(coin)
  
#Remove dups trading in both ETH/BTC - can track separately later if nec
uniq_list = set(known_coins)
known_coins = uniq_list

#Get coins from bittrex to compare with known_coins
url = ('https://bittrex.com/api/v1.1/public/getmarkets')
r = requests.get(url)
json_obj = json.loads(r.text)

for i in (json_obj['result']):
    marketcurrency = (i['MarketCurrency'])
    if (i['MarketCurrency']) in known_coins:
        pass
    else:
        print(marketcurrency + ' nope')
        basecurrency = (i['BaseCurrency'])
        created = (i['Created'])
        isactive = (i['IsActive'])
        exchange = 'bittrex'
        marketcurrency = (i['MarketCurrency']) 
        mysql_select = "insert into coins (marketcurrency, basecurrency, created, isactive, exchange) values(%s, %s, %s, %s, %s)"
        cursor.execute(mysql_select, (i['MarketCurrency'], i['BaseCurrency'], i['Created'], i['IsActive'], exchange))

db.commit()
db.close()