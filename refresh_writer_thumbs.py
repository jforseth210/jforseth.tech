import imgkit
import os
WRITER_PATH="text/writerdocs"
THUMB_PATH="static/writer/thumbs"
options={
    'height':'300',
    'width':'500',
    'encoding':'utf-8'
}
def main():
    if os.name == 'nt':
        config=imgkit.config(wkhtmltoimage=b"C:/Program Files/wkhtmltopdf/bin/wkhtmltoimage.exe")
    else:
        config=imgkit.config()
    if os.name == 'posix':
        options.update(xvfb="")
    files = os.listdir(WRITER_PATH)
    for i in files:
        if i!="oopsie":
            print(WRITER_PATH+"/"+i, THUMB_PATH+"/"+i+"_thumb.png", options,config)
            imgkit.from_file(WRITER_PATH+"/"+i, THUMB_PATH+"/"+i+"_thumb.png", options=options,config=config)
if __name__ == "__main__":
    main()
