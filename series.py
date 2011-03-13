import cuevana
from lxml.html import parse
import re

patron = re.compile("(\d+)")

def obtenerTodos(serie):
    """A partir de la pagina de serie, obtiene todos los capitulos disponibles"""
    p = parse(serie).getroot()
    uls = p.findall(".//ul[@id]")

    temporadas = {}
    episodios = []

    for u in uls:
        temporada = u.get("id")
        temporadas[temporada] = []
        for li in u.iterchildren():
            num = li[0].text
            cap = li[1].text
            link = li[1].get("href")
            clave = int(patron.search(link).groups()[0])
            temporadas[temporada].append((num, cap, clave))
            episodios.append(clave)

    return (episodios, temporadas)

def obtenerNuevos(episodios, ultimo_cap):
    """Obtiene los capitulos no vistos"""
    def mayorque(num):
        def inner(n):
            return n > num
        return inner
    
    return filter(mayorque(ultimo_cap), episodios)


def obtenerURLs(episodios):
    """Obtiene las URLs de descarga de los episodios"""
    urls = []
    for ep in episodios:
        urls.append(cuevana.getEpisodio(ep))
    return urls
