from django import template
from unukalhai.ext import routes
import re

#_SPLIT_RE = re.compile(r'(?P<key>\w+)=(?P<value>[^" ]+|"(.+?)[^\\]")')
_SPLIT_RE = re.compile(r'(?P<key>\w+)=(?P<value>[^" ]+)')

register = template.Library()

def do_url_for(parser, token):
    split = token.split_contents()
    del split[0]
    name = split[0]
    if name.find("=") == -1:
        del split[0]
    else:
        name = None
    rest = ' '.join(split)
    list = _SPLIT_RE.findall(rest)
    if not (list or name):
        raise template.TemplateSyntaxError("malformatted url_for tag")
    kwargs = {}
    for pair in list:
        kwargs[pair[0]] = pair[1]
    return UrlForNode(name, kwargs)

class UrlForNode(template.Node):
    def __init__(self, name, kwargs):
        self.name = name
        self.kwargs = kwargs
        
    def render(self, context):
        kwargs = self.kwargs.copy()
        for k in kwargs:
            if kwargs[k][0] == "'" and kwargs[k][-1] == "'":
                kwargs[k] = kwargs[k][1:-1]
            elif kwargs[k] in context:
                kwargs[k] = context[kwargs[k]]
        if self.name:
            return routes.url_for(self.name, **kwargs)
        else:
            return routes.url_for(**kwargs)

register.tag('url_for', do_url_for)