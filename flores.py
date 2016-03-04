import cherrypy
import os
import os.path
import sqlite3
import correo
import time
from jinja2 import Environment, FileSystemLoader
from auth import AuthController, require, member_of, name_is

class RestrictedArea:

    # all methods in this controller (and subcontrollers) is
    # open only to members of the admin group

    _cp_config = {
        'auth.require': [member_of('admin')]
    }

    @cherrypy.expose
    def index_admin(self):
        return """This is the admin only area."""



DB_STRING = "baseflores.db"
env = Environment(loader=FileSystemLoader('templates'))

class EditContent:
    _cp_config = {
        'auth.require': [member_of('admin')]
    }

class StringGeneratorWebService(object):
    exposed = True

    @cherrypy.tools.accept(media='text/plain')
    def last_value(self):
        with sqlite3.connect(DB_STRING) as c:
            cherrypy.session['ts'] = time.time()
            r = c.execute("SELECT id from text_page WHERE (SELECT MAX(ID)  FROM text_page)",
                      [cherrypy.session.id])
            return r.fetchone()

    def consulta(self, name):
        with sqlite3.connect(DB_STRING) as c:
            #cherrypy.session['ts'] = time.time()
            r = c.execute("SELECT value FROM text_page WHERE name=?",
                      [name])
            return r.fetchone()

    def crear(self, identificador, name, value):
        with sqlite3.connect(DB_STRING) as c:
            r = c.execute("INSERT INTO text_page VALUES (?, ?)",
                      [name, value])
        return r.fetchone()

    def actualizar(self, name, value):
        with sqlite3.connect(DB_STRING) as c:
            #cherrypy.session['ts'] = time.time()
            r = c.execute("SELECT value FROM text_page WHERE name=?",
                      [name])
            if r.fetchone()!=None:
                r = c.execute("UPDATE text_page SET value=? WHERE name=?",
                          [value, name])
            else:
                r = c.execute("INSERT INTO text_page VALUES (?, ?)",
                          [name, value])
            return """ terminado """

    def DELETE(self):
        with sqlite3.connect(DB_STRING) as c:
            c.execute("DELETE FROM text_page WHERE session_id=?",
                      [cherrypy.session.id])

class Root(object):

    _cp_config = {
        'tools.sessions.on': True,
        'tools.auth.on': True
    }

    auth = AuthController()
    restricted = EditContent()
    base = StringGeneratorWebService()

    @cherrypy.expose
    def index(self):
        base = StringGeneratorWebService()
        tmpl = env.get_template('index.html')
        try:
            titulo = base.consulta("index-title")[0]
            descripcion = base.consulta("index-description")[0]
        except:
            titulo = ""
            descripcion= ""
        dic_info = { "titulo": titulo, "descripcion": descripcion}
        return tmpl.render(title='Inicio', select='inicio', info=dic_info)

    @cherrypy.expose
    def nosotros(self):
        base = StringGeneratorWebService()
        tmpl = env.get_template('nosotros.html')
        try:
            mision = base.consulta("mision")[0]
            vision = base.consulta("vision")[0]
        except:
            titulo = ""
            descripcion= ""
        dic_info = { "mision": mision, "vision": vision}
        return tmpl.render(title='Nosotros', select='nosotros', info= dic_info)

    @cherrypy.expose
    def contacto(self):
        tmpl = env.get_template('contacto.html')
        return tmpl.render(title='Contactanos', select='contacto')

    @cherrypy.expose
    def envio_mensaje(self, **params):
        dic = cherrypy.request.body.params
        msg = "Nombre: "+dic['first_name']+" "+dic['last_name']+"\n telefono: "+dic['telephone']+"\n correo "+dic['email']+"\n"+dic['message']
        correo.mensaje(msg)
        tmpl = env.get_template('contacto.html')
        return tmpl.render(title='Contactanos', select='contacto', mensaje=True)

    @cherrypy.expose
    def galeria(self):
        tmpl = env.get_template('galeria2/index.html')
        return tmpl.render()

    @cherrypy.expose
    def galery(self):
        tmpl = env.get_template('galeria.html')
        return tmpl.render(title='Galeria', select='galeria')
    
    @cherrypy.expose
    @require()
    def index_admin(self):
        tmpl = env.get_template('index_admin.html')
        return tmpl.render(title='Admin')

    @cherrypy.expose
    @require()
    def login(self):
        return """This page only requires a valid login."""

    @cherrypy.expose
    def open(self):
        return """This page is open to everyone"""

    @cherrypy.expose
    @require(name_is("joe"))
    def only_for_joe(self):
        return """Hello Joe - this page is available to you only"""

    # This is only available if the user name is joe _and_ he's in group admin
    @cherrypy.expose
    @require(name_is("jardin_flores"))
    @require(member_of("admin"))   # equivalent: @require(name_is("joe"), member_of("admin"))
    def only_for_joe_admin(self):
        return """Hello Joe Admin - this page is available to you only"""


    @cherrypy.expose
    @require(name_is("jardin_flores"))
    def edit_index(self):
        base = StringGeneratorWebService()
        tmpl = env.get_template('edit_index.html')
        try:
            titulo = base.consulta("index-title")[0]
            descripcion = base.consulta("index-description")[0]
        except:
            titulo = ""
            descripcion= ""
        dic_info = { "titulo": titulo, "descripcion": descripcion}
        return tmpl.render(title="Editar Home", info = dic_info)

    @cherrypy.expose
    @require(name_is("jardin_flores"))
    def change_index(self, **params):
        dic = cherrypy.request.body.params
        base = StringGeneratorWebService()
        base.actualizar("index-title", dic['title'])
        base.actualizar("index-description", dic['description'])
        return """ sitio actualizado """

    @cherrypy.expose
    @require(name_is("jardin_flores"))
    def edit_we(self):
        base = StringGeneratorWebService()
        tmpl = env.get_template('edit_we.html')
        try:
            mision = base.consulta("mision")[0]
            vision = base.consulta("vision")[0]
        except:
            mision = ""
            vision = ""
        dic_info = { "mision": mision, "vision": vision}
        return tmpl.render(title="Editar Nosotros", info = dic_info)

    @cherrypy.expose
    @require(name_is("jardin_flores"))
    def change_we(self, **params):
        dic = cherrypy.request.body.params
        base = StringGeneratorWebService()
        base.actualizar("mision", dic['mision'])
        base.actualizar("vision", dic['vision'])
        return """ sitio actualizado """

    @cherrypy.expose
    @require(name_is("jardin_flores"))
    def edit_galery(self):
        base = StringGeneratorWebService()
        print os.listdir("static/img/")
        tmpl = env.get_template('edit_galery.html')
        """
        try:
            mision = base.consulta("mision")[0]
            vision = base.consulta("vision")[0]
        except:
            mision = ""
            vision = ""
        dic_info = { "mision": mision, "vision": vision}
        """
        return tmpl.render(title="Editar Galeria")

    @cherrypy.expose
    @require(name_is("jardin_flores"))
    def upload_image(self, **params):
        dic = cherrypy.request.body.params
        base = StringGeneratorWebService()
        base.actualizar("mision", dic['mision'])
        base.actualizar("vision", dic['vision'])
        return """ sitio actualizado """

def setup_database():
    """
    Create the `text_page` table in the database
    on server startup
    """
    with sqlite3.connect(DB_STRING) as con:
        con.execute("CREATE TABLE IF NOT EXISTS text_page (name, value)")

def cleanup_database():
    """
    Destroy the `text_page` table from the database
    on server shutdown.
    """
    with sqlite3.connect(DB_STRING) as con:
        con.execute("DROP TABLE text_page")

try:
    cherrypy.engine.subscribe('start', setup_database)
except (sqlalchemy.exc.NoSuchTableError):
    pass
#cherrypy.engine.subscribe('stop', cleanup_database)

app = cherrypy.tree.mount(Root(), '/')

if __name__ == '__main__':
    cherrypy.config.update({ 'server.socket_host': '0.0.0.0', 'server.socket_port': 8000, })
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    cherrypy.quickstart(Root(), config={
        '/css':
        { 'tools.staticdir.on':True,
          'tools.staticdir.dir': os.path.join(BASE_DIR, '', 'static/css')
        },
        '/img':
        { 'tools.staticdir.on':True,
          'tools.staticdir.dir': os.path.join(BASE_DIR, '', 'static/img')
        },
        '/script':
        { 'tools.staticdir.on':True,
          'tools.staticdir.dir': os.path.join(BASE_DIR, '', 'static/script')
        },
    })
