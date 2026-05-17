from flask import Flask, render_template_string

app = Flask(__name__)

NEWS_ITEMS = [
    {
        "headline": "Hugging Face Releases Major Transformers Update with Multi-Modal Agent Support",
        "source": "Hugging Face Blog",
        "source_initial": "HF",
        "source_color": "#FF9D00",
        "url": "https://huggingface.co/blog",
        "snippet": "The latest Transformers library update brings native multi-modal agent pipelines, improved quantization, and expanded model hub integrations for production deployments.",
        "timestamp": "2 hours ago",
    },
    {
        "headline": "Google DeepMind's Gemini 2.0 Sets New Benchmarks in Code Generation",
        "source": "Google DeepMind",
        "source_initial": "GD",
        "source_color": "#4285F4",
        "url": "https://deepmind.google/",
        "snippet": "Gemini 2.0 outperforms GPT-4 on HumanEval and MBPP benchmarks, with particular strength in multi-step reasoning and repository-level code understanding tasks.",
        "timestamp": "4 hours ago",
    },
    {
        "headline": "Anthropic Releases Claude 4 with Improved Safety Guardrails and Extended Context",
        "source": "Anthropic",
        "source_initial": "AN",
        "source_color": "#C97E4D",
        "url": "https://anthropic.com/news",
        "snippet": "Claude 4 introduces a 500K token context window and significantly enhanced Constitutional AI techniques, reducing harmful output rates by 40% compared to Claude 3.",
        "timestamp": "6 hours ago",
    },
    {
        "headline": "Meta's Llama 4 Open-Source Model Outperforms Previous Closed-Source Rivals",
        "source": "Meta AI",
        "source_initial": "MT",
        "source_color": "#0866FF",
        "url": "https://ai.meta.com/blog/",
        "snippet": "Meta's Llama 4 70B model achieves state-of-the-art performance on MMLU and HellaSwag, available under a permissive commercial license for businesses with under 700M users.",
        "timestamp": "8 hours ago",
    },
    {
        "headline": "Microsoft Integrates AI Agents Deeply Into Office 365 Productivity Suite",
        "source": "Microsoft AI",
        "source_initial": "MS",
        "source_color": "#00A4EF",
        "url": "https://blogs.microsoft.com/ai/",
        "snippet": "Copilot agents can now autonomously draft, schedule, and follow up on emails, analyze spreadsheets, and generate presentation slides with minimal human input.",
        "timestamp": "10 hours ago",
    },
    {
        "headline": "Stanford HAI Report: AI Adoption in Enterprise Doubles Year-Over-Year",
        "source": "Stanford HAI",
        "source_initial": "SH",
        "source_color": "#8C1515",
        "url": "https://hai.stanford.edu/news",
        "snippet": "The 2026 AI Index shows enterprise AI adoption reached 78% of Fortune 500 companies, with natural language processing and computer vision leading deployment categories.",
        "timestamp": "1 day ago",
    },
    {
        "headline": "EU AI Act Enforcement Begins: Companies Rush to Audit High-Risk Systems",
        "source": "MIT Technology Review",
        "source_initial": "TR",
        "source_color": "#A31F34",
        "url": "https://www.technologyreview.com/topic/artificial-intelligence/",
        "snippet": "With the EU AI Act now in effect, compliance teams are scrambling to classify their systems, conduct mandatory conformity assessments, and register high-risk AI deployments.",
        "timestamp": "1 day ago",
    },
    {
        "headline": "New Research Shows AI Can Design Novel Proteins for Drug Discovery at Scale",
        "source": "Nature",
        "source_initial": "NT",
        "source_color": "#1A73E8",
        "url": "https://www.nature.com/subjects/machine-learning",
        "snippet": "AlphaFold-derived protein design tools have enabled researchers to generate and wet-lab validate 150+ novel enzymes targeting antibiotic-resistant bacteria in a single study.",
        "timestamp": "2 days ago",
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
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: #F4F6F9;
      color: #1A202C;
      min-height: 100vh;
    }

    .page-header {
      background: #fff;
      border-bottom: 1px solid #E2E8F0;
      padding: 1.25rem 1.5rem;
      position: sticky;
      top: 0;
      z-index: 10;
    }

    .page-header-inner {
      max-width: 760px;
      margin: 0 auto;
    }

    .page-header h1 {
      font-size: 1.5rem;
      font-weight: 700;
      color: #0F172A;
      letter-spacing: -0.02em;
    }

    .page-header .tagline {
      font-size: 0.8rem;
      color: #94A3B8;
      margin-top: 0.2rem;
    }

    .feed {
      max-width: 760px;
      margin: 1.5rem auto;
      padding: 0 1rem 2rem;
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
    }

    .card {
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 12px rgba(0,0,0,0.04);
      border-left: 4px solid var(--accent);
      overflow: hidden;
      transition: box-shadow 0.18s ease, transform 0.18s ease;
    }

    .card:hover {
      box-shadow: 0 4px 16px rgba(0,0,0,0.12), 0 1px 3px rgba(0,0,0,0.06);
      transform: translateY(-1px);
    }

    .card-link {
      display: block;
      padding: 1rem 1.25rem;
      text-decoration: none;
      color: inherit;
    }

    .card-top {
      display: flex;
      align-items: flex-start;
      gap: 0.875rem;
    }

    .source-avatar {
      flex-shrink: 0;
      width: 42px;
      height: 42px;
      border-radius: 10px;
      background: var(--accent);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.72rem;
      font-weight: 700;
      color: #fff;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }

    .card-meta-wrap {
      flex: 1;
      min-width: 0;
    }

    .card-meta-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.5rem;
      margin-bottom: 0.3rem;
    }

    .source-name {
      font-size: 0.72rem;
      font-weight: 600;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.06em;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .timestamp {
      font-size: 0.72rem;
      color: #94A3B8;
      white-space: nowrap;
      flex-shrink: 0;
    }

    .headline {
      font-size: 0.975rem;
      font-weight: 600;
      line-height: 1.45;
      color: #0F172A;
      margin-bottom: 0.4rem;
    }

    .card:hover .headline {
      color: var(--accent);
    }

    .snippet {
      font-size: 0.83rem;
      color: #64748B;
      line-height: 1.55;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    .card-footer {
      display: flex;
      align-items: center;
      justify-content: flex-end;
      padding: 0 1.25rem 0.75rem;
    }

    .ext-link-label {
      font-size: 0.7rem;
      color: #94A3B8;
      display: flex;
      align-items: center;
      gap: 0.25rem;
    }

    .ext-link-label svg {
      width: 10px;
      height: 10px;
      fill: none;
      stroke: currentColor;
      stroke-width: 2;
      stroke-linecap: round;
      stroke-linejoin: round;
    }

    @media (max-width: 480px) {
      .page-header { padding: 1rem; }
      .page-header h1 { font-size: 1.25rem; }
      .feed { margin: 1rem auto; padding: 0 0.75rem 1.5rem; gap: 0.625rem; }
      .card-link { padding: 0.875rem 1rem; }
      .card-footer { padding: 0 1rem 0.625rem; }
      .source-avatar { width: 36px; height: 36px; font-size: 0.65rem; border-radius: 8px; }
      .headline { font-size: 0.9rem; }
      .snippet { font-size: 0.8rem; }
    }
  </style>
</head>
<body>
  <header class="page-header">
    <div class="page-header-inner">
      <h1>AI News</h1>
      <p class="tagline">Latest headlines from the world of artificial intelligence</p>
    </div>
  </header>

  <main class="feed">
    {% for item in news %}
    <article class="card" style="--accent: {{ item.source_color }}">
      <a class="card-link" href="{{ item.url }}" target="_blank" rel="noopener noreferrer">
        <div class="card-top">
          <div class="source-avatar">{{ item.source_initial }}</div>
          <div class="card-meta-wrap">
            <div class="card-meta-row">
              <span class="source-name">{{ item.source }}</span>
              <span class="timestamp">{{ item.timestamp }}</span>
            </div>
            <div class="headline">{{ item.headline }}</div>
            <div class="snippet">{{ item.snippet }}</div>
          </div>
        </div>
      </a>
      <div class="card-footer">
        <span class="ext-link-label">
          <svg viewBox="0 0 24 24"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
          opens in new tab
        </span>
      </div>
    </article>
    {% endfor %}
  </main>
</body>
</html>"""


@app.route("/")
def index():
    return render_template_string(HTML, news=NEWS_ITEMS)


@app.route("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
