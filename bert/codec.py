
import datetime
import re
import time

from erlastic import ErlangTermDecoder, ErlangTermEncoder, Atom

def utc_to_datetime(seconds, microseconds):
    return datetime.datetime.utcfromtimestamp(seconds).replace(microsecond=microseconds)

def datetime_to_utc(dt):
    # Can't use time.mktime as it assumes local timezone
    delta = dt - datetime.datetime(1970, 1, 1, 0, 0)
    return delta.days * 24 * 60 * 60 + delta.seconds, dt.microsecond

RE_TYPE = type(re.compile("foo"))

class BERTDecoder(object):
    def __init__(self, encoding="utf-8"):
        self.encoding = encoding
        self.erlang_decoder = ErlangTermDecoder()

    def decode(self, bytes, offset=0):
        obj = self.erlang_decoder.decode(bytes, offset)
        return self.convert(obj)

    def convert(self, item):
        if isinstance(item, tuple):
            if item[0] == "bert":
                return self.convert_bert(item)
            return tuple(self.convert(i) for i in item)
        elif isinstance(item, list):
            if item[0] == "bert":
                return self.convert_bert(item)
            return [self.convert(i) for i in item]
        return item

    def convert_bert(self, item):
        if item[1] == "nil":
            return None
        elif item[1] == "unicode":
            return item[2].decode(self.encoding)
        elif item[1] == "dict":
            return dict((self.convert(k), self.convert(v)) for k, v in item[2])
        elif item[1] in ("true", True):
            return True
        elif item[1] in ("false", False):
            return False
        elif item[1] == "time":
            return utc_to_datetime(item[2] * 1000000 + item[3], item[4])
        elif item[1] == "regex":
            flags = 0
            if 'extended' in item[3]:
                flags |= re.VERBOSE
            if 'caseless' in item[3]:
                flags |= re.IGNORECASE
            if 'multiline' in item[3]:
                flags |= re.MULTILINE
            if 'dotall' in item[3]:
                flags |= re.DOTALL
            return re.compile(item[2], flags)
        raise NotImplementedError("Unknown BERT type %s" % item[1])

class BERTEncoder(object):
    def __init__(self, encoding="utf-8"):
        self.encoding = encoding
        self.erlang_encoder = ErlangTermEncoder()

    def encode(self, obj):
        bert = self.convert(obj)
        return self.erlang_encoder.encode(bert)

    def convert(self, obj):
        if obj is True:
            return (Atom("bert"), Atom("true"))
        elif obj is False:
            return (Atom("bert"), Atom("false"))
        elif obj is None:
            return (Atom("bert"), Atom("nil"))
        elif isinstance(obj, unicode):
            return (Atom("bert"), Atom("unicode"), obj.encode(self.encoding))
        elif isinstance(obj, dict):
            return (Atom("bert"), Atom("dict"), [(self.convert(k), self.convert(v)) for k, v in obj.items()])
        elif isinstance(obj, datetime.datetime):
            seconds, microseconds = datetime_to_utc(obj)
            megaseconds = seconds // 1000000
            seconds = seconds % 1000000
            return (Atom("bert"), Atom("time"), megaseconds, seconds, microseconds)
        elif isinstance(obj, list):
            return [self.convert(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(self.convert(item) for item in obj)
        elif type(obj) == RE_TYPE:
            options = []
            if obj.flags & re.VERBOSE:
                options.append(Atom('extended'))
            if obj.flags & re.IGNORECASE:
                options.append(Atom('caseless'))
            if obj.flags & re.MULTILINE:
                options.append(Atom('multiline'))
            if obj.flags & re.DOTALL:
                options.append(Atom('dotall'))
            return (Atom("bert"), Atom("regex"), obj.pattern, tuple(options))
        return obj
