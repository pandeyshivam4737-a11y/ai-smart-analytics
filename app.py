"""
SmartInsight AI: Interactive Web Dashboard Server
Runs a zero-dependency web interface powered by Python's built-in http.server.
Usage:
  python app.py
  Then open: http://localhost:5000
"""

import sys
import os
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import webbrowser

# Add current dir to sys.path so core imports work cleanly
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from core.analyzer import DocumentAnalyticsEngine
from core.inverted_index import InvertedIndex

engine = DocumentAnalyticsEngine()
index = InvertedIndex()

# Index sample documents at startup
samples_dir = Path(__file__).parent / "samples"
if samples_dir.exists():
    for sample_file in samples_dir.glob("*.txt"):
        try:
            content = sample_file.read_text(encoding="utf-8")
            index.add_document(sample_file.name, content)
            # Also populate engine trie
            engine.analyze_document(content)
        except Exception:
            pass

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SmartInsight AI — NLP & Document Analytics</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #090d16;
      --card-bg: rgba(18, 26, 44, 0.75);
      --card-border: rgba(255, 255, 255, 0.08);
      --primary: #6366f1;
      --primary-light: #818cf8;
      --primary-glow: rgba(99, 102, 241, 0.25);
      --accent: #06b6d4;
      --success: #10b981;
      --warning: #f59e0b;
      --danger: #ef4444;
      --text: #f1f5f9;
      --text-muted: #94a3b8;
      --radius: 14px;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      background: var(--bg);
      background-image: 
        radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.12) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(6, 182, 212, 0.1) 0px, transparent 50%);
      color: var(--text);
      min-height: 100vh;
      line-height: 1.5;
    }
    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 32px 20px;
    }
    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 36px;
      padding-bottom: 24px;
      border-bottom: 1px solid var(--card-border);
    }
    .logo-group {
      display: flex;
      align-items: center;
      gap: 14px;
    }
    .logo-badge {
      background: linear-gradient(135deg, var(--primary), var(--accent));
      width: 44px;
      height: 44px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
      box-shadow: 0 8px 24px var(--primary-glow);
    }
    h1 {
      font-size: 24px;
      font-weight: 800;
      letter-spacing: -0.02em;
    }
    .subtitle {
      color: var(--text-muted);
      font-size: 13px;
    }
    .header-links a {
      color: var(--text-muted);
      text-decoration: none;
      font-size: 14px;
      font-weight: 500;
      padding: 8px 16px;
      border-radius: 8px;
      border: 1px solid var(--card-border);
      background: var(--card-bg);
      transition: all 0.2s;
    }
    .header-links a:hover {
      border-color: var(--primary);
      color: var(--text);
    }
    .grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
    }
    @media (max-width: 900px) {
      .grid { grid-template-columns: 1fr; }
    }
    .card {
      background: var(--card-bg);
      backdrop-filter: blur(16px);
      border: 1px solid var(--card-border);
      border-radius: var(--radius);
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }
    .card-title {
      font-size: 16px;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .dsa-tag {
      font-size: 11px;
      font-family: 'JetBrains Mono', monospace;
      padding: 3px 8px;
      border-radius: 6px;
      background: rgba(99, 102, 241, 0.15);
      color: var(--primary-light);
      border: 1px solid rgba(99, 102, 241, 0.3);
    }
    textarea {
      width: 100%;
      height: 220px;
      background: rgba(10, 14, 26, 0.8);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 14px;
      color: var(--text);
      font-family: inherit;
      font-size: 14px;
      resize: vertical;
      outline: none;
      transition: border-color 0.2s;
    }
    textarea:focus {
      border-color: var(--primary);
      box-shadow: 0 0 0 3px var(--primary-glow);
    }
    .btn-row {
      display: flex;
      gap: 12px;
      align-items: center;
      flex-wrap: wrap;
    }
    button {
      cursor: pointer;
      font-family: inherit;
      font-size: 14px;
      font-weight: 600;
      padding: 10px 20px;
      border-radius: 10px;
      border: none;
      transition: all 0.2s;
    }
    .btn-primary {
      background: linear-gradient(135deg, var(--primary), #4f46e5);
      color: #fff;
      box-shadow: 0 4px 14px var(--primary-glow);
    }
    .btn-primary:hover {
      transform: translateY(-1px);
      box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
    }
    .btn-secondary {
      background: rgba(255, 255, 255, 0.06);
      color: var(--text);
      border: 1px solid var(--card-border);
    }
    .btn-secondary:hover {
      background: rgba(255, 255, 255, 0.1);
    }
    .stat-cards {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
    }
    .stat-box {
      background: rgba(10, 14, 26, 0.6);
      border: 1px solid var(--card-border);
      padding: 12px;
      border-radius: 10px;
      text-align: center;
    }
    .stat-val {
      font-size: 20px;
      font-weight: 800;
      color: var(--accent);
      font-family: 'JetBrains Mono', monospace;
    }
    .stat-label {
      font-size: 11px;
      color: var(--text-muted);
      margin-top: 2px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .sentiment-banner {
      padding: 16px;
      border-radius: 10px;
      background: rgba(10, 14, 26, 0.7);
      border: 1px solid var(--card-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .badge {
      padding: 5px 12px;
      border-radius: 20px;
      font-weight: 700;
      font-size: 12px;
    }
    .badge-Positive { background: rgba(16, 185, 129, 0.2); color: var(--success); border: 1px solid var(--success); }
    .badge-Negative { background: rgba(239, 68, 68, 0.2); color: var(--danger); border: 1px solid var(--danger); }
    .badge-Neutral { background: rgba(148, 163, 184, 0.2); color: var(--text-muted); border: 1px solid var(--text-muted); }
    .summary-box {
      background: rgba(99, 102, 241, 0.06);
      border-left: 3px solid var(--primary);
      padding: 14px 16px;
      border-radius: 0 10px 10px 0;
      font-size: 14px;
      line-height: 1.6;
      color: #e2e8f0;
    }
    .pill-group {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
    .pill {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--card-border);
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 12px;
      font-family: 'JetBrains Mono', monospace;
    }
    .full-width {
      grid-column: 1 / -1;
    }
    .search-input-group {
      display: flex;
      gap: 10px;
    }
    .search-input-group input {
      flex: 1;
      background: rgba(10, 14, 26, 0.8);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 10px 14px;
      color: var(--text);
      font-family: inherit;
      outline: none;
    }
    .search-input-group input:focus {
      border-color: var(--accent);
    }
    .search-results {
      display: flex;
      flex-direction: column;
      gap: 10px;
      max-height: 200px;
      overflow-y: auto;
    }
    .result-item {
      padding: 12px;
      border-radius: 8px;
      background: rgba(10, 14, 26, 0.5);
      border: 1px solid var(--card-border);
    }
    .result-header {
      display: flex;
      justify-content: space-between;
      font-size: 13px;
      font-weight: 700;
      color: var(--accent);
      margin-bottom: 4px;
    }
    .result-preview {
      font-size: 12px;
      color: var(--text-muted);
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="logo-group">
        <div class="logo-badge">🧠</div>
        <div>
          <h1>SmartInsight AI</h1>
          <p class="subtitle">Intelligent NLP & Text Analytics Engine Powered by Core DSA</p>
        </div>
      </div>
      <div class="header-links">
        <a href="https://github.com/pandeyshivam4737-a11y/ai-smart-analytics" target="_blank">★ View on GitHub</a>
      </div>
    </header>

    <div class="grid">
      <!-- Input Panel -->
      <div class="card">
        <div class="card-title">
          <span>📝 Input Document / Text</span>
          <span class="dsa-tag">Raw String Stream</span>
        </div>
        <textarea id="inputText" placeholder="Paste or type any article, review, or paper here..."></textarea>
        <div class="btn-row">
          <button class="btn-primary" onclick="runAnalysis()">⚡ Analyze Document</button>
          <button class="btn-secondary" onclick="loadSample('ai')">📄 Sample AI Paper</button>
          <button class="btn-secondary" onclick="loadSample('review')">⭐ Sample Review</button>
        </div>
      </div>

      <!-- Live Analytics Dashboard -->
      <div class="card" id="resultsCard">
        <div class="card-title">
          <span>📊 Real-time AI Insights</span>
          <span class="dsa-tag" id="engineStatus">Ready</span>
        </div>

        <div class="stat-cards">
          <div class="stat-box">
            <div class="stat-val" id="statWords">0</div>
            <div class="stat-label">Words</div>
          </div>
          <div class="stat-box">
            <div class="stat-val" id="statReadability">0</div>
            <div class="stat-label">Reading Ease</div>
          </div>
          <div class="stat-box">
            <div class="stat-val" id="statTime">0s</div>
            <div class="stat-label">Read Time</div>
          </div>
        </div>

        <!-- Sentiment -->
        <div class="sentiment-banner">
          <div>
            <div style="font-size: 12px; color: var(--text-muted);">SENTIMENT POLARITY</div>
            <div style="font-size: 15px; font-weight: 700;" id="polarityVal">0.0 (Neutral)</div>
          </div>
          <span class="badge badge-Neutral" id="sentimentBadge">Neutral</span>
        </div>

        <!-- Summary -->
        <div>
          <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 6px; font-weight: 700;">
            EXTRACTIVE SUMMARY <span class="dsa-tag" style="margin-left: 6px;">Heapq O(S log K)</span>
          </div>
          <div class="summary-box" id="summaryText">Run analysis to generate an extractive AI summary...</div>
        </div>

        <!-- Keywords -->
        <div>
          <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 6px; font-weight: 700;">
            TOP KEYWORDS <span class="dsa-tag" style="margin-left: 6px;">Hash Counter O(N)</span>
          </div>
          <div class="pill-group" id="keywordsPill">
            <span class="pill">None</span>
          </div>
        </div>
      </div>

      <!-- Inverted Index Search & Trie Autocomplete Section -->
      <div class="card full-width">
        <div class="card-title">
          <span>🔍 Inverted Index Semantic Search & Trie Autocomplete</span>
          <span class="dsa-tag">Trie O(L) & TF-IDF Postings</span>
        </div>
        <div class="search-input-group">
          <input type="text" id="searchQuery" placeholder="Search across documents (e.g. 'latency', 'models', 'support')..." onkeyup="handleAutocomplete(this.value)">
          <button class="btn-primary" onclick="runSearch()">Search</button>
        </div>
        <div style="font-size: 12px; color: var(--text-muted);">
          Prefix Autocomplete (Trie): <span id="trieMatches" style="color: var(--accent); font-family: 'JetBrains Mono', monospace;">type 2+ letters...</span>
        </div>
        <div class="search-results" id="searchResults">
          <!-- Dynamic results -->
        </div>
      </div>
    </div>
  </div>

  <script>
    const sampleAI = `Artificial Intelligence and Machine Learning are transforming modern data processing pipelines at unprecedented speed. Large Language Models (LLMs) allow organizations to extract actionable insights from unstructured textual data with high accuracy. However, efficient deployment requires optimized algorithms and minimal latency. By leveraging specialized data structures such as Inverted Indexes and Priority Queues, software engineers can achieve sub-millisecond retrieval times even over millions of documents. Furthermore, combining rule-based heuristics with deep learning architectures delivers reliable, explainable results for mission-critical enterprise systems. In conclusion, mastering computational efficiency alongside AI models is the hallmark of modern software craftsmanship.`;

    const sampleReview = `The new cloud AI analytics engine is absolutely fantastic! The query response time is super fast and cut our data ingestion lag by 45%. The customer support team reached out to support@cloudai.io and resolved our billing inquiry of $1,250 within ten minutes. Overall, this is the most reliable and powerful platform we have used this year.`;

    function loadSample(type) {
      document.getElementById('inputText').value = (type === 'ai') ? sampleAI : sampleReview;
      runAnalysis();
    }

    async function runAnalysis() {
      const text = document.getElementById('inputText').value.trim();
      if (!text) {
        alert("Please enter or select some text to analyze.");
        return;
      }
      document.getElementById('engineStatus').innerText = "Processing...";

      try {
        const res = await fetch('/api/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: text })
        });
        const data = await res.json();

        // Populate Stats
        document.getElementById('statWords').innerText = data.statistics.word_count;
        document.getElementById('statReadability').innerText = data.readability.flesch_reading_ease;
        document.getElementById('statTime').innerText = data.statistics.estimated_read_time_seconds + 's';

        // Sentiment
        const sent = data.sentiment;
        document.getElementById('polarityVal').innerText = `${sent.polarity} (${sent.label})`;
        const badge = document.getElementById('sentimentBadge');
        badge.className = `badge badge-${sent.label}`;
        badge.innerText = `${sent.label} (${Math.round(sent.confidence * 100)}%)`;

        // Summary
        document.getElementById('summaryText').innerText = `"${data.summary.summary}"`;

        // Keywords
        const pillsContainer = document.getElementById('keywordsPill');
        pillsContainer.innerHTML = '';
        data.top_keywords.forEach(k => {
          const span = document.createElement('span');
          span.className = 'pill';
          span.innerText = `${k.keyword} (${k.frequency})`;
          pillsContainer.appendChild(span);
        });

        document.getElementById('engineStatus').innerText = "Active";
      } catch (err) {
        document.getElementById('engineStatus').innerText = "Error";
        console.error(err);
      }
    }

    async function handleAutocomplete(val) {
      val = val.trim();
      if (val.length < 2) {
        document.getElementById('trieMatches').innerText = 'type 2+ letters...';
        return;
      }
      try {
        const res = await fetch(`/api/complete?prefix=${encodeURIComponent(val)}`);
        const matches = await res.json();
        document.getElementById('trieMatches').innerText = matches.length > 0 ? matches.slice(0, 7).join(', ') : 'no matches';
      } catch (e) {}
    }

    async function runSearch() {
      const q = document.getElementById('searchQuery').value.trim();
      if (!q) return;
      try {
        const res = await fetch('/api/search', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: q })
        });
        const hits = await res.json();
        const container = document.getElementById('searchResults');
        container.innerHTML = '';

        if (hits.length === 0) {
          container.innerHTML = '<div class="result-item"><div class="result-preview">No matching documents found.</div></div>';
          return;
        }

        hits.forEach(hit => {
          const div = document.createElement('div');
          div.className = 'result-item';
          div.innerHTML = `
            <div class="result-header">
              <span>📄 ${hit.doc_id}</span>
              <span>Relevance Score: ${hit.relevance_score}</span>
            </div>
            <div class="result-preview">"${hit.preview}"</div>
          `;
          container.appendChild(div);
        });
      } catch (e) {
        console.error(e);
      }
    }

    // Auto-load default sample on start
    window.onload = () => loadSample('ai');
  </script>
</body>
</html>
"""

class SmartInsightHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))

        elif parsed.path == "/api/complete":
            query_params = urllib.parse.parse_qs(parsed.query)
            prefix = query_params.get("prefix", [""])[0]
            matches = engine.trie.starts_with(prefix)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(matches).encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")

        if parsed.path == "/api/analyze":
            data = json.loads(body) if body else {}
            text = data.get("text", "")
            results = engine.analyze_document(text)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(results).encode("utf-8"))

        elif parsed.path == "/api/search":
            data = json.loads(body) if body else {}
            query = data.get("query", "")
            hits = index.search(query)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(hits).encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=5000):
    server = HTTPServer(("127.0.0.1", port), SmartInsightHandler)
    print("\n" + "=" * 60)
    print(f"🚀 SmartInsight AI Web Dashboard is running!")
    print(f"👉 Local URL: http://127.0.0.1:{port}")
    print("=" * 60 + "\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        server.server_close()

if __name__ == "__main__":
    run_server(5000)
