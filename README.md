# An experimental Fuzzy + Semantic AI Search Engine

A hybrid search engine that can **find relevant results in noisy datasets** using:
- **Fuzzy matching** (Damerau–Levenshtein ≤ 1) for typo tolerance  
- **Semantic similarity** (Sentence-BERT) for meaning-based matches  

Built with a **custom Z-Algorithm-based matcher** for speed and an **inverted index** for efficient lookups.

---

## Features

**Fuzzy search** — matches terms even with typos, swaps, insertions, or deletions  
**Semantic search** — finds results by meaning, not just keywords  
**Hybrid ranking** — combine fuzzy + semantic scores with adjustable weights  
**Fast indexing** — inverted index stores token → document mapping  


---

## Example Usage

```python
from src.indexing.inverted_index import InvertedIndex
from src.search.search_engine import SearchEngine

# 1. Create and populate index
index = InvertedIndex()
index.add_document("doc1", "The presldent will address the nati0n tomorrow.")
index.add_document("doc2", "Nation building is a collective effort.")

# 2. Create search engine (fuzzy only)
engine = SearchEngine(index)

# 3. Run search
results = engine.search("nation")
for doc_id, score, text in results:
    print(f"{doc_id} (score={score}): {text}")
