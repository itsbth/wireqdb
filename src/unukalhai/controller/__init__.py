"""Unukalhai base controller"""
from os import listdir
import sys, traceback, StringIO

from django.conf import settings

settings._target = None

settings.configure(TEMPLATE_DIRS = ('application/templates',),
                   INSTALLED_APPS = ('unukalhai', 'application',))

from django.template import Template, Context
from django.template import loader

import unukalhai
from unukalhai.ext import routes

_TEMPLATE_CACHE = {}

def get_template(path):
    if path in _TEMPLATE_CACHE and not unukalhai.debug:
        return _TEMPLATE_CACHE[path]
    tpl = loader.get_template(path)
    _TEMPLATE_CACHE[path] = tpl
    return tpl

class Partial:
    _has_rendered = False
    def __init__(self, **kwargs):
        self.tpl = Context()
        self.arg = kwargs
        self.out = StringIO.StringIO()
        
    def render(self, msg):
        self._has_rendered = True
        self.out.write(msg)
    
    def _run(self, action, format='html'):
        action_m = getattr(self, action, None)
        if action_m:
            action_m()
            if not self._has_rendered:
                template = get_template("partial/%s/%s.%s" % (self.__class__.__name__[:5].lower(), action, format))
                self.render(template.render(self.tpl))
        else:
            raise Exception("Action not found")
        return self.out.getvalue()
    
class Controller:
    """Unukalhai base controller"""
    
    _has_rendered = False
    
    def __init__(self, hnd, arg):
        self.hnd = hnd
        self.arg = arg
        self.tpl = Context()
        
    def error_404(self):
        self.hnd.error(404)
        self.hnd.response.headers["Content-Type"] = "text/plain"
        self.render("404 Not Found")
    error_404.is_action = False
    
    def error_403(self):
        self.hnd.error(403)
        self.hnd.response.headers["Content-Type"] = "text/plain"
        self.render("403 Forbidden")
    error_403.is_action = False
    
    def error_500(self, reason):
        self.hnd.error(500)
        self.hnd.response.headers["Content-Type"] = "text/plain"
        if unukalhai.debug:
            self.render("500 Internal Server error\n")
            traceback.print_exc(25, self.hnd.response.out)
        else:
            self.render("500 Internal Server error")
    error_500.is_action = False
    
    def render(self, msg):
        self._has_rendered = True
        self.hnd.response.out.write(msg)
    render.is_action = False
    
    def redirect(self, *args, **kwargs):
        self.hnd.redirect(routes.url_for(*args, **kwargs))
        self._has_rendered = True
    redirect.is_action = False
    
    def url_for(self, *args, **kwargs):
        return routes.url_for(*args, **kwargs)
    url_for.is_action = False
    
    def _run(self, action):
        action_m = getattr(self, action, None)
        try:
            if action[1] != '_' and action_m and callable(action_m) and getattr(action_m, 'is_action', True):
                action_m()
                if not self._has_rendered:
                    template = get_template("controller/%s/%s.%s" % (self.arg['controller'], self.arg['action'], self.arg.get('format', 'html')))
                    self.render(template.render(self.tpl))
            else:
                self.error_404()
        except Exception, e:
            self.error_500(e)

def get_partial_class(partial):
    """Get the class from the partial name"""
    exec("from application.partial.%s import %sPartial" % (partial, partial.capitalize()))
    prt_cls = eval("%sPartial" % (partial.capitalize(),))
    return prt_cls

def get_controllers():
    """Get a list of all the controllers"""
    lst = map(lambda f: f[:-3], filter(lambda f: f[-3:] == '.py', listdir("application/controller/")))
    lst.remove("application")
    lst.remove("__init__")
    return lst

def register_controllers(m):
    """Register all controllers"""
    m.create_regs(get_controllers())

