#!/bin/bash/python

try:
    import sys
    can_sys = True
except ImportError:
    can_sys = False

try:
    import ast
    can_ast = True
except ImportError:
    can_ast = False

try:
    import json
    can_json = True
except ImportError:
    can_json = False

try:
    import sqlite3
    can_sqlite3 = True
except ImportError:
    can_sqlite3 = False

try:
    import argparse
    can_argparse = True
except ImportError:
    can_argparse = False

try:
    import cherrypy
    can_cherrypy = True
except ImportError:
    can_cherrypy = False

try:
    import jsonAPI
    can_jsonAPI = True
except ImportError:
    can_jsonAPI = False

# check for missing modules
modules = [('sys', can_sys), ('ast', can_ast), ('json', can_json),
           ('cherrypy', can_cherrypy), ('argparse', can_argparse),
           ('sqlite3', can_sqlite3), ('jsonAPI', can_jsonAPI)]
missing_modules = [x[0] for x in modules if x[1] is False]

if len(missing_modules) > 0:
    print "Please install the following modules: "
    for m in missing_modules:
        print m
    sys.exit(1)
else:
    print "You have all necessary modules!"


