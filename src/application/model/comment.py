from google.appengine.ext import db
from gaeo.model import BaseModel, SearchableBaseModel
from application.model.user import User

class Comment(BaseModel):
    content = db.TextProperty(required=True)
    rating = db.RatingProperty()

Comment.belongs_to(User)