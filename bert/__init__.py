
"""BERT-RPC Library"""

from bert.codec import BERTDecoder, BERTEncoder
from erlastic import Atom

encode = BERTEncoder().encode
decode = BERTDecoder().decode
