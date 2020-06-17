import os
import imgkit

options = {
    "height": "600",
    # 'width':'500',
    "crop-w": "1024",
    "encoding": "utf-8",
}


def refresh_thumbs(user):
    """Refresh the thumbnail images for the writer homepage.

    Arguments:
        user {str} -- The user to refresh the thumbs for. Passing 'all' will update all users thumbnails.
    """
    if user != "all":
        WRITER_PATH = "userdata/{}/writer/documents".format(user)
        THUMB_PATH = "userdata/{}/writer/thumbnails".format(user)
        # Windows needs executable path to be specified.
        if os.name == "nt":
            config = imgkit.config(
                wkhtmltoimage=b"C:/Program Files/wkhtmltopdf/bin/wkhtmltoimage.exe"
            )
        else:
            config = imgkit.config()
        # xvfb is needed by Linux
        if os.name == "posix":
            options.update(xvfb="")

        files = os.listdir(WRITER_PATH)
        for i in files:
            # Don't create a thumbnail for the backup folder.
            if i != "oopsie":
                imgkit.from_file(
                    WRITER_PATH + "/" + i,
                    THUMB_PATH + "/" + i + "_thumb.png",
                    options=options,
                    config=config,
                )
    else:
        # List every user and recursively refresh thumbnails.
        users = os.listdir("userdata/")
        for user in users:
            refresh_thumbs(user)


if __name__ == "__main__":
    refresh_thumbs("all")
