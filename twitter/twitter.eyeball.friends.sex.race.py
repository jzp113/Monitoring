from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from sys import argv
import webbrowser
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

#create web page
f = open("out.html", 'w')
message = """<html>
<head><meta http-equiv="refresh" content="3"></head>
<body><p>clear</p></body>
</html>"""
f.write(message)
f.write("\n")
f.truncate()

#open the page in browser
webbrowser.open_new_tab("out.html")

#Twitter API credentials
consumer_key            = ""
consumer_secret         = ""
access_token            = ""
access_token_secret     = ""

#Face++ API credentials
face_api_key = ''
face_api_secret = ''

class StdOutListener(StreamListener): 


    def on_data(self, data):
        print '==='
        username = json.loads(data)['user']['screen_name']
        friends = json.loads(data)['user']['friends_count']    
        followers = json.loads(data)['user']['followers_count']    
        #print followers
        if friends < 100:
            print 'nofriends ' + username
        else:
            print 'buddies ' + username
            description = json.loads(data)['user']['description']
            if not description:
                description = 'none'
             #location = json.loads(data)['user']['location']
            
            #if not username:
            #    username = 'none'

            picurl = json.loads(data)['user']['profile_image_url'].replace("_normal.",".")
            profurl = ("https://twitter.com/%s" % username)
            faceurl = "https://apius.faceplusplus.com/v2/detection/detect?url=%s&api_secret=%s&api_key=%s&attribute=gender,race" % (picurl, face_api_secret, face_api_key)
            r = requests.get(faceurl)
            if "gender" in r.text:
                gender = (json.loads(r.text)['face'][0]['attribute']['gender']['value'])
                race = (json.loads(r.text)['face'][0]['attribute']['race']['value'])
                if ("GENDER" in gender and "RACE" in race):
                    print gender + " " + race + " " + username + " " + description +  " " + profurl
                    f.write("<a href=\"")
                    f.write(profurl)
                    f.write("\"><img width = 150 height = 150 src = \"")
                    f.write(picurl)
                    f.write("\">")
                    print username
                    print picurl
                    print "---"
                    print (data)
                    f.truncate() 
                    return True                    
                else:
                    print 'not xxxxxxx ' + username
            else:
                print 'noface ' + username
    #        mediaurl = json.loads(data)["media"]["media_url"]
                


def on_error(self, status):
    print status

if __name__ == '__main__':

    try:
        l = StdOutListener()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, l)
        stream.filter(track=['search_terms'])
    except:
        pass

