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
    import server  # change name of api module
    server_loaded = True
except ImportError:
    server_loaded = False

modules = {'sys':sys_loaded, 'cherrypy':cherrypy_loaded,
           'json':json_loaded, 'server':server_loaded}
for key in modules:
    if modules[key] == False:
        print "errer msg bc specified module wouldnt load"
        sys.exit(1)

#import argparse

def main():
    """
    parser = argparse.ArgumentParser(description="Parser for API setup script")
    # not '-h', bc this is autoset to 'help'
    parser.add_argument('-l', '--host', help="HTTP HOST", required=True)
    parser.add_argument('-p', '--port', help="Port server listens at", required=True)
    parser.add_argument('-t', '--timeout', help="milliseconds before timeout", required=False)
    args = parser.parse_args()

    print "just a test", args.host, args.port, args.timeout
    """
    # 1) load config from conf file into dict
    # 2) apply changes from cmd-args
    #conf = None
    # 3) run app
    
    cherrypy.tree.mount( server.Objects(),
                         '/api/objects',
                         config="./cherrypy.conf")

    # start cherrypy engine
    cherrypy.engine.start()
    cherrypy.engine.block()

    #config = {'server.socket_host': 'localhost',
    #          'server.socker_port': 80,
    #          'response.timeout': 6000
    #          }


if __name__ == "__main__":
    main()