import imgkit
import os
WRITER_PATH="/var/www/html/text/writerdocs"
THUMB_PATH="/var/www/html/static/writer_thumbs"
options={
    'crop-h':'300',
    'crop-w':'500',
    'encoding':'utf-8',   
    'zoom':'200'
}

files = os.listdir(WRITER_PATH)
for i in files:
    imgkit.from_file(WRITER_PATH+"/"+i, THUMB_PATH+"/"+i+"_thumb.png", options=options)
