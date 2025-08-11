#inverted_index.py will handle document storage, tokenization, and building the index.

import re
from collections import defaultdict

class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(lambda: defaultdict(list))  # token → {doc_id: [positions]}
        self.documents = {}  # doc_id → original text

    def tokenize(self, text):
        # Simple tokenizer: lowercase, split on non-alphanumeric
        return re.findall(r'\w+', text.lower())

    def add_document(self, doc_id, text):
        self.documents[doc_id] = text
        tokens = self.tokenize(text)
        for pos, token in enumerate(tokens):
            self.index[token][doc_id].append(pos)

    def get_documents(self, token):
        """Return dict of {doc_id: [positions]} for this token."""
        return self.index.get(token, {})

    def all_tokens(self):
        return self.index.keys()
