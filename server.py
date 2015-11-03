# main server script for REST API

# cherrypy has native json functionality, but i dont
# understand it yet, so for now, im using json lib
import json
import cherrypy

my_url = "127.0.0.1:8080"

class UID():
    def __init__(self):
        self.uid = 1
    def get_uid(self):
        self.uid +=1
        return str(self.uid-1)



# class to represent 'object' resources
class Objects:
    exposed = True
    objects = {}
    uids = UID()
    
    def POST(self, json_data):
        """Creates object with new uid and returns it. If called 2+ times,
        creates identical objs with dif uids.
        """
        # create new uid
        new_uid = self.uids.get_uid()
        # uid is IN the object AND its the dict key
        try:
            new_obj = json.loads(json_data)
            new_obj['uid'] = new_uid
        except ValueError:
            err_msg = {
                        "verb": "POST",
                        "url": my_url+"/api/objects/",
                        "message": "Not a JSON object"
                      }
            return json.dumps(err_msg)
        
        objects[new_uid] = new_obj
        return json.dumps(new_obj)


    def PUT(self, uid, json_data):
        """Updates the obj specified by the uid.
        Is a COMPLETE REPLACEMENT. returns new obj
        """
        if (uid in objects):
            del objects[uid]
            new_obj = json.loads(json_data)
            new_obj['uid'] = uid
            objects[uid] = new_obj
            return obj
        else:
            #error
            pass


    def GET(self, uid=None):
        """call to objects/<uid> returns full obj.
        call to objects/ returns json of all uids
        """
        if (uid == None):
            # return list of all objects
            # make this a ffunc()
            return  "no objects"
            pass
        elif uid in j_objects:
            # return full json obj
            return "HIII test A"
        else:
            # return msg obj doesnt exist
            # OR (better) return error HTTP code
            pass

    def DELETE(self, uid):
        """ deletes uid specified obj from db.
        no response
        """
        if (uid in objects):
            del objects[uid]
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
