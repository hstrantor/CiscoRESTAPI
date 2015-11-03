# main server script for REST API

# cherrypy has native json functionality, but i dont
# understand it yet, so for now, im using json lib
import json
import cherrypy

my_url = "127.0.0.1:8080"+"/api/objects"

class UID():
    def __init__(self):
        self.uid = 1
    def get_uid(self):
        self.uid +=1
        return str(self.uid-1)



# class to represent 'object' resources
class Objects(object):
    exposed = True
    objects = {}
    uids = UID()
    
    def POST(self, data):
        """Creates object with new uid and returns it. If called 2+ times,
        creates identical objs with dif uids.
        """
        # create new uid
        new_uid = self.uids.get_uid()
        # uid is IN the object AND it's the dict key
        try:
            new_obj = json.loads(data)
            new_obj['uid'] = new_uid
        except ValueError:
            err_msg = {
                        "verb": "POST",
                        "url": my_url+"/",
                        "message": "Not a JSON object"
                      }
            return json.dumps(err_msg)
        
        self.objects[new_uid] = new_obj
        return json.dumps(new_obj)


    def PUT(self, data, uid):
        """Updates the obj specified by the uid.
        Is a COMPLETE REPLACEMENT. returns new obj
        """
        try:
            new_obj = json.loads(data)
        except ValueError:
            err_msg = { "verb": "PUT",
                        "url": my_url+'/',
                        "message": "Not a JSON object"
                      }
            return json.dumps(err_msg)

        if (uid in self.objects):
            del self.objects[uid]
            new_obj['uid'] = uid
            self.objects[uid] = new_obj
            return json.dumps(obj)
        else:
            err_msg = { "verb": "PUT",
                        "url": my_url+'/',
                        "message": "Object does not exist"
                      }
            return json.dumps(err_msg)


    def GET(self, uid=None):
        """call to objects/<uid> returns full obj.
        call to objects/ returns json of all uids
        """
        if (uid == None):
            # return list of all objects (the uid is also the dict key
            all_obj = [{'url': my_url+'/'+ key } for key in self.objects]
            return json.dumps(all_obj)
        elif uid in self.objects:
            return json.dumps(self.objects[uid])
        else:
            err_msg = {
                        "verb": "GET",
                        "url": my_url+"/",
                        "message": "Object does not exist"
                      }
            return json.dumps(err_msg)

    def DELETE(self, uid):
        """ deletes uid specified obj from db.
        no response
        """
        if (uid in self.objects):
            del self.objects[uid]
        else:
            err_msg = { "verb": "DELETE",
                        "url": my_url+"/",
                        "message": "Object does not exists"
                      }
            return json.dumps(err_msg)

if __name__ == "__main__":
    # cherrypy config
    #cherrypy.config.update({'server.socket_host': '52.32.119.107',
    #                        'server.socket_port': 80})
    
    # create cherrypy app
    # set to handle /api/objects with Objects()
    # activate Method dispatcher (this sends the
    # right HTTP call to the right function
    cherrypy.tree.mount(
            Objects(), '/api/objects',
            {'/': { 'request.dispatch': cherrypy.dispatch.MethodDispatcher()},
             '':  { 'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
            }
    )

    # start cherrypy engine
    cherrypy.engine.start()
    cherrypy.engine.block()
