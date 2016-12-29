from collections import OrderedDict
import json

class OrderDict(OrderedDict):
    def __init__(self, *args, **kwds):
        OrderedDict.__init__(*args, **kwds)

    def dumps(self):
        return '{"data":%s, "index":%s}' % (json.dumps(self), json.dumps(self.keys()))

    def loads(self, obj):
        if isinstance(obj, str) or isinstance(obj, unicode):
            str_json = json.loads(obj)
        elif isinstance(obj, dict):
            str_json = obj
            if 'data' not in str_json or 'index' not in str_json or \
                not isinstance(str_json['data'], dict):
                raise ValueError(u"%s is not a vaild OrderDict dumps string or dict" % unicode(obj))
        else:
            raise ValueError(u"%s is not a vaild OrderDict dumps string or dict" % unicode(obj))

        for item in str_json['index']:
            self[item] = str_json['data'].get(item)
        return self
