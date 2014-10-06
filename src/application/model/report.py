from google.appengine.ext import db
from unukalhai.model import Model
from application.model.user import User
from application.model.quote import Quote

class Report(Model):
    reason = db.TextProperty(required=True)
    active = db.BooleanProperty(required=True, default=True)
    created_at = db.DateTimeProperty(auto_now_add=True)

Report.belongs_to(User)
Report.belongs_to(Quote)