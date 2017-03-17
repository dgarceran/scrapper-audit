import io
from PIL import Image
from urllib import request, parse
from urllib.request import urlopen, urlparse
import db

def getInfoImage(url):
    hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Content-type': 'text/html; charset=utf-8',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}

    url = urlparse(url)
    req = request.Request(url.geturl(), headers=hdr)
    req.selector = parse.quote(req.selector)
    file = io.BytesIO(urlopen(req).read())

    # THE SIZE
    size = file.__sizeof__()

    # THE WIDTH / HEIGHT
    im=Image.open(file)
    width, height = im.size

def insertImage(link, alt, title, height, width, extra):
    try:
        with db.connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `images` (`link`, `alt`, `title`, `height`, `width`, `extra`) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (link, alt, title, height, width, extra))
        db.connection.commit()
    except:
        raise