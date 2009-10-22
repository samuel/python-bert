
from bert.codec import BERTDecoder, BERTEncoder

def encode(obj):
    return BERTEncoder().encode(obj)

def decode(obj):
    return BERTDecoder().decode(obj)
