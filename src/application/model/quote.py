from google.appengine.ext import db
from unukalhai.model import Model
from application.model.user import User

class Quote(Model):
    content = db.TextProperty(required=True)
    comment = db.StringProperty()
    tags = db.StringListProperty()
    rating = db.IntegerProperty(default=0)
    created_at = db.DateTimeProperty(auto_now_add=True)

Quote.belongs_to(User)