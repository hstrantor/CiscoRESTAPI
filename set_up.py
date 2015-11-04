#!/usr/bin/python

# check for necessary modules on system
try:
    import sys
    sys_loaded = True
except ImportError:
    sys_loaded = False
try:
    import cherrypy
    cherrypy_loaded = True
except ImportError:
    cherrypy_loaded = False
try:
    import json
    json_loaded = True
except ImportError:
    json_loaded = False
try:
    import server  # TODO change name of api module
    server_loaded = True
except ImportError:
    server_loaded = False

modules = {'sys':sys_loaded, 'cherrypy':cherrypy_loaded,
           'json':json_loaded, 'server':server_loaded}
for key in modules:
    if modules[key] == False:
        print "error msg bc specified module wouldnt load"
        sys.exit(1)

import argparse

def main():
    
    # TODO make these options affect the program
    parser = argparse.ArgumentParser(description="Parser for API setup script")
    parser.add_argument('-t', '--test', help="Run as test", required=False)
    parser.add_argument('-d', '--database', help="Run with a database (else, uses runtime dict)", required=False)
    args = parser.parse_args()

    print args

    # 1) load config from conf file into dict
    # 2) apply changes from cmd-args
    # 3) run app

    # load config file and run cherrypy server
    cherrypy.quickstart(server.Objects("ec2-52-32-119-107.us-west-2.compute.amazonaws.com"),
                        script_name='/api/objects',
                        config="cherrypy.conf") 


if __name__ == "__main__":
    main()
