from application import ApplicationController
from ..model.quote import Quote
import routes

class HomeController(ApplicationController):
    def index(self):
        self.tpl["quotes"] = Quote.all().order('-created_at').fetch(10)

    def about(self):
        pass