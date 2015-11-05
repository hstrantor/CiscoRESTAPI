#!/usr/bin/python

# TODO check for necessary modules on system -> set up
"""
try:
    import cherrypy
    cherrypy_loaded = True
except ImportError:
    cherrypy_loaded = False
try:
    import argparse
    argparse_loaded = True
except ImportError:
    argparse_loaded = False
try:
    import server  # TODO change name of api module
    server_loaded = True
except ImportError:
    server_loaded = False

modules = {'cherrypy':cherrypy_loaded,
           'argparse':argparse_loaded, 
           'server':server_loaded}

for key in modules:
    if modules[key] == False:
        print "error msg bc specified module wouldnt load"
        sys.exit(1)
"""
import sys
import argparse
import cherrypy
import sqlite3
import RESTAPI_basic
import RESTAPI_db

def main():
    
    parser = argparse.ArgumentParser(description="Parser for API setup script")
    parser.add_argument('-t', '--test', help="Run tests", required=False)
    parser.add_argument('-d', '--database', help="Run with a database instead of python dict", required=False)
    args = parser.parse_args()

    if args.database:
        # set up database
        with sqlite3.connect(args.database) as c:
            c.execute("CREATE TABLE IF NOT EXISTS objects (uid, value)")
        # set API to database version
        print "Running RESTAPI with database"
        cherrypy.quickstart(RESTAPI_db.Objects(args.database),
                            script_name='/api/objects',
                            config="cherrypy.conf") 
    else:
        # set API to non db version
        print "Running RESTAPI with no database"
        cherrypy.quickstart(RESTAPI_basic.Objects(),
                            script_name='/api/objects',
                            config="cherrypy.conf") 


if __name__ == "__main__":
    main()
