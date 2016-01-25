import cherrypy
import os.path
import sqlite3
from jinja2 import Environment, FileSystemLoader
from auth import AuthController, require, member_of, name_is

DB_STRING = "baseflores.py"
env = Environment(loader=FileSystemLoader('templates'))

class EditContent:
    _cp_config = {
        'auth.require': [member_of('admin')]
    }

class Root(object):

    auth = AuthController()
    restricted = EditContent()

    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('index.html')
        return tmpl.render(title='Inicio', select='inicio')

    @cherrypy.expose
    def nosotros(self):
        tmpl = env.get_template('nosotros.html')
        return tmpl.render(title='Nosotros', select='nosotros')

    @cherrypy.expose
    def contacto(self):
        tmpl = env.get_template('contacto.html')
        return tmpl.render(title='Contactanos', select='contacto')

    @require()
    @cherrypy.expose
    def edita_nosotros(self):
        return """Esta es un area restringda."""

    @cherrypy.expose
    def logeo():
        return auth.get_loginform()

if __name__ == '__main__':
    cherrypy.quickstart(Root(), config={
        '/css':
        { 'tools.staticdir.on':True,
          'tools.staticdir.dir': "/Users/fabricio/Desktop/jardin de las flores/sitio_cherry/static/css/"
        },
        '/img':
        { 'tools.staticdir.on':True,
          'tools.staticdir.dir': "/Users/fabricio/Desktop/jardin de las flores/sitio_cherry/static/img/"
        },
    })
