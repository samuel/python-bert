
import datetime
import re
import time

from erlastic import ErlangTermDecoder, ErlangTermEncoder, Atom

def utc_to_datetime(seconds, microseconds):
    return datetime.datetime.utcfromtimestamp(seconds).replace(microsecond=microseconds)

def datetime_to_utc(dt):
    # Can't use time.mktime as it assume local timezone
    delta = dt - datetime.datetime(1970, 1, 1, 0, 0)
    return delta.days * 24 * 60 * 60 + delta.seconds, dt.microsecond

class BERTDecoder(ErlangTermDecoder):
    def decode(self, bytes, offset=0):
        obj = super(BERTDecoder, self).decode(bytes, offset)
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
            if 'ignorecase' in item[3]:
                flags |= re.IGNORECASE
            if 'multiline' in item[3]:
                flags |= re.MULTILINE
            if 'dotall' in item[3]:
                flags |= re.DOTALL
            return re.compile(item[2], flags)
        raise NotImplementedError("Unknown BERT type %s" % item[1])

class BERTEncoder(ErlangTermEncoder):
    def encode(self, obj):
        bert = self.convert(obj)
        return super(BERTEncoder, self).encode(bert)

    def convert(self, obj):
        if obj is True:
            return (Atom("bert"), Atom("true"))
        elif obj is False:
            return (Atom("bert"), Atom("false"))
        elif obj is None:
            return (Atom("bert"), Atom("nil"))
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
        elif str(type(obj)) == "<type '_sre.SRE_Pattern'>":
            raise NotImplementedError("It is impossible to serialize a regex object")
        return obj

def datetime_to_split_time(dt):
    seconds = int(time.mktime(dt.timetuple()))
    megaseconds = seconds // 1000000
    seconds = seconds % 1000000
    microseconds = dt.microsecond
    return megaseconds, seconds, microseconds
