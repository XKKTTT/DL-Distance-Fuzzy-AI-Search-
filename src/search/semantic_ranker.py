from sentence_transformers import SentenceTransformer, util
import torch 

class SemanticRanker:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def rerank(self, query, results):
        """
        Rerank the results based on semantic similarity to the query.
        
        :param query: The search query string.
        :param results: List of (doc_id, score, text) from the fuzzy search.

        :return: List of (doc_id, new_score, text) sorted by semantic similarity.
        """

        if not results:
            return []
    
        docs = [text for _,_,text in results] 


        # Encode the query and results
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        print("Query embedding:", query_embedding.shape)
        doc_embeddings = self.model.encode(docs, convert_to_tensor=True)
        print("Document embeddings:", doc_embeddings.shape)

        # Compute cosine similarities
        similarities = util.cos_sim(query_embedding, doc_embeddings)
        print("Similarities:", similarities)
        similarities = similarities[0] # Remove the batch dimension

        similarities = similarities.cpu().numpy()

        reranked = [(doc_id, float(similarity_score), text) for (doc_id, _, text), similarity_score in zip(results, similarities)]

        reranked.sort(key=lambda x: x[1], reverse=True)

        return reranked
    

    def score(self, query: str, docs: list) -> list[float]:
        """
        Compute semantic similarity scores between query and a list of docs.
        Returns a list of floats.
        """
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        
        doc_embeddings = self.model.encode(docs, convert_to_tensor=True)

        similarity_scores = util.cos_sim(query_embedding, doc_embeddings)[0]

        return similarity_scores.cpu().numpy().tolist()


