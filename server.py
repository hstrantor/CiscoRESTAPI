# main server script for REST API

# cherrypy has native json functionality, but i dont
# understand it yet, so for now, im using json lib
import json
import cherrypy

# database
j_objects = {}

def get_uid():
    # returns new uid
    pass


#@cherrypy.popargs('name')
# class to represent 'object' resources
class Objects:
    exposed = True
    
    def POST(self, json_data):
        """Creates object with new uid and returns it. If called 2+ times,
        creates identical objs with dif uids.
        """
        new_uid = get_uid()
        new_obj = {
        

    def GET(self, id=None):
        if (id == None):
            # return list of uids of all objects
            pass
        elif id in j_objects:
            # return full json obj
            pass
        else:
            # return msg obj doesnt exist
            # OR (better) return HTTP code
            pass


if __name__ == "__main__":
    # create cherrypy app
    # set to handle /api/objects with Objects()
    # activate Method dispatcher (this sends the
    # right HTTP call to the right function
    cherrypy.tree.mount(
            Objects(), '/api/objects',
            {'/': { 'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
            }
    )

    # start cherrypy engine
    cherrypy.engine.start()
    cherrypy.engine.block()
