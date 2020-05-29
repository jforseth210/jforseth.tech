import os
import imgkit
options={
    'height':'600',
    #'width':'500',
    'crop-w': '1024',
    'encoding':'utf-8'
}
def refresh_thumbs(user):
    if user != "all":
        WRITER_PATH="userdata/{}/writer/documents".format(user)
        THUMB_PATH="userdata/{}/writer/thumbnails".format(user)
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
    else: 
        users = os.listdir("userdata/")
        for user in users:
            refresh_thumbs(user)
if __name__ == "__main__":
    refresh_thumbs("all")
