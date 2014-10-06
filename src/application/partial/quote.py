from unukalhai.controller import Partial
from application.model.user import User

class QuotePartial(Partial):
    def __init__(self, quote=None):
        Partial.__init__(self)
        self.tpl["quote"] = quote
        self.tpl["user_obj"] = User.get_current_user()
    def view_full(self):
        pass
    def form(self):
        pass