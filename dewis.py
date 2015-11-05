import cherrypy

class HelloWorld(object):
    msg = """<html> <head>
                    <title> Shup </title>
                    </head>
                    <body>
                        <p> Hi Noah, </p>
                        <p> This is your computer talking to you. </p>
                        <p> I fixed myself as soon as I noticed you purches that part to fix me.</p>
                        <p> What i'm trying to say is that I exists only to annoy you.</p>
                    </body>
            </html>"""
    @cherrypy.expose
    def index(self):
        return self.msg

if __name__ == "__main__":
    cherrypy.server.socket_host = '52.33.51.230'
    cherrypy.quickstart(HelloWorld())
