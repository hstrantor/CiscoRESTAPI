#!/usr/bin/python

# TODO check for necessary modules on system
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
    parser.add_argument('-d', '--database', help="Run with a database (else, uses runtime dict)", required=False)
    args = parser.parse_args()

    if args.database:
        # set up database
        with sqlite3.connect(args.database) as c:
            c.execute("CREATE TABLE IF NOT EXISTS objects (uid, value)")
        # set API to database version
        API = RESTAPI_db.Objects(args.database)
        print "Running RESTAPI with database"
    else:
        # set API to non db version
        API = RESTAPI_basic.Objects()
        print "Running RESTAPI with no database"

    if args.test:
        pass
        # TODO set up db for tests
        # run test script
    else:
        # load config file and run cherrypy server
        cherrypy.quickstart(RESTAPI_db.Objects(args.database),
                            script_name='/api/objects',
                            config="cherrypy.conf") 


if __name__ == "__main__":
    main()
