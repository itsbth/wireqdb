def check_access(min_access):
    def outer(fn):
        def inner(self, *args, **kwargs):
            if not self.user_obj:
                return self.error_403()
            if self.user_obj.level < min_access:
                return self.error_403()
            return fn(self, *args, **kwargs)
            print self.user_obj.level, min_access
        return inner
    return outer