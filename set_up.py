#!/usr/bin/python

# check for necessary modules on system
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

import argparse

def main():
    
    # TODO make these options affect the program
    parser = argparse.ArgumentParser(description="Parser for API setup script")
    parser.add_argument('-t', '--test', help="Run as test", required=False)
    parser.add_argument('-d', '--database', help="Run with a database (else, uses runtime dict)", required=False)
    args = parser.parse_args()

    print args
    #TODO get url out of conf file to put into Object()
    # 1) load config from conf file into dict
    # 2) apply changes from cmd-args
    # 3) run app

    # load config file and run cherrypy server
    cherrypy.quickstart(server.Objects(),
                        script_name='/api/objects',
                        config="cherrypy.conf") 


if __name__ == "__main__":
    main()
