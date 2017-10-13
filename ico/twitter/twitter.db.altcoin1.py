#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import MySQLdb
import json
import time
import datetime

conn = MySQLdb.connect("localhost","test","test","twitter",charset="utf8mb4",init_command='SET NAMES utf8mb4')
c = conn.cursor()

# Auth
consumer_key            =  " "
consumer_secret         = " "
access_token            = " - "
access_token_secret     = " "

class StdOutListener(StreamListener):

    def on_data(self, data):
        screen_name = json.loads(data)['user']['screen_name']
        screen_name = (screen_name).encode("utf-8","ignore")
        json.loads(data)['created_at']
        tweet_date = json.loads(data)['created_at']
        tweet_at = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet_date,'%a %b %d %H:%M:%S +0000 %Y'))
        user_created = json.loads(data)['user']['created_at']
        born = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(user_created,'%a %b %d %H:%M:%S +0000 %Y'))
        user_mentions = json.loads(data)['entities']['user_mentions']
        urls = json.loads(data)['entities']['urls']
        urls = str(urls)
        symbols = json.loads(data)['entities']['symbols']
        symbols = str(symbols)
        description = (json.loads(data)['user']['description'])
        username     = json.loads(data)['user']['name']
        username = str(username)
        text     = json.loads(data)['text']
        text = text.lower()
        followers = json.loads(data)['user']['followers_count']
        friends = json.loads(data)['user']['friends_count']
        source = json.loads(data)['source'].split(">")[-2].replace("</a","")
        location = json.loads(data)['user']['location']
        tweet_id = json.loads(data)['id']
        statuses_count = json.loads(data)['user']['statuses_count']
        time_zone = json.loads(data)['user']['time_zone']
        utc_offset = json.loads(data)['user']['utc_offset']
        user_id = json.loads(data)['user']['id']
        verified = json.loads(data)['user']['verified']
        in_reply_to_screen_name = json.loads(data)['in_reply_to_screen_name']
        in_reply_to_status_id = json.loads(data)['in_reply_to_status_id']
        in_reply_to_user_id = json.loads(data)['in_reply_to_user_id']
        user_mentions = json.loads(data)['entities']['user_mentions']
        if (len(user_mentions)) < 1:
            user_mentions = 'na'
        else:
            user_mentions = str(json.loads(data)['entities']['user_mentions'])
        c.execute("INSERT INTO tweets (screen_name,tweet_at,born,urls,symbols,description, username, text, followers, friends, source, location, tweet_id, statuses_count, time_zone, utc_offset, user_id, verified, logged) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",([screen_name,tweet_at,born,urls,symbols,description, username, text, followers, friends, source, location, tweet_id, statuses_count, time_zone, utc_offset, user_id, verified, datetime.datetime.now()]))
        conn.commit()        

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['$rep ','$inxt ','$vsmold ','$cld ','$e4row ','$ndc ','$salt ','$dcnt ','$goku ','$hsr ','$odn ','$rup ','$oax ','$tgt ','$mgo ','$net ','$quiztum ','$dgd ','$adt ','$rpl ','$pts ','$hkg ','$ebtc ','$nmr ','$bis ','$ldm ','$san ','$hmq ','$mkr ','$nxx ','$gno ','$rare ','$lottereum ','$bnt ','$lun ','$bmchain token ','$bop ','$bmt ','$tft ','$alis ','$whl ','$ind ','$trx ','$dtc ','$xai ','$frd ','$zec ','$piex ','$pow ','$jet ','$swp ','$proxy token ','$silent notary token ','$kick ','$sggcoin ','$fuckold ','$exn ','$nxc ','$orme ','$edoge ','$btn ','$r token ','$bananacoin extended ','$1life ','$natcoin ','$dgb ','$hpc ','$pt ','$network ','$umc ','$cnx ','$32c7 ','$evr ','$gcc24 ','$f2utoken ','$r ','$bco ','$sht ','$ntc ','$graphgrailai token ','$fnl ','$ktn ','$cash poker pro ','$play ','$onek ','$pme ','$unify ','$vibe ','$vsl ','$benja ','$gd2 ','$geluk ','$rlx ','$swt ','$wancoin ','$smt ','$roc ','$eltc ','$mix ','$art ','$etherbtc ','$namo ','$eripple ','$krosscoin ','$qau ','$thongdee ','$funold ','$rspr ','$zsc ','$king ','$elm ','$rlc ','$ethb ','$vib ','$cdx ','$dragon exchange ','$real ','$rent token ','$eren yilmaz ','$gup ','$itt ','$fam ','$iwt ','$mln ','$graphgrail ai ','$cct ','$etbs ','$riya ','$ebitcoincash ','$rent ','$kss ','$ctcold ','$wancoi ','$erippl ','$det ','$ebitco ','$rgc ','$slipst ','$ebcsh ','$hgt ','$rub ','$hlm ','$fuckol ','$lotter ','$arxai ','$exrp2 ','$eltc2 ','$eltc3 ','$ven ','$yester ','$nugd ','$cuong  ','$ethere ','$ezec ','$nimfa ','$xpa ','$xbta ','$paypie ','$gntw ','$cash p ','$mol ','$betkin ','$mvc ','$boptol ','$evx ','$ccrb ','$tpt ','$paybit ','$exrp n ','$iqt ','$sggcoi ','$voise ','$ppp ','$bkb ','$ezec2 ','$elite ','$qvt ','$vezt ','$ply ','$air ','$mcd ','$btdx ','$tix ','$ctic3 ','$sdrn ','$oligar ','$nch ','$wtc ','$graphg ','$edash ','$spectr ','$lla ','$aion ','$ogt ','$enigma ','$aio ','$_yoc ','$bel ','$ets ','$moacto ','$centra ','$cnd ','$eether ','$bet ','$ecash ','$eeth ','$cindic ','$mdt ','$egold ','$eng ','$tanger ','$xin ','$28c8 ','$dazz '], async=True)
