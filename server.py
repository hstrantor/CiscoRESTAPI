""" main server script for REST API

cherrypy has native json functionality, but it causes
the server to send an HTTP BAD REQUEST code when sent
non-json data. We want to send a json encoded error
message when this happens, and I don't want to wade
through the cherrypy error handlers, so for now I'm
just using the python json library.
"""

import uuid
import json
import cherrypy

#class UID():
#    def __init__(self):
#        self.uid = 1
#    def get_uid(self):
#        self.uid +=1
#        return str(self.uid-1)



# function to generate error messages
def get_error_msg(verb, url, message):
    """Generates message for HTTP handler functions.
    Doesn't convert to JSON
    """
    msg = { 'verb': verb,
            'url': url,
            'message': message
          }
    return msg
          

# class to represent 'object' resources
class Objects(object):
    """Class to represent arbitrary JSON resources.
    A cherrypy handler calls the specific function based
    on the matching HTTP request
    """
    exposed = True
    objects = {}
    #uids = UID()
    # default url is localhost
    #my_url = "127.0.0.1:80"+"/api/objects"

    #def __init__(self, url=None):
    #    if (url != None):
    #        self.my_url = url+"/api/objects"
   
    def POST(self, data=None):
        """Creates object with new uid and returns it. If called 2+ times,
        creates identical objects with different uids.
        
        Returns: the new json object as a response, or
                 if request data wasn't json, returns json encoded error
                 message.
        """
        # create new uid
        new_uid = uuid.uuid4().hex  # self.uids.get_uid()
        # uid is IN the object AND it's the dict key
        try:
            new_obj = json.loads(data)
            new_obj['uid'] = new_uid
        except (ValueError, TypeError):
            return json.dumps(get_error_msg('POST', cherrypy.url(), "Not a JSON object"))
        
        self.objects[new_uid] = new_obj
        return json.dumps(new_obj)

    # args take off consecutive bits of the url,
    # and then HTTP request body
    def PUT(self, uid, data=None):
        """Updates the object specified by the given uid.
        This is a COMPLETE REPLACEMENT; the entire object is
        replaced by the new one. The creation works the same way
        as in POST: adds the uid to the new object and json encodes it
        
        Returns: The new version of the object (JSON)
                 Or, if error: An error messsage (JSON)
        """
        try:
            new_obj = json.loads(data)
        except (ValueError, TypeError):
            return json.dumps(get_error_msg("PUT", cherrypy.url(), "Not a JSON object"))
        

        if (uid in self.objects):
            del self.objects[uid]
            new_obj['uid'] = uid
            self.objects[uid] = new_obj
            return json.dumps(new_obj)
        else:
            return json.dumps(get_error_msg("PUT", cherrypy.url(), "Object does not exist"))
    
    def GET(self, uid=None):
        """Returns object specified by uid, or if none is specified,
        returns a list of all <uid>:<object url> pairs.
        
        Returns: Specified object (JSON),
                 if no uid specified: List of all objects (JSON)
                 if object doesn't exist: Error message (JSON)
        """
        if (uid == None):
            # return list of all objects (the uid is also the dict key
            all_obj = [{'url': self.my_url+'/'+ key } for key in self.objects]
            return json.dumps(all_obj)
        elif uid in self.objects:
            return json.dumps(self.objects[uid])
        else:
            return json.dumps(get_error_msg("GET", cherrypy.url(), "Object does not exist"))
            #return json.dumps(get_error_msg("GET", cherrypy.request.url+'/', "Object does not exist"))
    

    def DELETE(self, uid):
        """Deletes object specified by the uid. Indempotent.
        
        Returns: if object exists: Nothing
                 if object doesn't exist: Error message (JSON)
        """
        if (uid in self.objects):
            del self.objects[uid]
        else:
            return json.dumps(get_error_msg("DELETE", cherrypy.url(), "Object does not exist"))

if __name__ == "__main__":
    # if this script is called as an executable (which it usually won't be),
    # it runs with these defaults
    
    # create cherrypy app
    # set to handle /api/objects with Objects()
    # activate Method dispatcher (this sends the right HTTP call to the right function)
    cherrypy.tree.mount(
            Objects(), '/api/objects',
            {'/': { 'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
            }
    )

    # start cherrypy engine
    cherrypy.engine.start()
    cherrypy.engine.block()
