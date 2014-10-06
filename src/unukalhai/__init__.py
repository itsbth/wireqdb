"""Unukalhai web framework"""
from google.appengine.ext import webapp
from unukalhai.dispatcher import dispatch

debug = False

class Handler(webapp.RequestHandler):
    """Unukalhai main handler"""
    
    __name__ = "unukalhai.Handler" # No idea why this is needed
    def get(self, *args):
        self.__process_request()

    def post(self, *args):
        self.__process_request()
        
    def head(self, *args):
        self.__process_request()
        
    def options(self, *args):
        self.__process_request()
        
    def put(self, *args):
        self.__process_request()
        
    def delete(self, *args):
        self.__process_request()
        
    def trace(self, *args):
        self.__process_request()

    def __process_request(self):
        """dispatch the request"""
        dispatcher.dispatch(self)