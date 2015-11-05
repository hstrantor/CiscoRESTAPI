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
import sqlite3
import ast


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
    
    def __init__(self, database):
        self.db = str(database)
   
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
        except (ValueError, TypeError):
            return json.dumps(get_error_msg('POST', cherrypy.url(), "Not a JSON object"))
        
        new_obj['uid'] = new_uid
        j_obj = json.dumps(new_obj)

        with sqlite3.connect(self.db) as conn:
            conn.execute("INSERT INTO objects VALUES(?, ?)", [new_uid, str(new_obj)])

        return j_obj

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
        
        new_obj['uid'] = uid
        j_obj = json.dumps(new_obj)

        with sqlite3.connect(self.db) as conn:
            r = conn.execute("SELECT value FROM objects WHERE uid=?", [uid])
            data = r.fetchone()
            if (data==None):
                return json.dumps(get_error_msg("PUT", cherrypy.url(), "Object does not exist"))
            else:
                r = conn.execute("UPDATE objects SET value=? WHERE uid=?", [str(new_obj), uid])
                return j_obj
        #else:
        #    return json.dumps(get_error_msg("PUT", cherrypy.url(), "Object does not exist"))
    
    def GET(self, uid=None):
        """Returns object specified by uid, or if none is specified,
        returns a list of all <uid>:<object url> pairs.
        
        Returns: Specified object (JSON),
                 if no uid specified: List of all objects (JSON)
                 if object doesn't exist: Error message (JSON)
        """
        if (uid == None):
            # return list of all objects (the uid is also the dict key
            with sqlite3.connect(self.db) as conn:
                r = conn.execute("SELECT uid FROM objects")
                all_uids = [x[0] for x in r.fetchall()]
                # get and fix url
                url = cherrypy.url()
                if url[len(url)-1] != '/':
                    url = url+'/'
                all_uids = [{'uid': x, 'url': url+x} for x in all_uids]
                return json.dumps(all_uids)
            
        with sqlite3.connect(self.db) as conn:
            #a = conn.execute("COL_LENGTH(objects, uid=?) IS NULL", [uid])
            #print type(a), a
            r = conn.execute("SELECT value FROM objects WHERE uid=?", [uid])
            data = r.fetchone()
            #data = ast.literal_eval(data)
            #print "data = ", data, type(data)
            
            if data==None:
                return json.dumps(get_error_msg("GET", cherrypy.url(), "Object does not exist"))
            else:
                return json.dumps(ast.literal_eval(data[0]))
            #return json.dumps(r.fetchone())
        #elif uid in self.objects:
        #    return json.dumps(self.objects[uid])
        #else:
        #    return json.dumps(get_error_msg("GET", cherrypy.url(), "Object does not exist"))
            #return json.dumps(get_error_msg("GET", cherrypy.request.url+'/', "Object does not exist"))
    

    def DELETE(self, uid):
        """Deletes object specified by the uid. Indempotent.
        
        Returns: if object exists: Nothing
                 if object doesn't exist: Error message (JSON)
        """
        with sqlite3.connect(self.db) as conn:
            r = conn.execute("SELECT value FROM objects WHERE uid=?", [uid])
            data = r.fetchone()
            if data==None:
                return json.dumps(get_error_msg("GET", cherrypy.url(), "Object does not exist"))
            else:
                conn.execute("DELETE FROM objects WHERE uid=?", [uid])


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
