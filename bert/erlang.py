
"""Erlang External Term Format serializer/deserializer"""

from __future__ import division

import math
import struct

NEW_FLOAT_EXT     = 'F' # 70  [Float64:IEEE float]
SMALL_INTEGER_EXT = 'a' # 97  [UInt8:Int] Unsigned 8 bit integer
INTEGER_EXT = 'b'       # 98  [Int32:Int] Signed 32 bit integer in big-endian format
FLOAT_EXT = 'c'         # 99  [31:Float String] Float in string format (formatted "%.20e", sscanf "%lf"). Superseded by NEW_FLOAT_EXT
ATOM_EXT = 'd'          # 100 [UInt16:Len, Len:AtomName] max Len is 255
SMALL_TUPLE_EXT = 'h'   # 104 [UInt8:Arity, N:Elements]
LARGE_TUPLE_EXT = 'i'   # 105 [UInt32:Arity, N:Elements]
NIL_EXT = 'j'           # 106 empty list
STRING_EXT = 'k'        # 107 [UInt32:Len, Len:Characters]
LIST_EXT = 'l'          # 108 [UInt32:Len, Elements, Tail]
BINARY_EXT = 'm'        # 109 [UInt32:Len, Len:Data]
SMALL_BIG_EXT = 'n'     # 110 [UInt8:n, UInt8:Sign, n:nums]
LARGE_BIG_EXT = 'o'     # 111 [UInt32:n, UInt8:Sign, n:nums]

class Atom(str):
    def __repr__(self):
        return "Atom(%s)" % super(Atom, self).__repr__()

class Binary(str):
    def __repr__(self):
        return "Binary(%s)" % super(Binary, self).__repr__()

class ErlangTermDecoder(object):
    def __init__(self):
        pass

    def decode(self, bytes, offset=0):
        if bytes[offset] == "\x83": # Version 131
            offset += 1
        return self._decode(bytes, offset)[0]

    def _decode(self, bytes, offset=0):
        tag = bytes[offset]
        offset += 1
        if tag == SMALL_INTEGER_EXT:
            return ord(bytes[offset]), offset+1
        elif tag == INTEGER_EXT:
            return struct.unpack(">l", bytes[offset:offset+4])[0], offset+4
        elif tag == FLOAT_EXT:
            return float(bytes[offset:offset+31].split('\x00', 1)[0]), offset+31
        elif tag == NEW_FLOAT_EXT:
            return struct.unpack(">d", bytes[offset:offset+8])[0], offset+8
        elif tag == ATOM_EXT:
            atom_len = struct.unpack(">H", bytes[offset:offset+2])[0]
            atom = bytes[offset+2:offset+2+atom_len]
            offset += 2+atom_len
            if atom == "true":
                return True, offset
            elif atom == "false":
                return False, offset
            return Atom(atom), offset
        elif tag in (SMALL_TUPLE_EXT, LARGE_TUPLE_EXT):
            if tag == SMALL_TUPLE_EXT:
                arity = ord(bytes[offset])
                offset += 1
            else:
                arity = struct.unpack(">L", bytes[offset:offset+4])[0]
                offset += 4

            items = []
            for i in range(arity):
                val, offset = self._decode(bytes, offset)
                items.append(val)
            return tuple(items), offset
        elif tag == NIL_EXT:
            return [], offset
        elif tag == STRING_EXT:
            length = struct.unpack(">H", bytes[offset:offset+2])[0]
            return bytes[offset+2:offset+2+length], offset+2+length
        elif tag == LIST_EXT:
            length = struct.unpack(">L", bytes[offset:offset+4])[0]
            offset += 4
            items = []
            for i in range(length):
                val, offset = self._decode(bytes, offset)
                items.append(val)
            tail, offset = self._decode(bytes, offset)
            if tail != []:
                # TODO: Not sure what to do with the tail
                raise NotImplementedError("Lists with non empty tails are not supported")
            return items, offset
        elif tag == BINARY_EXT:
            length = struct.unpack(">L", bytes[offset:offset+4])[0]
            return Binary(bytes[offset+4:offset+4+length]), offset+4+length
        elif tag in (SMALL_BIG_EXT, LARGE_BIG_EXT):
            if tag == SMALL_BIG_EXT:
                n = ord(bytes[offset])
                offset += 1
            else:
                n = struct.unpack(">L", bytes[offset:offset+4])[0]
                offset += 4
            sign = ord(bytes[offset])
            offset += 1
            b = 1
            val = 0
            for i in range(n):
                val += ord(bytes[offset]) * b
                b <<= 8
                offset += 1
            if sign != 0:
                val = -val
            return val, offset
        else:
            raise NotImplementedError("Unsupported tag %d" % tag)

class ErlangTermEncoder(object):
    def __init__(self):
        pass

    def encode(self, obj):
        bytes = [chr(131)]
        self._encode(obj, bytes)
        return "".join(bytes)

    def _encode(self, obj, bytes):
        if obj is False:
            bytes += [ATOM_EXT, struct.pack(">H", 5), "false"]
        elif obj is True:
            bytes += [ATOM_EXT, struct.pack(">H", 4), "true"]
        elif isinstance(obj, (int, long)):
            if 0 <= obj <= 255:
                bytes += [SMALL_INTEGER_EXT, chr(obj)]
            elif -2147483648 <= obj <= 2147483647:
                bytes += [INTEGER_EXT, struct.pack(">l", obj)]
            else:
                n = int(math.ceil(math.log(obj, 2) / 8))
                if n <= 256:
                    bytes += [SMALL_BIG_EXT, chr(n)]
                else:
                    bytes += [LARGE_BIG_EXT, struct.pack(">L", n)]
                if obj >= 0:
                    bytes.append("\x00")
                else:
                    bytes.append("\x01")
                    obj = -obj
                while obj > 0:
                    bytes.append(chr(obj & 0xff))
                    obj >>= 8
        elif isinstance(obj, float):
            floatstr = "%.20e" % obj
            bytes += [FLOAT_EXT, floatstr + "\x00"*(31-len(floatstr))]
        elif isinstance(obj, Atom):
            bytes += [ATOM_EXT, struct.pack(">H", len(obj)), obj]
        elif isinstance(obj, (Binary, buffer)):
            bytes += [BINARY_EXT, struct.pack(">L", len(obj)), obj]
        elif isinstance(obj, str):
            bytes += [STRING_EXT, struct.pack(">H", len(obj)), obj]
        elif isinstance(obj, unicode):
            self._encode([ord(x) for x in obj], bytes)
        elif isinstance(obj, tuple):
            n = len(obj)
            if n < 256:
                bytes += [SMALL_TUPLE_EXT, chr(n)]
            else:
                bytes += [LARGE_TUPLE_EXT, struct.pack(">L", n)]
            for item in obj:
                self._encode(item, bytes)
        elif obj == []:
            bytes.append(NIL_EXT)
        elif isinstance(obj, list):
            bytes += [LIST_EXT, struct.pack(">L", len(obj))]
            for item in obj:
                self._encode(item, bytes)
            bytes.append(NIL_EXT) # list tail - no such thing in Python
        else:
            raise NotImplementedError("Unable to serialize %r" % obj)
