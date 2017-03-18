import io
from PIL import Image
from urllib import request, parse
from urllib.request import urlopen, urlparse
from lxml import cssselect
from main import db

def getInfoImage(url, alt, title, hdr):

    url = urlparse(url)
    req = request.Request(url.geturl(), headers=hdr)
    req.selector = parse.quote(req.selector)
    file = io.BytesIO(urlopen(req).read())

    # THE SIZE
    size = file.__sizeof__()

    # THE WIDTH / HEIGHT
    im=Image.open(file)
    width, height = im.size

    if imageNotExists:
        insertImage(url.geturl(), alt, title, height, width, size, "")

def insertImage(link, alt, title, height, width, size, extra):
    try:
        with db.connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `images` (`link`, `alt_tag`, `title`, `height`, `width`, `size`, `extra`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (link, alt, title, height, width, size, extra))
        db.connection.commit()
    except:
        raise

def imageNotExists(link):
    try:
        with db.connection.cursor() as cursor:
             # Read a single record
             sql = "SELECT `id` FROM `images` WHERE `link`=%s"
             cursor.execute(sql, (link))
             result = cursor.fetchone()
             if(result is None):
                return True
             else:
                return False
    except:
        raise

def imageService(tree, hdr):
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

        getInfoImage(src, alt_tag, title, hdr)