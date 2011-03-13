import cmd
from stor import Seguidas
import cuevana
import series

class CuevanadorShell(cmd.Cmd):
    intro = "? para listar comandos -- configurar usuario y password primero -- mostrarSeries para comenzar a agregar una serie"

    def __init__(self):
        cmd.Cmd.__init__(self)

        self.stor = Seguidas()

    def do_usuario(self, arg):
        self.stor.usuario = arg

    def do_password(self, arg):
        self.stor.password = arg
        self.do_login("")

    def do_login(self, arg):
        print "Loggeando..."
        self.stor.login()

    def do_mostrarSeries(self, arg):
        self.do_login("")
        self.series = cuevana.getSeries()

        print "Series disponibles (junto a su id) -- * marca serie seguida"
        for s, id in self.series:
            seg = ""
            if(str(id) in self.stor.series):
                seg = "*"
            print "(%s%d) %s" % (seg, id, s)
        
        print "Usar 'mostrarTemporadas id' para ver temporadas disponibles"

    def do_mostrarTemporadas(self, serie):
        pag = cuevana.getPagSerie(serie)
        self.temp = series.obtenerTodos(pag)[1]

        self.serie = serie

        print "Temporadas disponibles"
        print self.temp.keys()

        print "Usar 'mostrarTemporada numero' para seleccionar temporada de origen"

    def do_mostrarTemporada(self, num):
        if not self.temp:
            print "Seleccionar serie antes"
            return

        print "(clave) numero capitulo - nombre"
        for cap in self.temp["temp"+num]:
            print "(%d) %s - %s" % (cap[2], cap[0], cap[1])

        print "Usar 'agregarSerie clave' para comenzar a seguir la serie a partir de ese capitulo"

    def do_agregarSerie(self, clave):
        self.stor.agregar(self.serie, int(clave))

        print "Usar 'actualizar' para obtener los ultimos capitulos"

    def do_actualizar(self, arg):
        self.stor.actualizar()

    def do_ver(self, arg):
        print "ID de serie e ID de ultimo capitulo visto"
        print self.stor.series

    def do_borrar(self, serie):
        self.stor.borrar(serie)

if __name__ == "__main__":
    CuevanadorShell().cmdloop()