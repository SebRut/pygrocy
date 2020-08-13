def get_val(obj):
    if hasattr(obj, 'as_dict'):
        as_attr = getattr(obj, 'as_dict')
        return as_attr()
    else:
        return obj


class DataModel(object):
    def as_dict(self):
        return {k: get_val(getattr(self, k)) for k, v in self.__class__.__dict__.items() if type(v) is property}
