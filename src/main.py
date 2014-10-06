import logging
import os
import re
import sys
import wsgiref.handlers

from google.appengine.ext import webapp

from google.appengine.dist import use_library
use_library('django', '1.0')

sys.path.append(os.path.join(os.path.dirname(__file__), 'unukalhai', 'ext'))

import unukalhai
unukalhai.debug = True

def main():
    app = webapp.WSGIApplication([
                (r'.*', unukalhai.Handler),
            ], debug=unukalhai.debug)
    wsgiref.handlers.CGIHandler().run(app)

if __name__ == '__main__':
    main()
