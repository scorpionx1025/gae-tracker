# encoding=utf-8

import logging
import os
import sys
import wsgiref.handlers

from google.appengine.ext import webapp

import handlers

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)

    sys.path.insert(0, os.path.dirname(__file__))
    webapp.template.register_template_library('filters')

    wsgiref.handlers.CGIHandler().run(webapp.WSGIApplication(handlers.handlers, debug=True))
