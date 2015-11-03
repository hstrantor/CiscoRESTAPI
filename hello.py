import cherrypy

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return """<html>
            <head></head>
        <body> 
            <p> I Love you! - Barry </p>
        </body>
        </html>"""

if __name__ == "__main__":
    cherrypy.quickstart(HelloWorld())
