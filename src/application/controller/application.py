from google.appengine.api import users
from ..model.user import User, USER_LEVEL_BLOCKED, USER_LEVEL_BANNED
from unukalhai.controller import Controller, get_template

class ApplicationController(Controller):
    """
    The base controller init mixin
    """
    def application_init(self):
        """
        default initialization method invoked by dispatcher
        """
        self.is_logged_in = users.get_current_user() is not None
        self.user = users.get_current_user()
        self.user_obj = User.get_current_user()
        self.is_admin = users.is_current_user_admin()
        if self.user_obj is not None and \
            self.user_obj.level == USER_LEVEL_BLOCKED:
            return self.error_403()
        self.tpl["is_logged_in"] = self.is_logged_in
        self.tpl["is_banned"] = self.user_obj and self.user_obj.level <= USER_LEVEL_BANNED
        self.tpl["user"] = self.user
        self.tpl["user_obj"] = self.user_obj
        self.tpl["login_url"] = users.create_login_url(self.hnd.request.path)
        self.tpl["logout_url"] = users.create_logout_url(self.hnd.request.path)
    
    def error_403(self):
        self.render(get_template("error/403.%s" % (self.arg['format'],)).render(self.tpl))
        