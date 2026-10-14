# SmartInsight AI 🧠⚡
### Intelligent Document & Sentiment Analytics Engine Powered by Core DSA

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](#running-tests)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Zero External Dependencies](https://img.shields.io/badge/dependencies-standard--library-success.svg)](#installation)

**SmartInsight AI** is an intelligent, high-performance Natural Language Processing (NLP) and Document Analytics engine designed in Python. It bridges modern AI text processing with classical Data Structures and Algorithms (DSA), achieving fast execution without requiring heavy external dependencies.

---

## 🌟 Key Features

- **Extractive AI Summarization**: Uses sentence frequency scoring with **Priority Queues (Heaps)** to extract key summary sentences in $\mathcal{O}(S \log K)$.
- **Sentiment & Emotion Analysis**: Rule-based lexicon engine with negation handling, intensity dampeners/boosters, and subjectivity ratings.
- **Inverted Index Document Search**: Multi-document semantic keyword search with **TF-IDF relevance ranking** powered by hash map postings lists.
- **Prefix Autocomplete via Trie**: $\mathcal{O}(L)$ vocabulary indexing and prefix completion using a dedicated **Trie (Prefix Tree)**.
- **Readability & Complexity Index**: Flesch Reading Ease score, difficulty level classification, syllable estimation, and estimated reading time.
- **Named Entity & Pattern Extractor**: Automatic detection of emails, URLs, monetary amounts, and percentages.
- **Interactive CLI & JSON Reporting**: Terminal interface with formatted reporting and structured JSON export.

---

## 🏗️ Architecture & DSA Integration

```
Input Document / Query
        │
        ├───► Trie (Prefix Tree) ───────────────► O(L) Vocabulary Search & Autocomplete
        │
        ├───► Sentiment Engine ────────────────► Lexicon Polarity & Subjectivity Scoring
        │
        ├───► Text Summarizer (Heapq) ──────────► O(S log K) Top-Sentence Extraction
        │
        ├───► Inverted Index (Hash Map) ────────► TF-IDF Ranked Document Search
        │
        └───► Readability & Entity Extractor ───► Flesch Metric + Pattern Matching
```

| Component | Underlying Data Structure / Algorithm | Time Complexity | Purpose |
| :--- | :--- | :--- | :--- |
| **Vocabulary Index** | Trie (Prefix Tree) | $\mathcal{O}(L)$ | Prefix autocomplete & dictionary lookups |
| **Text Summarizer** | Min-Heap / Max-Heap (`heapq`) | $\mathcal{O}(S \log K)$ | Selecting Top-K salient sentences |
| **Document Search** | Inverted Index (Hash Map + Postings) | $\mathcal{O}(Q \cdot D)$ | Fast multi-file keyword retrieval |
| **Sentiment Analyzer** | Hash Table Lexicon & Sliding Lookback | $\mathcal{O}(N)$ | Real-time sentiment classification |

---

## 🚀 Quickstart & Installation

### 1. Prerequisites
- Python 3.10+ installed.

### 2. Clone the Repository
```bash
git clone https://github.com/pandeyshivam4737-a11y/ai-smart-analytics.git
cd ai-smart-analytics
```

*(No external dependencies needed for core execution!)*

---

## 💻 CLI Usage Examples

### 1. Run Complete Analysis on a File
```bash
python cli.py analyze --file samples/ai_research_overview.txt
```

### 2. Export Structured Report to JSON
```bash
python cli.py analyze --file samples/customer_reviews.txt --export report.json
```

### 3. Analyze Inline Text
```bash
python cli.py analyze --text "The new release is exceptionally fast, clean, and bug-free!"
```

### 4. Search Documents via Inverted Index
```bash
python cli.py search --dir samples --query "latency"
```

### 5. Autocomplete Vocabulary via Trie
```bash
python cli.py complete --prefix "in"
```

---

## 🧪 Running Tests

Execute the automated test suite:

```bash
python -m unittest discover -s tests
```

---

## 📁 Repository Structure

```text
ai-smart-analytics/
├── core/
│   ├── __init__.py           # Package exports
│   ├── analyzer.py           # Unified document analytics engine
│   ├── inverted_index.py     # TF-IDF inverted index search engine
│   ├── sentiment.py          # Lexicon sentiment & emotion classifier
│   ├── summarizer.py         # Priority Queue extractive summarizer
│   └── trie.py               # Trie data structure for prefix matching
├── samples/
│   ├── ai_research_overview.txt
│   └── customer_reviews.txt
├── tests/
│   └── test_analyzer.py      # Automated unit tests
├── cli.py                    # Command-line interface entrypoint
├── requirements.txt          # Optional dev packages
├── .gitignore
├── LICENSE                   # MIT License
└── README.md                 # Project documentation
```

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
