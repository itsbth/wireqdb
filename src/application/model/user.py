from google.appengine.ext import db
from google.appengine.api import users
from unukalhai.model import Model

"""Unable to access the site."""
USER_LEVEL_BLOCKED = -2
"""Able to read, but not edit or create new."""
USER_LEVEL_BANNED = -1
"""Normal user."""
USER_LEVEL_NORMAL = 0
"""Able to edit and delete."""
USER_LEVEL_STAFF = 1
"""Able to edit user level"""
USER_LEVEL_ADMIN = 2

LEVEL_MAP = dict(blocked=USER_LEVEL_BLOCKED, banned=USER_LEVEL_BANNED, normal=USER_LEVEL_NORMAL, staff=USER_LEVEL_STAFF, admin=USER_LEVEL_ADMIN)
MAP_LEVEL = {}
for k in LEVEL_MAP.keys():
    MAP_LEVEL[LEVEL_MAP[k]] = k.capitalize()

USER_KEY_PREFIX = "usr##"

class User(Model):
    user = db.UserProperty()
    level = db.IntegerProperty(default=USER_LEVEL_NORMAL)
    first_seen = db.DateTimeProperty(auto_now_add=True)
    
    def is_staff(self):
        return self.level >= USER_LEVEL_STAFF
    
    def is_admin(self):
        return self.level >= USER_LEVEL_ADMIN
    
    def level_name(self):
        return MAP_LEVEL[self.level]
    
    @classmethod
    def get_or_insert_by_email(cls, mail, usr=None):
        key = USER_KEY_PREFIX + mail
        return cls.get_or_insert(key, user=usr, level=0)
    
    @classmethod
    def get_current_user(cls):
        usr = users.get_current_user()
        if usr is None: return None
        userobj = cls.get_or_insert_by_email(usr.email(), usr)
        if users.is_current_user_admin() and userobj.level != USER_LEVEL_ADMIN:
            userobj.level = USER_LEVEL_ADMIN
            userobj.save()
        #self._current_user = userobj
        return userobj