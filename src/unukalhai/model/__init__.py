import re
from google.appengine.ext import db, gql

def _pluralize(noun):
    if re.search('[sxz]$', noun):
        return re.sub('$', 'es', noun)
    elif re.search('[^aeioudgkprt]h$', noun):
        return re.sub('$', 'es', noun)
    elif re.search('[^aeiou]y$', noun):
        return re.sub('y$', 'ies', noun)
    else:
        return noun + 's'

class Model(db.Model):
    @classmethod
    def belongs_to(cls, ref_cls, name = None, plural_name = None, **kwargs):
        name = name or ref_cls.__name__.lower()
        plural_name = plural_name or _pluralize(name)
        prop = db.ReferenceProperty(ref_cls, **kwargs)
        cls._properties[name] = prop
        prop.__property_config__(cls, name)
        setattr(cls, name, prop)
        def getter(cls):
            return cls.gql("WHERE %s = :1" % (name,), self)
        setattr(ref_cls, plural_name, getter)