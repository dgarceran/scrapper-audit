from lxml import cssselect, etree
from main import db
import main

def headersService(tree, link):
    selectTitle = cssselect.CSSSelector("h1")
    cantidad = len(selectTitle(tree))
    print(cantidad)
    if(cantidad > 0):
        for el in selectTitle(tree):
            texto = etree.tostring(el)
            if headerNotExists(link, texto):
                main.check_images = True
                insertHeader(link, cantidad, texto)
            else:
                main.check_images = False
    else:
        if headerNotExists(link, ""):
            main.check_images = True
            insertHeader(link, cantidad, "")
        else:
            main.check_images = False

def insertHeader(link, cantidad, texto):
    try:
        with db.connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `title_headers` (`link`, `cantidad`, `texto`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (link, cantidad, texto))
        db.connection.commit()
    except:
        raise

def headerNotExists(link, texto):
    try:
        with db.connection.cursor() as cursor:
             # Read a single record
             sql = "SELECT `id` FROM `title_headers` WHERE `link`=%s and texto=%s"
             cursor.execute(sql, (link, texto))
             result = cursor.fetchone()
             if(result is None):
                return True
             else:
                return False
    except:
        raise