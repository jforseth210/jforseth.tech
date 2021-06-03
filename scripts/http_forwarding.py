from flask import *
import requests

http_forwarding = Blueprint("http_forwarding", __name__)

# TODO: Make this actually work.
@http_forwarding.route("/httpforwarding")
def experiment():
    ATTRIBUTES = ["src", "href", "content", "action", "data-unscoped-search-url"]

    requested_url = escape(request.args.get("url"))

    # If the user hasn't entered a url yet, return this message.
    if requested_url is None:
        page = "Enter your desired page"
        return "<form><input name='url' /><input type='submit'></form>" + str(page)
    # Did the user request an image?
    ispng = requested_url[:-4] == ".png"
    isjpg = requested_url[:-4] == ".jpg"
    isjpeg = requested_url[:-5] == ".jpeg"

    isimage = ispng or isjpg or isjpeg
    if isimage:
        # If the user has requested an image, send it raw, not as text.
        return str(requests.get(requested_url).raw)
    page = requests.get(requested_url).content
    requested_url_utf = requested_url.encode("utf-8")
    for attribute in ATTRIBUTES:
        # page=page.replace(attribute.encode('utf-8')+b"=",attribute.encode('utf-8')+b"=https://jforseth.tech/experiment?url="+requested_url_utf)
        page = page.replace(
            attribute.encode("utf-8") + b"='/",
            attribute.encode("utf-8")
            + b"=https://jforseth.tech/experiment?url="
            + requested_url_utf
            + b"/",
        )
        page = page.replace(
            attribute.encode("utf-8") + b'="/',
            attribute.encode("utf-8")
            + b"=https://jforseth.tech/experiment?url="
            + requested_url_utf
            + b"/",
        )
        page = page.replace(
            attribute.encode("utf-8") + b"=/",
            attribute.encode("utf-8")
            + b"=https://jforseth.tech/experiment?url="
            + requested_url_utf
            + b"/",
        )
    return "<form><input name='url' /><input type='submit'></form>" + str(page)
