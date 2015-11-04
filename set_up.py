#!/usr/bin/python

# parsing largely inspired by an article on cyberciti.biz

# TODO check for necessary modules on system
import cherrypy
import argparse
import server

def main():
    parser = argparse.ArgumentParser(description="Parser for API setup script")
    # not '-h', bc this is autoset to 'help'
    parser.add_argument('-l', '--host', help="HTTP HOST", required=True)
    parser.add_argument('-p', '--port', help="Port server listens at", required=True)
    parser.add_argument('-t', '--timeout', help="milliseconds before timeout", required=False)
    args = parser.parse_args()

    print "just a test", args.host, args.port, args.timeout

    # 1) load config from conf file into dict
    # 2) apply changes from cmd-args
    # 3) run app
    
    cherrypy.tree.mount(
            server.Objects(), '/api/objects',
            {'/': { 'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
            }
    )

    # start cherrypy engine
    cherrypy.engine.start()
    cherrypy.engine.block()

    #config = {'server.socket_host': 'localhost',
    #          'server.socker_port': 80,
    #          'response.timeout': 6000
    #          }


if __name__ == "__main__":
    main()
