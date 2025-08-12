# tests/test_search_engine.py

from src.indexing.inverted_index import InvertedIndex
from src.search.search_engine import SearchEngine

# 1. Create the index and add documents
index = InvertedIndex()
index.add_document("doc1", "The presldent will address the nati0n tomorrow.")
index.add_document("doc2", "Nation building is a collective effort.")
index.add_document("doc3", "The Prime Minister will speak to the country.")
index.add_document("doc4", "A national holiday has been declared.")
index.add_document("doc5", "President to speak on unity and growth.")

# 2. Function to run and display results
def run_search(engine, query):
    print(f"\n🔍 Query: '{query}'")
    results = engine.search(query, top_k=5)
    if not results:
        print("No results found.")
        return
    for rank, (doc_id, score, text) in enumerate(results, start=1):
        print(f"{rank}. {doc_id} | score={score:.4f}\n   {text}")

# 3. Test fuzzy search (typo-tolerant only)
print("\n=== FUZZY SEARCH ONLY ===")
fuzzy_engine = SearchEngine(index, use_semantic=False)
run_search(fuzzy_engine, "nation")
run_search(fuzzy_engine, "president")
run_search(fuzzy_engine, "presedent")  # Typo
run_search(fuzzy_engine, "address the nation")

# 4. Test hybrid search (fuzzy + semantic reranking)
print("\n=== HYBRID SEARCH (Fuzzy + Semantic) ===")
semantic_engine = SearchEngine(index, use_semantic=True, alpha=0.6, beta=0.4)
run_search(semantic_engine, "nation")
run_search(semantic_engine, "president")
run_search(semantic_engine, "head of state")  # Semantic match to 'president'
run_search(semantic_engine, "speak to the country")

