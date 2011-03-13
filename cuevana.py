import cookielib
from lxml.html import fromstring
import urllib
import urllib2
import re

patron = re.compile("(\d+)")

global opener
opener = None

def login(usuario, password):
    """Loggearse a cuevana"""
    login_page = "http://www.cuevana.tv/login_get.php"
    login_info = {'usuario': usuario, 'password': password, 'ingresar':'true'}

    jar = cookielib.CookieJar()

    global opener
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))

    login_info = urllib.urlencode(login_info)
    resp = opener.open(login_page, login_info)
    

def getEpisodio(num):
    """Obtiene el link de megaupload del episodio"""
    resp = opener.open("http://www.cuevana.tv/botlink_des.php?id=%s&serie=true" % num)
    pag = resp.read()
    p = fromstring(pag)
    idm = p.forms[0].inputs['megaid'].value

    return "http://www.megaupload.com/?d=%s" % idm
	
def getSeries():
    """Devuelve todas las series disponibles junto a su ID"""
    resp = opener.open("http://www.cuevana.tv/series/")
    pag = resp.read()
    p = fromstring(pag)
    series = []
    for s in p.findall(".//li[@onclick]"):
        id = int(patron.findall(s.get("onclick"))[1])
        series.append( (s.text, id))
    return series

def getPagSerie(serie_id):
    """A partir del ID de serie, obtiene la pagina base de serie"""
    resp = opener.open("http://www.cuevana.tv/list_search_info.php?serie=%s" % serie_id)
    pag = resp.read()
    p = fromstring(pag)

    return "http://cuevana.tv" + p.find(".//input").get("onclick").split("'")[1]
