from src.indexing.inverted_index import InvertedIndex
from src.search.search_engine import SearchEngine

index = InvertedIndex()
index.add_document("doc1", "The presldent will address the nati0n tomorrow.")
index.add_document("doc2", "Nation building is a collective effort.")

engine = SearchEngine(index)
results = engine.search("building")
print(results)


# for doc_id, score, text in results:
    # print(doc_id, score, text)
