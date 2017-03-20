import io
from PIL import Image
from urllib import request, parse
from urllib.request import urlopen, urlparse
from lxml import cssselect
from main import db
from main.config import *

def getInfoImage(url, alt, title, hdr, url_origin):
    url = urlparse(url)
    if(url.netloc == ''):
        url = url._replace(netloc=URL_BASE)

    if(url.scheme == ''):
        url = url._replace(scheme='http')
    req = request.Request(url.geturl(), headers=hdr)
    req.selector = parse.quote(req.selector)
    file = io.BytesIO(urlopen(req).read())

    # THE SIZEº
    size = file.__sizeof__()

    # THE WIDTH / HEIGHT
    im=Image.open(file)
    width, height = im.size

    if imageNotExists(url.geturl(), url_origin):
        insertImage(url.geturl(), alt, title, height, width, size, url_origin)

def insertImage(link, alt, title, height, width, size, url_origin):
    try:
        with db.connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `images` (`link`, `alt_tag`, `title`, `height`, `width`, `size`, `origin`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (link, alt, title, height, width, size, url_origin))
        db.connection.commit()
    except:
        raise

def imageNotExists(link, url_origin):
    try:
        with db.connection.cursor() as cursor:
             # Read a single record
             sql = "SELECT `id` FROM `images` WHERE `link`=%s and `origin`=%s"
             cursor.execute(sql, (link, url_origin))
             result = cursor.fetchone()
             if(result is None):
                return True
             else:
                return False
    except:
        raise

def imageService(tree, hdr, url_origin):
    selectImg = cssselect.CSSSelector("img")
    for el in selectImg(tree):
        src = ""
        alt_tag = ""
        title = ""

        try:
            src = el.get('src')
        except TypeError:
            print("none src")
            raise

        try:
            alt_tag = el.get('alt')
            if(alt_tag is None):
               alt_tag = ""
        except TypeError:
            print("none alt")
            raise

        try:
            title = el.get('title')
            if(title is None):
                title = ""
        except TypeError:
            print("none title")
            raise

        getInfoImage(src, alt_tag, title, hdr, url_origin)