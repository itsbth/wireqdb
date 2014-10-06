from application import ApplicationController
from ..controller import check_access
from ..model.quote import Quote
from ..model.rating import Rating
from ..model.user import User, USER_LEVEL_NORMAL, USER_LEVEL_STAFF
from ..model.counter import get_count, increment, decrement

try:
    import json
except ImportError:
        import simplejson as json
import math
import datetime, time

_RATING_MAX = 2**32-1

class QuoteController(ApplicationController):
    def index(self):
        last = self.arg['id'] is not None and datetime.datetime.fromtimestamp(int(self.arg['id'])) or datetime.datetime.now()
        quotes = Quote.gql("WHERE created_at < :1 ORDER BY created_at DESC", last).fetch(10)
        offset = len(quotes) == 10 and time.mktime(quotes[-1].created_at.timetuple()) or 0
        self.tpl['quotes'] = quotes
        self.tpl['offset'] = str(int(offset))
        self.tpl['total'] = int(get_count("total_quotes"))
        #self.tpl['pages'] = range(math.ceil(self.tpl['total'] / 10))
        
    def show(self):
        self.tpl['q'] = Quote.get(self.arg['id'])
        
    def top(self):
        last = self.arg.get('id', 0)
        quotes = Quote.gql("WHERE rating < :1 ORDER BY rating DESC", last).fetch(10)
        offset = len(quotes) == 10 and quotes[-1].rating
        self.tpl['quotes'] = quotes
        self.tpl['offset'] = str(int(offset))
        self.tpl['total'] = int(get_count("total_quotes"))
        #self.tpl['pages'] = range(math.ceil(self.tpl['total'] / 10))
        
    @check_access(USER_LEVEL_NORMAL)
    def new(self):
        pass
    
    @check_access(USER_LEVEL_NORMAL)
    def create(self):
        content = self.hnd.request.get('content')
        tags = self.hnd.request.get('tags')
        s = Quote(content=content, user=User.get_current_user())
        s.tags = tags.lower().split()
        s.save()
        increment("total_quotes")
        self.redirect(controller='home')
    
    @check_access(USER_LEVEL_NORMAL)
    def rate(self):
        try:
            u = self.user_obj
            if not u:
                return self.render(json.dumps("must log in"))
            q = Quote.get(self.arg['id'])
            r = Rating.get_by_user_and_quote(u, q)
            if not r:
                r = Rating(user=u, quote=q)
            dir = int(self.hnd.request.get('rating'))
            if not (dir == 1 or dir == 0 or dir == -1): return self.render(json.dumps("error"))
            if r.dir != dir:
                q.rating += dir
                r.dir = dir
                q.save()
                r.save()
            return self.render(json.dumps(q.rating))
        except Exception, e:
            self.render(json.dumps("error: " + str(e)))
            
    @check_access(USER_LEVEL_STAFF)
    def delete(self):
        q = Quote.get(self.arg['id'])
        if q is not None:
            q.delete()
            decrement("total_quotes")
        self.redirect(controller='quote')
        
    def tag(self):
        self.tpl['tag'] = self.arg['id']
        self.tpl['quotes'] = Quote.gql("WHERE tags = :1", self.arg['id'])