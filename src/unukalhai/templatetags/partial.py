from django import template
from unukalhai.controller import get_partial_class

register = template.Library()

def do_partial(parser, token):
    """Parse the node"""
    lst = token.split_contents()
    rest = [parser.compile_filter(t) for t in lst[3:]]
    return PartialNode(lst[1], lst[2], rest)

class PartialNode(template.Node):
    """Render a partial
    {% partial blog comment comment %}"""
    def __init__(self, partial, action, args):
        self.controller = partial
        self.action = action
        self.args = args
        self.prt_cls = get_partial_class(partial)
        
    def render(self, context):
        dct = [n.resolve(context) for n in self.args]
        partial = self.prt_cls(*dct)
        return partial._run(self.action)

register.tag('partial', do_partial)