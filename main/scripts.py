from urllib import request, parse
from urllib.request import HTTPError, urlopen, urlparse
from lxml import cssselect,html
from main import db

def scriptsService(url, hdr):
    print("CHECKING ALL THE SCRIPTS BEFORE WE START")
    url = urlparse(url)
    req = request.Request(url.geturl(), headers=hdr)
    req.selector = parse.quote(req.selector)
    try:
        page = urlopen(req)
        try:
            pagedecoded = page.read().decode('utf-8')
        except UnicodeDecodeError:
            pagedecoded = page.read().decode('utf-16')

        tree = html.fromstring(pagedecoded)

        selectScript = cssselect.CSSSelector("script")
        for el in selectScript(tree):
            src = ""
            version = ""
            minified = False

            if (el.get('src') != None):
                src = el.get('src')
                src = urlparse(src);
                print(src)
                text = ""
                version = src.query[4:]
                if(src.path[-7:] == ".min.js"):
                    minified = True

                insertScript(src.geturl(), version, minified, text)
            else:
                text = el.text
                if len(text.split('\n')) < 5:
                    minified = True
                insertScript(src, version, minified, text)
    except HTTPError:
        raise

    return

def insertScript(src, version, minified, text):
    try:
        with db.connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `scripts` (`link`, `version`, `minified`, `text`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (src, version, minified, text))
        db.connection.commit()
    except:
        raise

    return