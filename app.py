from flask import Flask, render_template_string

app = Flask(__name__)

NEWS_ITEMS = [
    {
        "headline": "Hugging Face Releases Major Transformers Update with Multi-Modal Agent Support",
        "source": "Hugging Face Blog",
        "url": "https://huggingface.co/blog",
    },
    {
        "headline": "Google DeepMind's Gemini 2.0 Sets New Benchmarks in Code Generation",
        "source": "Google DeepMind",
        "url": "https://deepmind.google/",
    },
    {
        "headline": "Anthropic Releases Claude 4 with Improved Safety Guardrails",
        "source": "Anthropic",
        "url": "https://anthropic.com/news",
    },
    {
        "headline": "Meta's Llama 4 Open-Source Model Outperforms Previous Closed-Source Rivals",
        "source": "Meta AI",
        "url": "https://ai.meta.com/blog/",
    },
    {
        "headline": "Microsoft Integrates AI Agents Deeply Into Office 365 Productivity Suite",
        "source": "Microsoft AI",
        "url": "https://blogs.microsoft.com/ai/",
    },
    {
        "headline": "Stanford HAI Report: AI Adoption in Enterprise Doubles Year-Over-Year",
        "source": "Stanford HAI",
        "url": "https://hai.stanford.edu/news",
    },
    {
        "headline": "EU AI Act Enforcement Begins: Companies Rush to Audit High-Risk Systems",
        "source": "MIT Technology Review",
        "url": "https://www.technologyreview.com/topic/artificial-intelligence/",
    },
    {
        "headline": "New Research Shows AI Can Design Novel Proteins for Drug Discovery",
        "source": "Nature",
        "url": "https://www.nature.com/subjects/machine-learning",
    },
]

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>AI News Feed</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #f0f4f8;
      color: #1a202c;
      min-height: 100vh;
      padding: 2rem 1rem;
    }

    header {
      max-width: 720px;
      margin: 0 auto 2rem;
    }

    header h1 {
      font-size: 2rem;
      font-weight: 700;
      color: #2d3748;
      letter-spacing: -0.02em;
    }

    header p {
      margin-top: 0.4rem;
      color: #718096;
      font-size: 0.95rem;
    }

    .feed {
      max-width: 720px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }

    .card {
      background: #fff;
      border-radius: 10px;
      padding: 1.25rem 1.5rem;
      box-shadow: 0 1px 4px rgba(0,0,0,0.08);
      transition: box-shadow 0.15s;
    }

    .card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.12); }

    .card a {
      text-decoration: none;
      color: inherit;
      display: block;
    }

    .headline {
      font-size: 1.05rem;
      font-weight: 600;
      line-height: 1.45;
      color: #2d3748;
    }

    .card:hover .headline { color: #3182ce; }

    .meta {
      margin-top: 0.5rem;
      font-size: 0.8rem;
      color: #a0aec0;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }

    .source-badge {
      background: #ebf8ff;
      color: #2b6cb0;
      padding: 0.15rem 0.5rem;
      border-radius: 4px;
      font-weight: 500;
    }

    footer {
      max-width: 720px;
      margin: 2rem auto 0;
      text-align: center;
      font-size: 0.78rem;
      color: #cbd5e0;
    }

    @media (max-width: 480px) {
      header h1 { font-size: 1.5rem; }
      .card { padding: 1rem 1.1rem; }
      .headline { font-size: 0.97rem; }
    }
  </style>
</head>
<body>
  <header>
    <h1>AI News Feed</h1>
    <p>Latest headlines from the world of artificial intelligence</p>
  </header>

  <main class="feed">
    {% for item in news %}
    <article class="card">
      <a href="{{ item.url }}" target="_blank" rel="noopener noreferrer">
        <div class="headline">{{ item.headline }}</div>
        <div class="meta">
          <span class="source-badge">{{ item.source }}</span>
          <span>&#8599; external link</span>
        </div>
      </a>
    </article>
    {% endfor %}
  </main>

  <footer>Updated {{ date }} &mdash; Powered by Elitez AI</footer>
</body>
</html>"""


@app.route("/")
def index():
    from datetime import date
    return render_template_string(HTML, news=NEWS_ITEMS, date=date.today().strftime("%B %d, %Y"))


@app.route("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
