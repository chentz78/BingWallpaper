#! /usr/bin/env python3.6
# -*- coding: utf-8 -*-

import sys
import re
import os
import json
import requests
import urllib.request
import datetime as dt

def imgAjusts(fp, text, fpout):  
  c = f'identify -format %w {fp}'
  iw = int(os.popen(c).read())
  c = f'''
convert -size {iw}x35 xc:none -gravity southwest \
-font Georgia -pointsize 20 \
-stroke black -strokewidth 2 -annotate 0 '{text}' \
-background none -shadow {iw}x2+0+0 +repage \
-stroke none -fill white -annotate 0 '{text}' \
{fp}  +swap -gravity southwest -geometry +7+20 \
-composite -quality 95 {fpout} 
''' #-filter Lanczos2 -resize 1920x1080!
  os.system(c)
  
idxDay = int(sys.argv[1]) if len(sys.argv) > 1 else 0
dtNow = dt.datetime.now()
if idxDay > 0:
  dtNow = (dtNow - dt.timedelta(days=idxDay))

dtNow = dtNow.strftime("%d/%m/%Y")

URL = f"http://www.bing.com/HPImageArchive.aspx?format=js&idx={idxDay}&n=1"

image_data = json.loads(requests.get(URL).text)
image_url = 'http://www.bing.com' + image_data['images'][0]['url']

# url for better quality image
image_download_url = 'http://www.bing.com/hpwp/' + image_data['images'][0]['hsh']

image_name = image_url[re.search("=", image_url).end():re.search('\.jpg\&', image_url).start()] + '.jpg'

dir_path = os.environ['HOME'] + '/Pictures/Bing_Pic_of_the_Day/' 

#check if the directory exists and create it otherwise
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

file_path = dir_path + image_name
finalWLP = dir_path+'current.jpg'

try:
    # try downloading by first url(better quality)
    urllib.request.urlretrieve(image_url, filename=file_path)
except urllib.error.HTTPError:
    # if first url fails
    urllib.request.urlretrieve(image_url, filename=file_path)
t = image_data['images'][0]['copyright']
image_desc = t[:re.search("\(", t).start()].strip()
image_cRight = t[re.search("\(", t).end():re.search("\)", t).start()].strip()
imgAjusts(file_path, f'{image_desc}\nBing: {dtNow}', finalWLP)

command = 'gsettings set org.gnome.desktop.background picture-uri file://'+finalWLP
os.system(command)