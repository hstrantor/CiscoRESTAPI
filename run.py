#!/usr/bin/python

import sys
import argparse
import cherrypy
import sqlite3
import jsonAPI


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
        cherrypy.quickstart(jsonAPI.Objects_db(args.database),
                            script_name='/api/objects',
                            config="cherrypy.conf") 
    else:
        # set API to non db version
        print "Running RESTAPI with no database"
        cherrypy.quickstart(jsonAPI.Objects_nodb(),
                            script_name='/api/objects',
                            config="cherrypy.conf") 


if __name__ == "__main__":
    main()
