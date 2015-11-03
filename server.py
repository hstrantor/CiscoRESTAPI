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
        # create new uid
        new_uid = get_uid()
        # create obj from json_data, by adding uid
        
        # add new obj to database

        #return obj with uid
        
    def PUT(self, uid, json_data):
        """Updates the obj specified by the uid.
        Is a COMPLETE REPLACEMENT. returns new obj
        """
        if (uid in objects):
            # save uid
            # remove obj from db
            # create new obj from json_data and uid
            # add object to db
            #return obj
            pass
        else:
            #error
            pass


    def GET(self, uid=None):
        """call to objects/<uid> returns full obj.
        call to objects/ returns json of all uids
        """
        if (uid == None):
            # return list of uids of all objects
            pass
        elif uid in j_objects:
            # return full json obj
            pass
        else:
            # return msg obj doesnt exist
            # OR (better) return error HTTP code
            pass

    def DELETE(self, uid):
        """ deletes uid specified obj from db.
        no response
        """
        if (uid in objects):
            # delete from db
            pass
        else:
            #errro
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
