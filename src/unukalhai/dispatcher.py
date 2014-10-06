"""Unukalhai dispatcher"""
import sys
import urls
from unukalhai import controller
from routes import url_for

def dispatch(hnd):
    """Dispatch the request to the correct controller"""
    hnd.response.headers["Content-Type"] = "text/html"
    tmp = urls.m.routematch(hnd.request.path)
    if tmp is None:
        hnd.error(404)
        hnd.response.headers["Content-Type"] = "text/plain"
        hnd.response.out.write("404 Not Found")
        return
    m, route = tmp
    if 'format' in route.defaults and hnd.request.path[-1] != '/'\
        and not hnd.request.POST and hnd.request.path.find("?"):
        hnd.redirect(hnd.request.path + '/', True)
        return
    try:
        #exec("from application.controller.%s import %sController" % (m['controller'], m['controller'].capitalize()))
        __import__("application.controller.%s" % (m['controller'],))
        mod = sys.modules["application.controller.%s" % (m['controller'],)]
        print repr(mod), str(dir(mod))
        cnt_clz = getattr(mod, "%sController" % (m['controller'].capitalize(),))
        cnt = cnt_clz(hnd, m)
        if not isinstance(cnt, controller.Controller):
            hnd.error(500)
            hnd.response.headers["Content-Type"] = "text/plain"
            hnd.response.out.write("Invalid controller")
            return
        cnt.application_init()
        cnt._run(m['action'])
    except ImportError, e:
        hnd.error(404)
        hnd.response.headers["Content-Type"] = "text/plain"
        hnd.response.out.write("404 Not Found\n")
        hnd.response.out.write(str(e))