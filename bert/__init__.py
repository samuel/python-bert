
"""BERT-RPC Library"""

__version__ = "1.0.0"

from bert.codec import BERTDecoder, BERTEncoder
from erlastic import Atom

encode = BERTEncoder().encode
decode = BERTDecoder().decode
