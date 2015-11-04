import cherrypy

class HelloWorld(object):
    msg = """<html> <head>
                    <title> My Soosoo </title>
                    </head>
                    <body>
                        <p> Sarice! </p>
                        <p> You're the most wonderful girl in the world. I'm so unbelievably glad I met you. :D </p>
                        <p> Love, </p>
                        <p>     Stinky Doo Doo</p>
                    </body>
            </html>"""
    @cherrypy.expose
    def index(self):
        return self.msg

if __name__ == "__main__":
    cherrypy.server.socket_host = 'ec2-52-32-119-107.us-west-2.compute.amazonaws.com'
    
    cherrypy.quickstart(HelloWorld())
