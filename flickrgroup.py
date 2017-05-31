#Downloads highest resolution pics available from the Flickr Groups specified. Images with faces detected via Google Vision are added to the db
#Needs Flickr API key, Google Vision API and postgresql credentials.  
import flickrapi
import requests
import pprint
import psycopg2
import hashlib
import wget
import os
import piexif
import datetime
import os
import base64
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from PIL import Image 
from PIL import ImageDraw
import glob
import PIL
import httplib2

from apiclient.discovery import build
from oauth2client.client import GoogleCredentials

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/path/to/google/vision-credentials.json'

#flickr auth
api_key = ''
secret = ''
flickr = flickrapi.FlickrAPI(api_key, secret, format='parsed-json')

API_DISCOVERY_FILE = 'https://vision.googleapis.com/$discovery/rest?version=v1'
http = httplib2.Http()

credentials = GoogleCredentials.get_application_default().create_scoped(
    ['https://www.googleapis.com/auth/cloud-platform'])
credentials.authorize(http)

service = build('vision', 'v1', http, discoveryServiceUrl=API_DISCOVERY_FILE)

for group_id in ['*target group here*']:
    page = 1
    success = True

    #Get list of existing photos from database
    conn = psycopg2.connect("dbname='' user='' host='' password='' port=''")
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("""SELECT filepath from raw_images""")
    
    #Add existing db records to 'files' 
    files = cur.fetchall()
    group_pool_photos = []
    
    #Get list of photos from Flickr for group and store tehm in group_pool_photos
    while True:
        response = flickr.groups.pools.getPhotos(group_id=group_id, page=page, perpage='300')
        if response['stat'] != 'ok':
            print 'Error occurred in flickr.groups.pools.getPhotos'
            print(response)
            success = False
            break

        if len(response['photos']['photo']) == 0:
            break

        group_pool_photos.extend(response['photos']['photo'])
        page += 1

    if success:
        print 'Total photos {}'.format(len(group_pool_photos))

    #diff filelist db id's with new flickr photo ids to download only new photos 
    filelist = str(files).strip('[]')  
    for photo in group_pool_photos:
        if photo['id'] in filelist:
            print 'Found'
        else:
            photoinfo = flickr.photos.getInfo(photo_id=photo['id'])
            description = (photoinfo['photo']['description']['_content'])
            if not description:
                description = 'na'
            taken = photoinfo['photo']['dates']['taken']
            path_alias = photoinfo['photo']['owner']['path_alias']
            if not path_alias:
                path_alias = 'na'
            title = photoinfo['photo']['title']['_content']
            picsize = flickr.photos.getSizes(photo_id=photo['id'])
            picurl = (picsize['sizes']['size'][-1]['source'])
            fname = picurl.split("/")[-1]

            if os.path.isfile(fname):
                print 'already downloaded'
            else:
                filename = wget.download(picurl)
 
    #Compute hash of original file
            hasher = hashlib.sha256()
            with open(fname, 'rb') as afile:
                buf = afile.read()
                hasher.update(buf)
                hash_img = (hasher.hexdigest())           
        
    #Remove exif data
            piexif.remove(fname, fname)
        
    #Reduce the files that are over 4/8 MB        
            statinfo = os.stat(fname)
            filesize = statinfo.st_size
            if filesize > 8000000:
                basewidth = 6000
                img = Image.open(fname)
                wpercent = (basewidth / float(img.size[0]))
                hsize = int((float(img.size[1]) * float(wpercent)))
                img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
                img.save(fname)
            if filesize > 4000000:
                basewidth = 4000
                img = Image.open(fname)
                wpercent = (basewidth / float(img.size[0]))
                hsize = int((float(img.size[1]) * float(wpercent)))
                img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
                img.save(fname)        
   
    #Submit photo to Google Vision for face detection
            with open(fname, 'rb') as image:
                image_content = base64.b64encode(image.read())
                service_request = service.images().annotate(
                    body={
                        'requests': [{
                            'image': {
                                'content': image_content
                                },
                            'features': [{
                                'type': 'FACE_DETECTION',
                                'maxResults': 5,
                            }]
                        }]
                    })
                response = service_request.execute()
                for results in response['responses']:
                    if 'faceAnnotations' not in results:
                        print 'no face found'
                        date_image_inserted = datetime.date.today()
                        is_tagged = 'f'                        
                        cur.execute('INSERT INTO raw_images (filepath, hash_img, date_image_inserted, date_image_taken, is_tagged) VALUES (%s, %s, %s, %s, %s)', ("noface_" + fname, hash_img, date_image_inserted, taken, is_tagged))
                    else:
                        print results['faceAnnotations'][0]['detectionConfidence']
                        print 'face detected'                        
                        date_image_inserted = datetime.date.today()
                        is_tagged = 'f'
                        cur.execute('INSERT INTO raw_images (filepath, hash_img, date_image_inserted, date_image_taken, is_tagged) VALUES (%s, %s, %s, %s, %s)', (fname, hash_img, date_image_inserted, taken, is_tagged))
