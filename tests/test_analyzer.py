"""
Unit Tests for SmartInsight AI Engine
Tests cover:
- Trie insertion, exact search, and prefix matching
- Sentiment scoring, negation handling, and polarity bounds
- Extractive Summarizer sentence reduction and heap ranking
- Inverted Index TF-IDF scoring and retrieval
- Entity extraction & readability metrics
"""

import unittest
from core.trie import VocabularyTrie
from core.sentiment import SentimentEngine
from core.summarizer import TextSummarizer
from core.inverted_index import InvertedIndex
from core.analyzer import DocumentAnalyticsEngine

class TestSmartInsightAI(unittest.TestCase):

    def setUp(self):
        self.trie = VocabularyTrie()
        self.sentiment = SentimentEngine()
        self.summarizer = TextSummarizer()
        self.inv_index = InvertedIndex()
        self.engine = DocumentAnalyticsEngine()

    def test_trie_operations(self):
        words = ["algorithm", "algorithmic", "array", "ai", "artificial"]
        for w in words:
            self.trie.insert(w)

        self.assertTrue(self.trie.search("algorithm"))
        self.assertTrue(self.trie.search("array"))
        self.assertFalse(self.trie.search("unknown"))

        matches = self.trie.starts_with("al")
        self.assertEqual(sorted(matches), ["algorithm", "algorithmic"])

        a_matches = self.trie.starts_with("a")
        self.assertEqual(len(a_matches), 5)

    def test_sentiment_polarity_and_negation(self):
        pos = self.sentiment.analyze("The algorithm is extremely fast, reliable, and awesome!")
        self.assertEqual(pos["label"], "Positive")
        self.assertGreater(pos["polarity"], 0.3)

        neg = self.sentiment.analyze("The system is slow, buggy, and completely broken.")
        self.assertEqual(neg["label"], "Negative")
        self.assertLess(neg["polarity"], -0.3)

        negated = self.sentiment.analyze("The result is not good.")
        self.assertLessEqual(negated["polarity"], 0.0)

    def test_summarizer(self):
        sample_doc = (
            "Machine learning is revolutionizing automation across multiple industries. "
            "Engineers use specialized algorithms to minimize data processing latency. "
            "Data structures like hash maps provide constant time lookups. "
            "This makes large-scale data systems scalable and reliable. "
            "In summary, efficient code and smart models drive future technology."
        )
        res = self.summarizer.summarize(sample_doc, max_sentences=2)
        self.assertEqual(res["sentence_count"], 2)
        self.assertEqual(res["original_sentence_count"], 5)
        self.assertIn("summary", res)

    def test_inverted_index(self):
        self.inv_index.add_document("doc1", "Python and data structures are essential for software engineers.")
        self.inv_index.add_document("doc2", "Machine learning and artificial intelligence require data processing.")

        results = self.inv_index.search("software")
        self.assertTrue(len(results) >= 1)
        self.assertEqual(results[0]["doc_id"], "doc1")

    def test_document_analyzer_integration(self):
        text = "Contact support@example.com for refunds over $500. The engine is great with 99.9% uptime."
        res = self.engine.analyze_document(text)

        self.assertIn("support@example.com", res["entities"]["emails"])
        self.assertIn("99.9%", res["entities"]["percentages"])
        self.assertGreater(res["statistics"]["word_count"], 0)
        self.assertIn("flesch_reading_ease", res["readability"])

if __name__ == "__main__":
    unittest.main()
