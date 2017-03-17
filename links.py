from urllib import request, parse
from urllib.request import urlopen, HTTPError, urlparse
from lxml import html, cssselect
from os.path import splitext
import db

# LINK CRAWLER
#
# By David Garcerán - DEIDEAS Marketing Solutions.
# dgarceran@deideasmarketing.com

urls = []
alreadyChecked = []
otherUrls = []
filesUrls = []
images = []

def initialCall(url):

    getAllLinks(url)
    iterateUrls()

    return

def getAllLinks(url):
    "Gets all the links of a website"

    alreadyChecked.append(url)
    links = []

    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Content-type': 'text/html; charset=utf-8',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}


    if(url is not '#' and url is not ''):
        url = urlparse(url)
        print(url)

        if (url.scheme == ''):
            url._replace(scheme="http")

        endingurl = get_ext(url.geturl())

        if endingurl != 'jpg' and endingurl != 'pdf' and endingurl != 'png' and endingurl !='gif' and endingurl != 'zip' and endingurl != 'rar' and endingurl != 'doc' and endingurl != 'xls' and endingurl != 'lsx' and endingurl != 'ppt':
            req = request.Request(url.geturl(), headers=hdr)
            req.selector = parse.quote(req.selector)

            try:
                page = urlopen(req)
                try:
                    pagedecoded = page.read().decode('utf-8')
                except UnicodeDecodeError:
                    pagedecoded = page.read().decode('utf-16')

                tree = html.fromstring(pagedecoded)

                # LINKS

                select = cssselect.CSSSelector("a")

                for el in select(tree):
                    try:
                        if (el.get('href') not in alreadyChecked, el.get('href') not in urls):
                            links.append(el)
                    except TypeError:
                        print("none")
                        raise

                for l in links:
                    text = ""
                    target = ""
                    link = ""

                    try:
                        text = l.text_content()
                    except AttributeError:
                        print("no text")
                        raise

                    try:
                        target = l.get('target')
                    except AttributeError:
                        print("no target")
                        raise

                    try:
                        link = l.get('href')
                    except TypeError:
                        print("none link")
                        raise

                    linkBase = 'www.gruposifu.com'

                    endingurl = get_ext(link)

                    if (urlparse(link).netloc == linkBase):
                        if (link != url and link not in urls):
                            profundidad = len(urlparse(link).path.split('/')) - 2
                            if (profundidad < 0):
                                profundidad = 0
                            urls.append(link)
                            if endingurl != 'jpg' and endingurl != 'pdf' and endingurl != 'png' and endingurl != 'gif' and endingurl != 'zip' and endingurl != 'rar' and endingurl != 'doc' and endingurl != 'xls' and endingurl != 'lsx' and endingurl != 'ppt':
                                insert(link, text, target, "url", profundidad)
                            else:
                                insert(link, text, target, "archivos", profundidad)
                    else:
                        if (link != None):
                            if (link not in otherUrls):
                                profundidad = len(urlparse(link).path.split('/'))
                                # print("another url ", link)
                                otherUrls.append(link)
                                if endingurl != 'jpg' and endingurl != 'pdf' and endingurl != 'png' and endingurl != 'gif' and endingurl != 'zip' and endingurl != 'rar' and endingurl != 'doc' and endingurl != 'xls' and endingurl != 'lsx' and endingurl != 'ppt':
                                    insert(link, text, target, "otras", profundidad)
                                else:
                                    insert(link, text, target, "archivos", profundidad)

                '''
                # IMAGES

                selectImg = cssselect.CSSSelector("img")
                for el in selectImg(tree):
                    src = ""
                    alt_tag = ""

                    print()
                '''
            except HTTPError:
                profundidad = len(urlparse(url.geturl()).path.split('/')) - 2
                if (linkNotExists(url.geturl())):
                    insert(url.geturl(), "", "", "roto", profundidad)
                else:
                    cursor = db.connection.cursor()
                    id = str(idLink(url.geturl()))
                    cursor.execute("UPDATE `links` SET `tipo` = 'roto' WHERE `id` = " + id )
                    cursor.close()
                    db.connection.commit()
                print("404 - ", url.geturl())

        else:
            profundidad = len(urlparse(url.geturl()).path.split('/'))
            if(url.geturl() not in filesUrls):
                #print("File: ")
                filesUrls.append(url.geturl())
                insert(url.geturl(), "", "", "archivos", profundidad)
    return

def iterateUrls():
    for url in urls:
        #print(url)
        if(url not in alreadyChecked):
            getAllLinks(url)
            #closeConnection()

def insert(link, texto, target, tipo, profundidad):
    if(linkNotExists(link)):
        if(target == None):
            target = ""
        try:
            with db.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `links` (`link`, `texto`, `target`, `tipo`, `profundidad`) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (link, texto, target, tipo, profundidad))
            db.connection.commit()
        except:
            raise

    return

def closeConnection():
    db.connection.close()
    return

def linkNotExists(link):
    try:
        with db.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id` FROM `links` WHERE `link`=%s"
            cursor.execute(sql, (link))
            result = cursor.fetchone()
            if(result is None):
                #print("is none")
                return True
            else:
                #print("already exists")
                return False
    except:
        raise

def idLink(link):
    try:
        with db.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id` FROM `links` WHERE `link`=%s"
            cursor.execute(sql, (link))
            result = cursor.fetchone()
            return result['id']
    except:
        raise

def get_ext(url):
    """Return the filename extension from url, or ''."""
    parsed = urlparse(url)
    root, ext = splitext(parsed.path)
    return ext[1:]  # or ext[1:] if you don't want the leading '.'