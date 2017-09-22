#!/usr/bin/python3
import pymysql
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import json

# Open database connection
db = pymysql.connect("localhost","test","test","ico" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sql = "SELECT * FROM coins"

cursor.execute(sql)
# Check which coin are in the db as known_coins
results = cursor.fetchall()
known_coins = []
for row in results:
    marketcurrency = row[0]
    basecurrency = row[1]
    created = row[2]
    isactive = row[3]
    exchange = row[4]
    
#Append coins to list known_coins
    known_coins.append(marketcurrency)
#print(known_coins)

#Get coins from bittrex to compare with know_coins
url = ('https://bittrex.com/api/v1.1/public/getmarkets')
r = requests.get(url)
json_obj = json.loads(r.text)
#print(json_obj)
for i in (json_obj['result']):
    marketcurrency = (i['MarketCurrency'])
    if marketcurrency not in known_coins:
        basecurrency = (i['BaseCurrency'])
        created = (i['Created'])
        isactive = (i['IsActive'])
        exchange = 'bittrex'
        
        #Insert record with new coins into ico.coins db
        
       #print('nope')
        #print(marketcurrency)
        #print(basecurrency)
       # print(created)
       # print(isactive)
       # print(exchange)     
# disconnect from server
db.close()