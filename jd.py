from lxml.html import parse
import urllib
import urllib2

def activo():
    """Chequea si el JDownloader esta corriendo en la pc"""
    try:
        p = parse("http://127.0.0.1:9666/flash/").getroot()
        if "JDownloader" in p.text_content():
            return True
        else:
            return False
    except IOError:
        return False

def descargar(urls):
    """Agrega la lista de urls al JD"""
    jd_pagina = "http://127.0.0.1:9666/flash/add"
    info = {'urls': "\r\n".join(urls)}
    info = urllib.urlencode(info)
    req = urllib2.Request(jd_pagina, info)
    response = urllib2.urlopen(req)
    response.read()

