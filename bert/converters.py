
import datetime
import re

from bert.erlang import ErlangTermDecoder

class BERTDecoder(ErlangTermDecoder):
    def __init__(self):
        pass

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
        elif item[1] == "true":
            return True
        elif item[1] == "false":
            return False
        elif item[1] == "time":
            return datetime.timedelta(seconds=item[2] * 1000000 + item[3], microseconds=item[4])
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
        return None
