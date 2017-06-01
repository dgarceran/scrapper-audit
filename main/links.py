from urllib.request import urlparse
from lxml import cssselect
from os.path import splitext
import main
from main import db
from main.config import *

otherUrls = []
filesUrls = []
images = []

linkBase = URL_BASE
linkBase2 = URL_BASE2

def save404(url):
     profundidad = len(urlparse(url.geturl()).path.split('/')) - 2
     if(linkNotExists(url.geturl())):
         insert(url.geturl(), "", "", "roto", profundidad)
     else:
        cursor = db.connection.cursor()
        id = str(idLink(url.geturl()))
        cursor.execute("UPDATE `links` SET `tipo` = 'roto' WHERE `id` = " + id )
        cursor.close()
        db.connection.commit()
     return

def linksService(tree):
    links = []
    select = cssselect.CSSSelector("a")

    for el in select(tree):
        try:
            if (el.get('href') not in main.alreadyChecked, el.get('href') not in main.urls):
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

        endingurl = get_ext(link)

        if (urlparse(link).netloc == linkBase or urlparse(link).netloc == linkBase2):
            if (link not in main.urls):
                profundidad = len(urlparse(link).path.split('/')) - 2
                if (profundidad < 0):
                    profundidad = 0
                main.urls.append(link)
                print("Found link: " + link)
                if endingurl != 'jpg' and endingurl != 'pdf' and endingurl != 'png' and endingurl != 'gif' and endingurl != 'zip' and endingurl != 'rar' and endingurl != 'doc' and endingurl != 'xls' and endingurl != 'lsx' and endingurl != 'ppt':
                    insert(link, text, target, "url", profundidad)
                else:
                    insert(link, text, target, "archivos", profundidad)
        else:
            if (link != None):
                if (link not in otherUrls):
                    profundidad = len(urlparse(link).path.split('/'))
                    # print("another url ", link)
                    print("Found external link: " + link)
                    otherUrls.append(link)
                    if endingurl != 'jpg' and endingurl != 'pdf' and endingurl != 'png' and endingurl != 'gif' and endingurl != 'zip' and endingurl != 'rar' and endingurl != 'doc' and endingurl != 'xls' and endingurl != 'lsx' and endingurl != 'ppt':
                        insert(link, text, target, "otras", profundidad)
                    else:
                        insert(link, text, target, "archivos", profundidad)

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
            link = urlparse(link)
            link = link._replace(fragment='')
            # Read a single record
            sql = "SELECT `id` FROM `links` WHERE `link`=%s"
            cursor.execute(sql, (link.geturl()))
            result = cursor.fetchone()
            if(result is None):
                return True # Link does not exist
            else:
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