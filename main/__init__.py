from urllib import request, parse
from urllib.request import urlopen, HTTPError, urlparse
from os.path import splitext
from lxml import html
from main import links, imgs, title_headers
from main.config import *

url = URL
hdr = HDR

urls = []
alreadyChecked = []

def initialCall(url):


    crawler(url, hdr)
    iterateUrls()

    return

def crawler(url, hdr):
    "Gets all the links of a website"

    alreadyChecked.append(url)

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
                links.linksService(tree)

                # TITLE HEADERS
                title_headers.headersService(tree, url.geturl())

                # IMAGES
                imgs.imageService(tree, hdr)

            except HTTPError:
                links.save404(url)
        else:
            profundidad = len(urlparse(url.geturl()).path.split('/'))
            if(url.geturl() not in links.filesUrls):
                #print("File: ")
                links.filesUrls.append(url.geturl())
                links.insert(url.geturl(), "", "", "archivos", profundidad)
    return

def iterateUrls():
    for url in urls:
        #print(url)
        if(url not in alreadyChecked):
            crawler(url, hdr)

def get_ext(url):
    """Return the filename extension from url, or ''."""
    parsed = urlparse(url)
    root, ext = splitext(parsed.path)
    return ext[1:]  # or ext[1:] if you don't want the leading '.'

initialCall(url)