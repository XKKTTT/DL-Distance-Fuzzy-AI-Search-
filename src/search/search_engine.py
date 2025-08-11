

from src.indexing.dl_matcher import find_near_exact_matches
from src.indexing.inverted_index import InvertedIndex
from collections import defaultdict


#search_engine.py will orchestrate the search 
# it’ll take a query, break it into tokens, use find_near_exact_matches for fuzzy matching, and rank results.

class SearchEngine:
    def __init__(self, index: InvertedIndex):
        self.index = index

    def search(self, query):
        results = defaultdict(int)  # doc_id → score
        query_tokens = self.index.tokenize(query)

        for q_token in query_tokens:
            for token in self.index.all_tokens():
                # Use DL ≤ 1 matcher to check token similarity
                match_positions = find_near_exact_matches(token, q_token)
                
                if any(dist <= 1 for dist in match_positions.values()):
                    docs = self.index.get_documents(token)
                    for doc_id, positions in docs.items():
                        results[doc_id] += len(positions)  # score: occurrences

        # Sort results by score
        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
        return [(doc_id, score, self.index.documents[doc_id]) for doc_id, score in sorted_results]
