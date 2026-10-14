"""
SmartInsight AI: Main Document & Text Analytics Engine
Integrates:
- Statistical linguistics (reading ease, grade levels, reading time)
- Named Entity & Pattern Recognition
- Rule-based Sentiment & Emotion Analysis
- Extractive Summarization via Priority Queues
- Vocabulary Trie Indexing
"""

import re
import math
from collections import Counter
from core.sentiment import SentimentEngine
from core.summarizer import TextSummarizer, STOPWORDS
from core.trie import VocabularyTrie

class DocumentAnalyticsEngine:
    def __init__(self):
        self.sentiment_engine = SentimentEngine()
        self.summarizer = TextSummarizer()
        self.trie = VocabularyTrie()

    def _count_syllables(self, word: str) -> int:
        """Estimate syllable count in an English word."""
        word = word.lower()
        if len(word) <= 3:
            return 1
        count = len(re.findall(r"[aeiouy]+", word))
        if word.endswith("e") and not word.endswith("le") and count > 1:
            count -= 1
        return max(1, count)

    def extract_entities(self, text: str) -> dict:
        """Extract structured entities (emails, urls, monetary amounts, metrics)."""
        emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
        urls = re.findall(r"https?://[^\s]+", text)
        currencies = re.findall(r"[\$€£¥]\s*\d+(?:,\d{3})*(?:\.\d+)?|\b\d+(?:,\d{3})*(?:\.\d+)?\s*(?:USD|EUR|GBP|INR)\b", text)
        percentages = re.findall(r"\b\d+(?:\.\d+)?%", text)

        return {
            "emails": list(set(emails)),
            "urls": list(set(urls)),
            "financial_figures": list(set(currencies)),
            "percentages": list(set(percentages))
        }

    def analyze_document(self, text: str, summary_sentences: int = 3, top_k_keywords: int = 8) -> dict:
        """
        Perform complete multi-faceted AI analysis on the document.
        """
        words = re.findall(r"\b[a-zA-Z0-9']+\b", text)
        clean_words = [w.lower() for w in words if w.isalpha()]
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        sentences = [s.strip() for s in sentences if len(s.strip()) > 3]

        total_words = len(clean_words)
        total_sentences = max(len(sentences), 1)

        # Build Trie & count non-stopword frequencies
        content_words = []
        for word in clean_words:
            self.trie.insert(word)
            if word not in STOPWORDS and len(word) > 2:
                content_words.append(word)

        word_freq = Counter(content_words)
        top_keywords = word_freq.most_common(top_k_keywords)

        # Lexical Readability Metrics (Flesch Reading Ease & ARI)
        total_syllables = sum(self._count_syllables(w) for w in clean_words) if clean_words else 1
        asl = total_words / total_sentences  # Average Sentence Length
        asw = total_syllables / max(total_words, 1)  # Average Syllables per Word

        # Flesch Reading Ease: 206.835 - 1.015(ASL) - 84.6(ASW)
        flesch_score = 206.835 - (1.015 * asl) - (84.6 * asw)
        flesch_score = round(max(0.0, min(100.0, flesch_score)), 1)

        if flesch_score >= 80:
            reading_difficulty = "Easy (Elementary / General Audience)"
        elif flesch_score >= 60:
            reading_difficulty = "Standard (High School / Conversational)"
        elif flesch_score >= 30:
            reading_difficulty = "Challenging (College / Professional)"
        else:
            reading_difficulty = "Academic / Very Technical"

        # Reading Time (assuming average 220 words per minute)
        estimated_read_seconds = math.ceil((total_words / 220) * 60)

        # Type-Token Ratio (Vocabulary Diversity)
        unique_words = len(set(clean_words))
        diversity_ratio = round(unique_words / max(total_words, 1), 3)

        # Sentiment Analysis
        sentiment = self.sentiment_engine.analyze(text)

        # Summarization
        summary_res = self.summarizer.summarize(text, max_sentences=summary_sentences)

        # Entities
        entities = self.extract_entities(text)

        return {
            "statistics": {
                "word_count": total_words,
                "unique_words": unique_words,
                "sentence_count": total_sentences,
                "vocabulary_diversity_ttr": diversity_ratio,
                "estimated_read_time_seconds": estimated_read_seconds
            },
            "readability": {
                "flesch_reading_ease": flesch_score,
                "difficulty_level": reading_difficulty
            },
            "sentiment": sentiment,
            "top_keywords": [{"keyword": k, "frequency": count} for k, count in top_keywords],
            "entities": entities,
            "summary": summary_res
        }
