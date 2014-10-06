from application import ApplicationController
from ..controller import check_access
from ..model.quote import Quote
from ..model.user import User, MAP_LEVEL, LEVEL_MAP, USER_LEVEL_STAFF, USER_LEVEL_ADMIN
from ..model.report import Report

class UsrController(ApplicationController):
    @check_access(USER_LEVEL_STAFF)
    def index(self):
        self.tpl['users'] = User.all().fetch(1000)
    
    @check_access(USER_LEVEL_ADMIN)
    def set_access(self):
        usr = User.get(self.arg['id'])
        usr.level = LEVEL_MAP[self.hnd.request.get('access').lower()]
        usr.save()
        self.redirect(controller='usr')
        
    def form(self):
        usr = User.get(self.arg['id'])
        self.tpl['id'] = self.arg['id']
        self.tpl['access'] = MAP_LEVEL[usr.level]
        self.tpl['levels'] = MAP_LEVEL.values()