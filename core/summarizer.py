"""
Extractive AI Text Summarizer
Uses Sentence Importance Scoring & Heap (Priority Queue) to extract key sentences.

DSA Concept:
- Min-Heap / Max-Heap (`heapq`) to retrieve Top-K highest ranked sentences in O(S log K)
  where S is total number of sentences.
- Hash Map frequency counting for token relevance in O(N).
"""

import re
import heapq
from collections import Counter

STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
    "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both",
    "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't",
    "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't",
    "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm",
    "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more",
    "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or",
    "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's",
    "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they",
    "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under",
    "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who",
    "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll",
    "you're", "you've", "your", "yours", "yourself", "yourselves"
}

class TextSummarizer:
    def __init__(self, stopwords: set[str] | None = None):
        self.stopwords = stopwords if stopwords is not None else STOPWORDS

    def _split_sentences(self, text: str) -> list[str]:
        """Split text into sentences cleanly using regex."""
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        return [s.strip() for s in sentences if len(s.strip()) > 5]

    def _tokenize(self, text: str) -> list[str]:
        """Extract lowercase alphabetic words."""
        return re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())

    def summarize(self, text: str, max_sentences: int = 3) -> dict:
        """
        Produce an extractive summary of the text.
        Returns a dict containing the summary text, compression ratio, and sentence scores.
        """
        sentences = self._split_sentences(text)
        if len(sentences) <= max_sentences:
            return {
                "summary": " ".join(sentences),
                "sentence_count": len(sentences),
                "original_sentence_count": len(sentences),
                "compression_ratio": "100%"
            }

        # Calculate word frequencies (Hash Map - O(N))
        words = [w for w in self._tokenize(text) if w not in self.stopwords]
        if not words:
            return {"summary": text[:200] + "...", "sentence_count": 1, "original_sentence_count": len(sentences), "compression_ratio": "N/A"}

        freq = Counter(words)
        max_freq = max(freq.values())
        # Normalize frequencies
        norm_freq = {word: count / max_freq for word, count in freq.items()}

        # Score each sentence based on normalized word frequencies + position bias
        sentence_scores = []
        for idx, sentence in enumerate(sentences):
            sent_words = [w for w in self._tokenize(sentence) if w not in self.stopwords]
            if not sent_words:
                continue

            base_score = sum(norm_freq.get(w, 0) for w in sent_words) / len(sent_words)
            # Position bias: First sentences and concluding sentences carry higher informational weight
            position_bias = 1.25 if (idx == 0 or idx == len(sentences) - 1) else 1.0
            total_score = base_score * position_bias
            sentence_scores.append((total_score, idx, sentence))

        # Use Heap (Priority Queue - O(S log K)) to get top-K sentences
        top_k = heapq.nlargest(max_sentences, sentence_scores, key=lambda x: x[0])
        # Sort back into chronological narrative order
        top_k.sort(key=lambda x: x[1])

        summary_text = " ".join([item[2] for item in top_k])
        compression = f"{(len(top_k) / len(sentences)) * 100:.1f}%"

        return {
            "summary": summary_text,
            "sentence_count": len(top_k),
            "original_sentence_count": len(sentences),
            "compression_ratio": compression,
            "top_sentences": [{"sentence": item[2], "score": round(item[0], 4)} for item in top_k]
        }
