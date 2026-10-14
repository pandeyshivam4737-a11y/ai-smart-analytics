"""
Inverted Index & Document Search Engine
DSA Concept:
- Inverted Index maps each unique term to a posting list of documents containing it.
- Time Complexity for Query: O(Q * D) where Q is query terms, D is document matches (much faster than scanning all files O(Total Words)).
- TF-IDF Relevance Ranking.
"""

import math
import re
from collections import defaultdict
from core.summarizer import STOPWORDS

class InvertedIndex:
    def __init__(self):
        # term -> {doc_id: term_frequency}
        self.index: dict[str, dict[str, int]] = defaultdict(dict)
        self.doc_lengths: dict[str, int] = {}
        self.documents: dict[str, str] = {}
        self.doc_count = 0

    def _tokenize(self, text: str) -> list[str]:
        words = re.findall(r"\b[a-zA-Z]{2,}\b", text.lower())
        return [w for w in words if w not in STOPWORDS]

    def add_document(self, doc_id: str, content: str) -> None:
        """Index a document into the inverted index."""
        tokens = self._tokenize(content)
        self.doc_lengths[doc_id] = len(tokens)
        self.documents[doc_id] = content
        self.doc_count += 1

        for token in tokens:
            self.index[token][doc_id] = self.index[token].get(doc_id, 0) + 1

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """
        Search indexed documents using TF-IDF ranking.
        Returns top-k most relevant documents.
        """
        query_tokens = self._tokenize(query)
        if not query_tokens or self.doc_count == 0:
            return []

        doc_scores = defaultdict(float)

        for term in query_tokens:
            if term not in self.index:
                continue

            postings = self.index[term]
            df = len(postings)
            # Inverse Document Frequency (IDF)
            idf = math.log((self.doc_count + 1) / (df + 1)) + 1.0

            for doc_id, tf in postings.items():
                doc_len = max(self.doc_lengths.get(doc_id, 1), 1)
                # Term Frequency (TF) normalized
                norm_tf = tf / doc_len
                doc_scores[doc_id] += norm_tf * idf

        if not doc_scores:
            return []

        # Sort documents by score descending
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

        results = []
        for doc_id, score in ranked:
            preview = self.documents[doc_id][:150].strip() + ("..." if len(self.documents[doc_id]) > 150 else "")
            results.append({
                "doc_id": doc_id,
                "relevance_score": round(score, 4),
                "preview": preview
            })

        return results
