import cherrypy
import os
import os.path
import sqlite3
import correo
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

    @require()
    @cherrypy.expose
    def edita_nosotros(self):
        return """Esta es un area restringda."""

    @cherrypy.expose
    def logeo():
        return auth.get_loginform()

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
