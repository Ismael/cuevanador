import pickle
import cuevana
import series
import jd

class Seguidas(object):
    def __init__(self):
        self.cargar()

    def cargar(self):
        self.series = {}
        self.usuario = ""
        self.password = ""

        try:
            f = open("stor.db")
            datos = pickle.load(f)
            self.series = datos['series']
            self.usuario = datos['usuario']
            self.password = datos['password']
            f.close()
        except:
            print "No se cargaron datos"

    def guardar(self):
        f = open("stor.db", "w")
        datos = {'series':self.series, 'usuario':self.usuario, 'password':self.password}
        pickle.dump(datos, f)
        f.close()

    def __del__(self):
        self.guardar()
    
    def agregar(self, serie, cap):
        self.series[serie] = cap

    def borrar(self, serie):
        del self.series[serie]

    def login(self):
        cuevana.login(self.usuario, self.password)

    def actualizar(self):
        self.login()

        for serie in self.series.keys():
            pag = cuevana.getPagSerie(serie)
            eps = series.obtenerTodos(pag)[0]

            ultimo_visto = self.series[serie]
            nuevos = series.obtenerNuevos(eps, ultimo_visto)

            if len(nuevos) > 0:
                urls = series.obtenerURLs(nuevos)

                if jd.activo():
                    jd.descargar(urls)

                print "Nuevos capitulos"
                print "\n".join(urls)

                #Actualizar ultimo visto
                self.series[serie] = max(nuevos)