

from src.indexing.dl_matcher import find_near_exact_matches
from src.indexing.inverted_index import InvertedIndex
from src.search.semantic_ranker import SemanticRanker
from collections import defaultdict


#search_engine.py will orchestrate the search 
# it’ll take a query, break it into tokens, use find_near_exact_matches for fuzzy matching, and rank results.

class SearchEngine:
    def __init__(self, index: InvertedIndex, use_semantic = False, alpha=0.5, beta=0.5):
        self.index = index
        self.use_semantic = use_semantic
        self.alpha = alpha  # Weight for fuzzy match score
        self.beta = beta    # Weight for semantic match score
        self.semantic_ranker = SemanticRanker() if use_semantic else None


    def search(self, query: str, top_k = None):
        fuzzy_scores = defaultdict(int)  # doc_id: score
        query_tokens = self.index.tokenize(query) #returns a list of the tokens 

        for q_token in query_tokens:
            for token in self.index.all_tokens():

                # Use DL ≤ 1 matcher to check token similarity
                match_positions = find_near_exact_matches(token, q_token)

                if len(match_positions) == 0:
                    continue 
                
                if any(dist <= 1 for dist in match_positions.values()):
                    #check if this index token matches the query token with ≤ 1 edit
                    #if so we treat it as a match 

                    #get all the documents containing this token 
                    docs = self.index.get_documents(token)

                    #count fuzzy scores 
                    for doc_id, positions in docs.items():
                        fuzzy_scores[doc_id] += len(positions)  # score: occurrences



        # Convert scores to a list of tuples (doc_id, score, text)

        
        results_with_text = [(doc_id, fuzzy_score, self.index.documents[doc_id]) for doc_id, fuzzy_score in fuzzy_scores.items()]


        #Do semantic search if semantic reranking is enabled 
        if self.use_semantic:
            docs_text = [doc for _,_,doc in results_with_text]
            semantic_scores = self.semantic_ranker.score(query, docs_text)

            combined_results = []

            for (doc_id, fuzzy_score, text), semantic_score in zip(results_with_text, semantic_scores):
                #calculated weighted final score 
                final_score = self.alpha * fuzzy_score + self.beta * semantic_score
                combined_results.append((doc_id, final_score, text)) 
            
            #Reorder results based on combined scores
            combined_results.sort(key = lambda x : x[1], reverse=True)


        final_results = []
        if self.use_semantic:
            final_results = combined_results
        else:
            final_results = results_with_text 

        if top_k:
            top_k = max(top_k, len(final_results))
            return final_results[:top_k]
        else:
            return final_results

                



            
