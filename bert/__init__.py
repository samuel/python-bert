
"""BERT-RPC Library"""

__version__ = "1.0.0"

from bert.codec import BERTDecoder, BERTEncoder
from erlastic import Atom

def encode(obj):
    return BERTEncoder().encode(obj)

def decode(obj):
    return BERTDecoder().decode(obj)
