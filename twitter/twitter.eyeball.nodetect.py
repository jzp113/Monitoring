#display profile pics for matching terms on a webpage.
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from sys import argv
import webbrowser
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

#create web page
f = open("picurls.html", 'w')
message = """<html>
<head><meta http-equiv="refresh" content="3"></head>
<body><p>clear</p></body>
</html>"""
f.write(message)
f.write("\n")
f.truncate()

#open the page in browser
webbrowser.open_new_tab("picurls.html")

#Twitter API credentials
consumer_key            = ""
consumer_secret         = ""
access_token            = ""
access_token_secret     = ""


class StdOutListener(StreamListener):


    def on_data(self, data):
        description = json.loads(data)['user']['description']
        if not description:
            description = 'none'
        username = json.loads(data)['user']['screen_name']
        picurl = json.loads(data)['user']['profile_image_url'].replace("_normal.",".")
        profurl = ("https://twitter.com/%s" % username)
        f.write("<a href=\"")
        f.write(profurl)
        f.write("\"><img width = 150 height = 150 src = \"")
        f.write(picurl)
        f.write("\">")
        f.truncate()
        return True

 
def on_error(self, status):
    print status

if __name__ == '__main__':


    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=['search', 'terms'])


