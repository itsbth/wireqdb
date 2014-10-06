from application import ApplicationController
from ..controller import check_access
from ..model.quote import Quote
from ..model.user import User, USER_LEVEL_NORMAL, USER_LEVEL_STAFF
from ..model.report import Report


class ReportController(ApplicationController):
    
    @check_access(USER_LEVEL_STAFF)
    def index(self):
        self.tpl['lst'] = Report.gql("WHERE active = TRUE").fetch(10)
        
    @check_access(USER_LEVEL_STAFF)
    def manage(self):
        r = Report.get(self.hnd.request.get('key'))
        if self.hnd.request.get('action') == 'dq':
            r.quote.delete()
            r.active = False
            r.save()
        elif self.hnd.request.get('action') == 'dr':
            r.active = False
            r.save()
        self.redirect(controller='report', action='index')
    
    def new(self):
        self.tpl['id'] = self.arg['id']
    
    @check_access(USER_LEVEL_NORMAL)
    def create(self):
        q = Quote.get(self.arg['id'])
        if q is None: return self.render("Error")
        u = self.user_obj
        r = Report(reason=self.hnd.request.get('reason'), quote=q, user=u)
        r.save()
        self.render('Success')
        
        