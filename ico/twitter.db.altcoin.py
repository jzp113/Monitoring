#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import webbrowser
import pprint
import MySQLdb
import time
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import re


conn = MySQLdb.connect("localhost","test","test","twitter",charset="utf8mb4",init_command='SET NAMES utf8mb4')
c = conn.cursor()

# authentication pieces
consumer_key            = ""
consumer_secret         = ""
access_token            = ""
access_token_secret     = ""


class StdOutListener(StreamListener):

    def on_data(self, data):
        try:
            data = (data).encode("utf-8","ignore")
            description = (json.loads(data)['user']['description'])
            name     = json.loads(data)['user']['name']
            text     = json.loads(data)['text']
            screen_name = json.loads(data)['user']['screen_name']
            profurl = ("https://twitter.com/%s" % screen_name) 
            followers = json.loads(data)['user']['followers_count']
            friends = json.loads(data)['user']['friends_count']
            source = json.loads(data)['source'].split(">")[-2].replace("</a","")
            location = json.loads(data)['user']['location']
            tweet_id = json.loads(data)['id']
            tweet_date = json.loads(data)['created_at']
            user_created = json.loads(data)['user']['created_at']
            tweet_at = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet_date,'%a %b %d %H:%M:%S +0000 %Y'))
            born = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(user_created,'%a %b %d %H:%M:%S +0000 %Y'))
            text = text.lower()  
            c.execute("INSERT INTO tweets (born,tweet_at,tweet_id,screen_name,name,text,description,profurl,followers,friends,source,location) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(born,tweet_at,tweet_id,screen_name,name,text,description,profurl,followers,friends,source,location))
            conn.commit()
            return True
        except:
            pass

def on_error(self, status):
    print(status)

if __name__ == '__main__':


    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=['$LTC','$DOGE','$VTC','$PPC','$FTC','$RDD','$NXT','$DASH','$POT','$BLK','$EMC2','$XMY','$AUR','$EFL','$GLD','$SLR','$PTC','$GRS','$NLG','$RBY','$XWC','$MONA','$THC','$ENRG','$ERC','$VRC','$CURE','$XMR','$CLOAK','$START','$KORE','$XDN','$TRUST','$NAV','$XST','$BTCD','$VIA','$UNO','$PINK','$IOC','$CANN','$SYS','$NEOS','$DGB','$BURST','$EXCL','$SWIFT','$DOPE','$BLOCK','$ABY','$BYC','$XMG','$BLITZ','$BAY','$BTS','$FAIR','$SPR','$VTR','$XRP','$GAME','$COVAL','$NXS','$XCP','$BITB','$GEO','$FLDC','$GRC','$FLO','$NBT','$MUE','$XEM','$CLAM','$DMD','$GAM','$SPHR','$OK ','$SNRG','$PKB','$CPC','$AEON','$ETH','$GCR','$TX ','$BCY','$EXP','$INFX','$OMNI','$AMP','$AGRS','$XLM','$BTA','$CLUB','$VOX','$EMC','$FCT','$MAID','$EGC','$SLS','$RADS','$DCR','$SAFEX','$BSD','$XVG','$PIVX','$XVC','$MEME','$STEEM','$2GIVE','$LSK','$PDC','$BRK','$DGD','$WAVES','$RISE','$LBC','$SBD','$BRX','$DRACO','$ETC','$STRAT','$UNB','$SYNX','$TRIG','$EBST','$VRM','$SEQ','$XAUR','$SNGLS','$REP','$SHIFT','$ARDR','$XZC','$NEO','$ZEC','$ZCL','$IOP','$DAR','$GOLOS','$UBQ','$KMD','$GBG','$SIB','$ION','$LMC','$QWARK','$CRW','$SWT','$TIME','$MLN','$ARK','$DYN','$TKS','$MUSIC','$DTB','$INCNT','$GBYTE','$GNT','$NXC','$EDG','$LGD','$TRST','$WINGS','$RLC','$GNO','$GUP','$LUN','$APX','$TKN','$HMQ','$ANT','$SC ','$BAT','$ZEN','$1ST','$QRL','$CRB','$PTOY','$MYST','$CFI','$BNT','$NMR','$SNT','$DCT','$XEL','$MCO','$ADT','$FUN','$PAY','$MTL','$STORJ','$ADX','$OMG','$CVC','$PART','$QTUM','$BCC','$USD','$611','$9COIN','$ABC','$ACP','$ADCN','$ADL','$AIB','$ALT','$APC','$APW','$ARC','$AURS','$BASH','$BBP','$BDL','$BEE','$BHC','$BITCF','$BIZ','$BLC','$BOST','$BQ ','$BRIT','$BTCHC','$BTCS','$BTLC','$BTXC','$BTQ','$CALC','$CCRB','$CESC','$CNB','$CNT','$CJ ','$CRC','$CRE','$CRPC','$CTIC2','$CTO','$DAS','$DDC','$DEEP','$DESH','$DEUS','$DRM8','$DRZ','$GAC','$EBH','$EC ','$ECN','$EL ','$ETX','$FCH','$FIRST','$FJC','$FUTC','$GARY','$GBC','$GBRC','$GLTC','$GMX','$GUC','$HEAT','$HOP','$ICOBI','$ILC','$IOT','$JIO','$JNS','$KGDC','$KLC','$KPL','$KRONE','$KRS','$LDCN','$LINDA','$LOG','$LOYAL','$LTS','$LEO','$LTCR','$MALC','$MBL','$MCAP','$MEN','$ETT','$MCR','$MHC','$MOIN','$MOON','$NDC','$NEWB','$NLC2','$NOTE','$NVC','$OD ','$OPNC','$OTC','$OTX','$PLBT','$PCS','$PGUC','$PHX','$PIE','$PIZZA','$POLY','$PRC','$PRES','$PROC','$PROPY','$PSB','$R ','$RBIES','$RKC','$REV','$RHFC','$ROBO','$ROLC','$SGC','$SIKKA','$RIYA','$SVC','$TCASH','$TCOIN','$TERA','$TERI','$TERRA','$TESLA','$TLAC','$TOA','$TRC','$TRUMP','$UNY','$USDT','$UTA','$VAK','$VRS','$VSX','$VUC','$WA ','$WCN','$WEX','$WOP','$XB ','$XBG','$XBP','$XBY','$XCXT','$XFC','$XGB','$XHI','$XID','$XNC','$XODUS','$XOM','$XOT','$XTO','$XTP','$XZA','$YOC','$ZBCN','$ZENI','$ZNY','$SMLY'], async=True)
