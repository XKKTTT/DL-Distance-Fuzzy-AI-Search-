# scripts/test_search.py
from src.search.search_engine import SearchEngine
from src.indexing.inverted_index import InvertedIndex

# Build a small in-memory index
index = InvertedIndex()
index.add_document("doc1", "The presldent will address the nati0n tomorrow.")
index.add_document("doc2", "Nation building is a collective effort.")

# Run search
engine = SearchEngine(index)
results = engine.search("president address the nation")

for doc_id, score, text in results:
    print(f"{doc_id} | score={score}\n{text}\n")
