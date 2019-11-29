import imgkit
import os
WRITER_PATH="/var/www/html/text/writerdocs"
THUMB_PATH="/var/www/html/static/writer_thumbs"
options={
    'height':'300',
    'width':'500',
    'encoding':'utf-8',
    "xvfb": ""
}

files = os.listdir(WRITER_PATH)
for i in files:
    print(WRITER_PATH+"/"+i, THUMB_PATH+"/"+i+"_thumb.png", options)
    imgkit.from_file(WRITER_PATH+"/"+i, THUMB_PATH+"/"+i+"_thumb.png", options=options)
