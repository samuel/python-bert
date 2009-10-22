
"""BERT-RPC Library"""

__version__ = "0.0.1"

from bert.codec import BERTDecoder, BERTEncoder

def encode(obj):
    return BERTEncoder().encode(obj)

def decode(obj):
    return BERTDecoder().decode(obj)
