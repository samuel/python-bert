
from bert.erlang import ErlangTermDecoder, ErlangTermEncoder, Atom, Binary
from bert.codec import BERTDecoder, BERTEncoder

def erlang_encode(obj):
    return ErlangTermEncoder().encode(obj)

def erlang_decode(obj):
    return ErlangTermDecoder().decode(obj)

def encode(obj):
    return BERTEncoder().encode(obj)

def decode(obj):
    return BERTDecoder().decode(obj)
