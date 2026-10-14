"""
SmartInsight AI: Interactive Command Line Interface (CLI)
Usage:
  python cli.py analyze --file samples/ai_research_overview.txt
  python cli.py sentiment --text "This system is incredibly fast and reliable!"
  python cli.py search --dir samples --query "latency"
  python cli.py interactive
"""

import sys
import os
import json
import argparse
from pathlib import Path
from core.analyzer import DocumentAnalyticsEngine
from core.inverted_index import InvertedIndex

def format_header(title: str) -> None:
    print("\n" + "=" * 65)
    print(f"  {title.upper()}")
    print("=" * 65)

def print_analysis(results: dict) -> None:
    stats = results["statistics"]
    read = results["readability"]
    sentiment = results["sentiment"]
    summary = results["summary"]
    entities = results["entities"]
    keywords = results["top_keywords"]

    format_header("Document Statistics")
    print(f"Total Words:             {stats['word_count']}")
    print(f"Unique Words:            {stats['unique_words']}")
    print(f"Total Sentences:         {stats['sentence_count']}")
    print(f"Vocabulary Diversity:    {stats['vocabulary_diversity_ttr']}")
    print(f"Est. Reading Time:       ~{stats['estimated_read_time_seconds']} seconds")

    format_header("Readability Assessment")
    print(f"Flesch Reading Ease:     {read['flesch_reading_ease']} / 100")
    print(f"Target Level:            {read['difficulty_level']}")

    format_header("AI Sentiment & Emotion Analysis")
    print(f"Sentiment Polarity:      {sentiment['polarity']} (Score: -1.0 to +1.0)")
    print(f"Classification:          {sentiment['label']}")
    print(f"Subjectivity:            {sentiment['subjectivity']} (0.0=Objective, 1.0=Subjective)")
    if sentiment["positive_matches"]:
        print(f"Positive Triggers:       {', '.join(sentiment['positive_matches'])}")
    if sentiment["negative_matches"]:
        print(f"Negative Triggers:       {', '.join(sentiment['negative_matches'])}")

    format_header("Key Extracted Entities")
    for key, values in entities.items():
        if values:
            print(f"{key.replace('_', ' ').capitalize()}: {', '.join(values)}")

    format_header("Top Keywords (Frequency)")
    kw_str = ", ".join([f"{item['keyword']} ({item['frequency']})" for item in keywords])
    print(kw_str if kw_str else "None")

    format_header("Extractive AI Summary")
    print(f"Original Sentences: {summary['original_sentence_count']} -> Summary Sentences: {summary['sentence_count']}")
    print(f"Compression:        {summary['compression_ratio']}\n")
    print(f"\"{summary['summary']}\"")
    print("=" * 65 + "\n")

def main():
    parser = argparse.ArgumentParser(description="SmartInsight AI: NLP & Document Analytics Engine")
    subparsers = parser.add_subparsers(dest="command")

    # Analyze file or text
    analyze_parser = subparsers.add_parser("analyze", help="Analyze document or text")
    analyze_parser.add_argument("--file", "-f", type=str, help="Path to text file")
    analyze_parser.add_argument("--text", "-t", type=str, help="Raw text string to analyze")
    analyze_parser.add_argument("--export", "-e", type=str, help="Export JSON report to output file")

    # Search documents
    search_parser = subparsers.add_parser("search", help="Search text files using Inverted Index")
    search_parser.add_argument("--dir", "-d", type=str, default="samples", help="Directory containing text files")
    search_parser.add_argument("--query", "-q", type=str, required=True, help="Search query")

    # Autocomplete using Trie
    trie_parser = subparsers.add_parser("complete", help="Autocomplete prefix using Trie")
    trie_parser.add_argument("--prefix", "-p", type=str, required=True, help="Prefix to search")

    args = parser.parse_args()

    engine = DocumentAnalyticsEngine()

    if args.command == "analyze":
        if args.file:
            path = Path(args.file)
            if not path.exists():
                print(f"Error: File not found at '{args.file}'")
                sys.exit(1)
            content = path.read_text(encoding="utf-8")
        elif args.text:
            content = args.text
        else:
            print("Error: Specify either --file or --text")
            sys.exit(1)

        results = engine.analyze_document(content)
        print_analysis(results)

        if args.export:
            with open(args.export, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2)
            print(f"Analysis saved to: {args.export}")

    elif args.command == "search":
        search_dir = Path(args.dir)
        if not search_dir.exists():
            print(f"Error: Directory '{args.dir}' does not exist")
            sys.exit(1)

        inv_index = InvertedIndex()
        file_count = 0
        for txt_file in search_dir.glob("*.txt"):
            inv_index.add_document(txt_file.name, txt_file.read_text(encoding="utf-8"))
            file_count += 1

        print(f"Indexed {file_count} documents from '{args.dir}'.")
        hits = inv_index.search(args.query)

        format_header(f"Search Results for '{args.query}'")
        if not hits:
            print("No matching documents found.")
        else:
            for i, hit in enumerate(hits, 1):
                print(f"[{i}] {hit['doc_id']}  (Score: {hit['relevance_score']})")
                print(f"    Preview: \"{hit['preview']}\"\n")

    elif args.command == "complete":
        # Load sample files to populate Trie
        samples_dir = Path("samples")
        if samples_dir.exists():
            for f in samples_dir.glob("*.txt"):
                engine.analyze_document(f.read_text(encoding="utf-8"))

        matches = engine.trie.starts_with(args.prefix)
        print(f"\nVocabulary matches for prefix '{args.prefix}':")
        print(matches if matches else "No matching words found.")

    else:
        # Default run demo on sample file
        sample_path = Path("samples/ai_research_overview.txt")
        if sample_path.exists():
            print("\n[Running default demo on 'samples/ai_research_overview.txt']\n")
            results = engine.analyze_document(sample_path.read_text(encoding="utf-8"))
            print_analysis(results)
        else:
            parser.print_help()

if __name__ == "__main__":
    main()
