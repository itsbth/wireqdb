from google.appengine.ext import db
from unukalhai.model import Model
from application.model.user import User
from application.model.quote import Quote

class Rating(Model):
    created_at = db.DateTimeProperty(auto_now_add=True)
    dir = db.IntegerProperty()
    
    @classmethod
    def get_by_user_and_quote(cls, user, quote):
        ret = cls.gql("WHERE user = :1 AND quote = :2", user, quote).fetch(1)
        if ret: ret = ret[0]
        return ret

Rating.belongs_to(User)
Rating.belongs_to(Quote)