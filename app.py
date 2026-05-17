from flask import Flask, render_template_string

app = Flask(__name__)

# Source logo SVGs — brand-representative marks (not generic 2-letter squares)
SOURCE_LOGOS = {
    "Hugging Face Blog": """<svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="20" cy="20" r="20" fill="#FF9D00"/>
      <ellipse cx="14.5" cy="18" rx="3" ry="4" fill="#fff"/>
      <ellipse cx="25.5" cy="18" rx="3" ry="4" fill="#fff"/>
      <ellipse cx="14.5" cy="18.5" rx="1.5" ry="2" fill="#2d1b00"/>
      <ellipse cx="25.5" cy="18.5" rx="1.5" ry="2" fill="#2d1b00"/>
      <path d="M13 26 Q20 31 27 26" stroke="#2d1b00" stroke-width="1.8" stroke-linecap="round" fill="none"/>
      <path d="M10 13 C10 10 13 8 14 11" stroke="#2d1b00" stroke-width="1.5" stroke-linecap="round" fill="none"/>
      <path d="M30 13 C30 10 27 8 26 11" stroke="#2d1b00" stroke-width="1.5" stroke-linecap="round" fill="none"/>
    </svg>""",

    "Google DeepMind": """<svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="20" cy="20" r="20" fill="#fff"/>
      <circle cx="20" cy="20" r="20" fill="url(#gd_grad)"/>
      <defs><linearGradient id="gd_grad" x1="0" y1="0" x2="40" y2="40" gradientUnits="userSpaceOnUse">
        <stop stop-color="#4285F4"/><stop offset="0.33" stop-color="#34A853"/><stop offset="0.66" stop-color="#FBBC05"/><stop offset="1" stop-color="#EA4335"/>
      </linearGradient></defs>
      <text x="20" y="26" text-anchor="middle" font-family="Arial,sans-serif" font-weight="700" font-size="18" fill="#fff">G</text>
    </svg>""",

    "Anthropic": """<svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="20" cy="20" r="20" fill="#C97E4D"/>
      <path d="M14 28 L20 12 L26 28" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
      <path d="M16.5 23 L23.5 23" stroke="#fff" stroke-width="2" stroke-linecap="round"/>
    </svg>""",

    "Meta AI": """<svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="20" cy="20" r="20" fill="#0866FF"/>
      <path d="M10 20 C10 15.5 12.5 13 15 13 C17 13 18.5 14.5 20 17 C21.5 14.5 23 13 25 13 C27.5 13 30 15.5 30 20 C30 24.5 27.5 27 25 27 C23 27 21.5 25.5 20 23 C18.5 25.5 17 27 15 27 C12.5 27 10 24.5 10 20Z" stroke="#fff" stroke-width="2" fill="none"/>
    </svg>""",

    "Microsoft AI": """<svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="20" cy="20" r="20" fill="#00A4EF"/>
      <rect x="11" y="11" width="8" height="8" rx="1" fill="#F25022"/>
      <rect x="21" y="11" width="8" height="8" rx="1" fill="#7FBA00"/>
      <rect x="11" y="21" width="8" height="8" rx="1" fill="#00A4EF"/>
      <rect x="21" y="21" width="8" height="8" rx="1" fill="#FFB900"/>
    </svg>""",

    "Stanford HAI": """<svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="20" cy="20" r="20" fill="#8C1515"/>
      <text x="20" y="26" text-anchor="middle" font-family="Georgia,serif" font-weight="700" font-size="18" fill="#fff">S</text>
    </svg>""",

    "MIT Technology Review": """<svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="20" cy="20" r="20" fill="#A31F34"/>
      <text x="20" y="24" text-anchor="middle" font-family="Arial,sans-serif" font-weight="700" font-size="10" letter-spacing="0.5" fill="#fff">MIT</text>
    </svg>""",

    "Nature": """<svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="20" cy="20" r="20" fill="#1A6E3C"/>
      <path d="M20 30 L20 18" stroke="#fff" stroke-width="2" stroke-linecap="round"/>
      <path d="M20 22 C20 22 14 19 13 13 C13 13 20 14 20 22Z" fill="#fff"/>
      <path d="M20 18 C20 18 26 15 27 9 C27 9 20 10 20 18Z" fill="#b8e6c8"/>
    </svg>""",
}

NEWS_ITEMS = [
    {
        "headline": "Hugging Face Releases Major Transformers Update with Multi-Modal Agent Support",
        "source": "Hugging Face Blog",
        "source_color": "#FF9D00",
        "url": "https://huggingface.co/blog",
        "snippet": "The latest Transformers library update brings native multi-modal agent pipelines, improved quantization, and expanded model hub integrations for production deployments.",
        "timestamp": "2 hours ago",
        "category": "Open Source",
        "category_color": "#FF9D00",
    },
    {
        "headline": "Google DeepMind's Gemini 2.0 Sets New Benchmarks in Code Generation",
        "source": "Google DeepMind",
        "source_color": "#4285F4",
        "url": "https://deepmind.google/",
        "snippet": "Gemini 2.0 outperforms GPT-4 on HumanEval and MBPP benchmarks, with particular strength in multi-step reasoning and repository-level code understanding tasks.",
        "timestamp": "4 hours ago",
        "category": "Research",
        "category_color": "#4285F4",
    },
    {
        "headline": "Anthropic Releases Claude 4 with Improved Safety Guardrails and Extended Context",
        "source": "Anthropic",
        "source_color": "#C97E4D",
        "url": "https://anthropic.com/news",
        "snippet": "Claude 4 introduces a 500K token context window and significantly enhanced Constitutional AI techniques, reducing harmful output rates by 40% compared to Claude 3.",
        "timestamp": "6 hours ago",
        "category": "Safety",
        "category_color": "#C97E4D",
    },
    {
        "headline": "Meta's Llama 4 Open-Source Model Outperforms Previous Closed-Source Rivals",
        "source": "Meta AI",
        "source_color": "#0866FF",
        "url": "https://ai.meta.com/blog/",
        "snippet": "Meta's Llama 4 70B model achieves state-of-the-art performance on MMLU and HellaSwag, available under a permissive commercial license for businesses with under 700M users.",
        "timestamp": "8 hours ago",
        "category": "Open Source",
        "category_color": "#0866FF",
    },
    {
        "headline": "Microsoft Integrates AI Agents Deeply Into Office 365 Productivity Suite",
        "source": "Microsoft AI",
        "source_color": "#00A4EF",
        "url": "https://blogs.microsoft.com/ai/",
        "snippet": "Copilot agents can now autonomously draft, schedule, and follow up on emails, analyze spreadsheets, and generate presentation slides with minimal human input.",
        "timestamp": "10 hours ago",
        "category": "Industry",
        "category_color": "#00A4EF",
    },
    {
        "headline": "Stanford HAI Report: AI Adoption in Enterprise Doubles Year-Over-Year",
        "source": "Stanford HAI",
        "source_color": "#8C1515",
        "url": "https://hai.stanford.edu/news",
        "snippet": "The 2026 AI Index shows enterprise AI adoption reached 78% of Fortune 500 companies, with natural language processing and computer vision leading deployment categories.",
        "timestamp": "1 day ago",
        "category": "Research",
        "category_color": "#8C1515",
    },
    {
        "headline": "EU AI Act Enforcement Begins: Companies Rush to Audit High-Risk Systems",
        "source": "MIT Technology Review",
        "source_color": "#A31F34",
        "url": "https://www.technologyreview.com/topic/artificial-intelligence/",
        "snippet": "With the EU AI Act now in effect, compliance teams are scrambling to classify their systems, conduct mandatory conformity assessments, and register high-risk AI deployments.",
        "timestamp": "1 day ago",
        "category": "Policy",
        "category_color": "#A31F34",
    },
    {
        "headline": "New Research Shows AI Can Design Novel Proteins for Drug Discovery at Scale",
        "source": "Nature",
        "source_color": "#1A6E3C",
        "url": "https://www.nature.com/subjects/machine-learning",
        "snippet": "AlphaFold-derived protein design tools have enabled researchers to generate and wet-lab validate 150+ novel enzymes targeting antibiotic-resistant bacteria in a single study.",
        "timestamp": "2 days ago",
        "category": "Science",
        "category_color": "#1A6E3C",
    },
]


HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>AI News</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg: #F0F2F5;
      --surface: #fff;
      --border: #E4E8EF;
      --text-primary: #0F172A;
      --text-secondary: #64748B;
      --text-muted: #94A3B8;
      --accent-default: #6366F1;
      --header-h: 72px;
      --radius-card: 14px;
      --radius-btn: 10px;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text-primary);
      min-height: 100vh;
    }

    /* ── HEADER ────────────────────────────────────────── */
    .app-header {
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      position: sticky;
      top: 0;
      z-index: 20;
      box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }

    .header-inner {
      max-width: 800px;
      margin: 0 auto;
      padding: 0 1.25rem;
      height: var(--header-h);
      display: flex;
      align-items: center;
      gap: 1rem;
    }

    .header-brand {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      flex-shrink: 0;
    }

    /* AI logo badge */
    .ai-badge {
      width: 40px;
      height: 40px;
      border-radius: 12px;
      background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #A855F7 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 2px 8px rgba(99,102,241,0.45);
      flex-shrink: 0;
    }

    .ai-badge svg {
      width: 22px;
      height: 22px;
    }

    .brand-text h1 {
      font-size: 1.15rem;
      font-weight: 800;
      color: var(--text-primary);
      letter-spacing: -0.02em;
      line-height: 1.2;
    }

    .brand-text .tagline {
      font-size: 0.72rem;
      color: var(--text-muted);
      line-height: 1;
      margin-top: 1px;
    }

    /* Toolbar */
    .header-toolbar {
      flex: 1;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      justify-content: flex-end;
    }

    .search-wrap {
      position: relative;
      flex: 1;
      max-width: 280px;
    }

    .search-wrap svg {
      position: absolute;
      left: 10px;
      top: 50%;
      transform: translateY(-50%);
      width: 15px;
      height: 15px;
      color: var(--text-muted);
      pointer-events: none;
    }

    .search-input {
      width: 100%;
      height: 36px;
      border: 1.5px solid var(--border);
      border-radius: var(--radius-btn);
      background: var(--bg);
      padding: 0 0.75rem 0 2.1rem;
      font-size: 0.82rem;
      color: var(--text-primary);
      outline: none;
      transition: border-color 0.15s;
    }

    .search-input:focus {
      border-color: #6366F1;
      background: #fff;
    }

    .search-input::placeholder { color: var(--text-muted); }

    .toolbar-btn {
      width: 36px;
      height: 36px;
      border: 1.5px solid var(--border);
      border-radius: var(--radius-btn);
      background: var(--bg);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      color: var(--text-secondary);
      transition: background 0.15s, border-color 0.15s, color 0.15s;
      position: relative;
      flex-shrink: 0;
    }

    .toolbar-btn:hover, .toolbar-btn.active {
      background: #EEF2FF;
      border-color: #6366F1;
      color: #6366F1;
    }

    .toolbar-btn svg {
      width: 16px;
      height: 16px;
    }

    /* Filter dropdown */
    .filter-dropdown {
      position: absolute;
      top: calc(100% + 8px);
      right: 0;
      background: var(--surface);
      border: 1.5px solid var(--border);
      border-radius: 12px;
      padding: 0.5rem;
      min-width: 160px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.12);
      display: none;
      z-index: 30;
    }

    .filter-dropdown.open { display: block; }

    .filter-option {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.45rem 0.6rem;
      border-radius: 8px;
      cursor: pointer;
      font-size: 0.8rem;
      color: var(--text-secondary);
      transition: background 0.12s;
    }

    .filter-option:hover { background: var(--bg); }
    .filter-option.selected { color: #6366F1; background: #EEF2FF; }

    .filter-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      flex-shrink: 0;
    }

    /* ── FEED CONTAINER ───────────────────────────────── */
    .feed-wrap {
      max-width: 800px;
      margin: 0 auto;
      padding: 1.25rem 1.25rem 3rem;
    }

    /* ── SKELETON LOADING ─────────────────────────────── */
    .skeleton-card {
      background: var(--surface);
      border-radius: var(--radius-card);
      padding: 1.1rem 1.25rem;
      margin-bottom: 0.75rem;
      border-left: 4px solid #E2E8F0;
    }

    .skel {
      background: linear-gradient(90deg, #EEF2FF 25%, #E2E8EF 50%, #EEF2FF 75%);
      background-size: 200% 100%;
      animation: shimmer 1.4s infinite;
      border-radius: 6px;
    }

    @keyframes shimmer {
      0% { background-position: 200% 0; }
      100% { background-position: -200% 0; }
    }

    .skel-row { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem; }
    .skel-avatar { width: 40px; height: 40px; border-radius: 10px; flex-shrink: 0; }
    .skel-lines { flex: 1; }
    .skel-line { height: 11px; margin-bottom: 6px; }
    .skel-line.short { width: 40%; }
    .skel-line.medium { width: 65%; }
    .skel-line.full { width: 100%; }
    .skel-headline { height: 14px; width: 90%; margin-bottom: 8px; }
    .skel-snippet { height: 11px; margin-bottom: 5px; }

    /* ── ILLUSTRATED STATES ───────────────────────────── */
    .state-panel {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 4rem 1.5rem;
      text-align: center;
    }

    .state-illustration { margin-bottom: 1.5rem; }

    .state-title {
      font-size: 1.1rem;
      font-weight: 700;
      color: var(--text-primary);
      margin-bottom: 0.4rem;
    }

    .state-body {
      font-size: 0.85rem;
      color: var(--text-secondary);
      max-width: 280px;
      line-height: 1.55;
      margin-bottom: 1.25rem;
    }

    .state-cta {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      background: linear-gradient(135deg, #6366F1, #8B5CF6);
      color: #fff;
      border: none;
      border-radius: 10px;
      padding: 0.6rem 1.35rem;
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      transition: opacity 0.15s, transform 0.15s;
      box-shadow: 0 4px 14px rgba(99,102,241,0.35);
    }

    .state-cta:hover { opacity: 0.9; transform: translateY(-1px); }

    .state-cta.secondary {
      background: var(--surface);
      color: var(--text-secondary);
      border: 1.5px solid var(--border);
      box-shadow: none;
    }

    /* ── FEED CARDS ───────────────────────────────────── */
    .feed { display: flex; flex-direction: column; gap: 0.75rem; }

    .card {
      background: var(--surface);
      border-radius: var(--radius-card);
      border-left: 4px solid var(--card-accent, #6366F1);
      box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 4px 16px rgba(0,0,0,0.04);
      overflow: hidden;
      transition: box-shadow 0.18s, transform 0.18s;
    }

    .card:hover {
      box-shadow: 0 4px 20px rgba(0,0,0,0.10), 0 1px 4px rgba(0,0,0,0.06);
      transform: translateY(-2px);
    }

    .card[data-hidden="true"] { display: none; }

    .card-link {
      display: block;
      padding: 1rem 1.25rem 0.75rem;
      text-decoration: none;
      color: inherit;
    }

    .card-top {
      display: flex;
      align-items: flex-start;
      gap: 0.875rem;
    }

    /* Source logo — real brand mark */
    .source-logo {
      flex-shrink: 0;
      width: 44px;
      height: 44px;
      border-radius: 11px;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 1.5px solid var(--border);
      background: var(--bg);
    }

    .source-logo svg {
      width: 44px;
      height: 44px;
    }

    .card-body { flex: 1; min-width: 0; }

    .card-meta-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.5rem;
      margin-bottom: 0.35rem;
    }

    .source-name {
      font-size: 0.7rem;
      font-weight: 700;
      color: var(--card-accent, #6366F1);
      text-transform: uppercase;
      letter-spacing: 0.06em;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .card-badges {
      display: flex;
      align-items: center;
      gap: 0.35rem;
      flex-shrink: 0;
    }

    .category-badge {
      font-size: 0.64rem;
      font-weight: 600;
      padding: 2px 7px;
      border-radius: 20px;
      background: color-mix(in srgb, var(--card-accent, #6366F1) 12%, transparent);
      color: var(--card-accent, #6366F1);
      white-space: nowrap;
    }

    .timestamp {
      font-size: 0.7rem;
      color: var(--text-muted);
      white-space: nowrap;
    }

    .headline {
      font-size: 0.95rem;
      font-weight: 700;
      line-height: 1.45;
      color: var(--text-primary);
      margin-bottom: 0.4rem;
      transition: color 0.15s;
    }

    .card:hover .headline { color: var(--card-accent, #6366F1); }

    .snippet {
      font-size: 0.82rem;
      color: var(--text-secondary);
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

    .read-more {
      font-size: 0.7rem;
      color: var(--text-muted);
      display: flex;
      align-items: center;
      gap: 0.25rem;
      text-decoration: none;
    }

    .read-more svg {
      width: 11px;
      height: 11px;
      stroke: currentColor;
      fill: none;
      stroke-width: 2;
      stroke-linecap: round;
      stroke-linejoin: round;
    }

    /* ── NO-RESULTS INLINE ────────────────────────────── */
    .no-results {
      text-align: center;
      padding: 2.5rem 1rem;
      color: var(--text-muted);
      font-size: 0.85rem;
      display: none;
    }

    /* ── RESPONSIVE ───────────────────────────────────── */
    @media (max-width: 540px) {
      .header-inner { padding: 0 1rem; }
      .brand-text h1 { font-size: 1rem; }
      .brand-text .tagline { display: none; }
      .search-wrap { max-width: none; }
      .feed-wrap { padding: 1rem 0.75rem 2rem; }
      .card-link { padding: 0.875rem 1rem 0.625rem; }
      .card-footer { padding: 0 1rem 0.625rem; }
      .source-logo { width: 38px; height: 38px; border-radius: 9px; }
      .source-logo svg { width: 38px; height: 38px; }
      .headline { font-size: 0.88rem; }
      .snippet { font-size: 0.78rem; }
    }
  </style>
</head>
<body>

<header class="app-header">
  <div class="header-inner">
    <div class="header-brand">
      <!-- AI logo badge -->
      <div class="ai-badge" aria-hidden="true">
        <svg viewBox="0 0 22 22" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M11 2 L13.2 8.2 L19.8 8.2 L14.6 12.2 L16.8 18.4 L11 14.4 L5.2 18.4 L7.4 12.2 L2.2 8.2 L8.8 8.2 Z" fill="white" opacity="0.9"/>
          <circle cx="11" cy="11" r="2.5" fill="white"/>
        </svg>
      </div>
      <div class="brand-text">
        <h1>AI News</h1>
        <p class="tagline">Latest from the world of artificial intelligence</p>
      </div>
    </div>

    <div class="header-toolbar">
      <!-- Search -->
      <div class="search-wrap">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="7" cy="7" r="4.5"/><path d="M10.5 10.5 L14 14"/>
        </svg>
        <input
          class="search-input"
          type="search"
          placeholder="Search headlines…"
          id="search-input"
          aria-label="Search headlines"
        />
      </div>

      <!-- Filter -->
      <button class="toolbar-btn" id="filter-btn" aria-label="Filter by category" title="Filter">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
          <path d="M2 4h12M4 8h8M6 12h4"/>
        </svg>
        <div class="filter-dropdown" id="filter-dropdown">
          <div class="filter-option selected" data-cat="all">
            <span class="filter-dot" style="background:#6366F1"></span> All
          </div>
          <div class="filter-option" data-cat="Research">
            <span class="filter-dot" style="background:#4285F4"></span> Research
          </div>
          <div class="filter-option" data-cat="Open Source">
            <span class="filter-dot" style="background:#FF9D00"></span> Open Source
          </div>
          <div class="filter-option" data-cat="Safety">
            <span class="filter-dot" style="background:#C97E4D"></span> Safety
          </div>
          <div class="filter-option" data-cat="Industry">
            <span class="filter-dot" style="background:#00A4EF"></span> Industry
          </div>
          <div class="filter-option" data-cat="Policy">
            <span class="filter-dot" style="background:#A31F34"></span> Policy
          </div>
          <div class="filter-option" data-cat="Science">
            <span class="filter-dot" style="background:#1A6E3C"></span> Science
          </div>
        </div>
      </button>

      <!-- Settings -->
      <button class="toolbar-btn" id="settings-btn" aria-label="Settings" title="Settings">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="8" cy="8" r="2.5"/>
          <path d="M8 1.5 L8 3M8 13 L8 14.5M1.5 8 L3 8M13 8 L14.5 8M3.3 3.3 L4.4 4.4M11.6 11.6 L12.7 12.7M3.3 12.7 L4.4 11.6M11.6 4.4 L12.7 3.3"/>
        </svg>
      </button>
    </div>
  </div>
</header>

<div class="feed-wrap">

  <!-- LOADING STATE -->
  <div id="state-loading">
    {% for _ in range(4) %}
    <div class="skeleton-card">
      <div class="skel-row">
        <div class="skel skel-avatar"></div>
        <div class="skel-lines">
          <div class="skel skel-line short"></div>
          <div class="skel skel-line medium"></div>
        </div>
      </div>
      <div class="skel skel-headline"></div>
      <div class="skel skel-snippet full"></div>
      <div class="skel skel-snippet medium" style="width:70%;margin-top:5px"></div>
    </div>
    {% endfor %}
  </div>

  <!-- EMPTY STATE -->
  <div id="state-empty" class="state-panel" hidden>
    <div class="state-illustration">
      <!-- Friendly robot SVG illustration -->
      <svg width="160" height="160" viewBox="0 0 160 160" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <!-- Stars / sparkles background -->
        <circle cx="30" cy="25" r="3" fill="#C7D2FE" opacity="0.7"/>
        <circle cx="130" cy="35" r="2" fill="#A5B4FC" opacity="0.6"/>
        <circle cx="145" cy="80" r="2.5" fill="#C7D2FE" opacity="0.5"/>
        <circle cx="20" cy="100" r="2" fill="#A5B4FC" opacity="0.5"/>
        <path d="M50 20 L52 16 L54 20 L50 20Z" fill="#C7D2FE" opacity="0.6"/>
        <path d="M120 18 L122 14 L124 18 L120 18Z" fill="#A5B4FC" opacity="0.6"/>

        <!-- Robot body -->
        <rect x="52" y="72" width="56" height="52" rx="12" fill="#6366F1"/>
        <rect x="58" y="78" width="44" height="28" rx="7" fill="#4338CA"/>

        <!-- Antenna -->
        <rect x="78" y="50" width="4" height="18" rx="2" fill="#818CF8"/>
        <circle cx="80" cy="47" r="7" fill="#A5B4FC"/>
        <circle cx="80" cy="47" r="4" fill="#6366F1"/>
        <circle cx="80" cy="47" r="2" fill="#fff"/>

        <!-- Head -->
        <rect x="57" y="56" width="46" height="36" rx="13" fill="#818CF8"/>

        <!-- Eyes -->
        <ellipse cx="70" cy="70" rx="6" ry="6.5" fill="#fff"/>
        <ellipse cx="90" cy="70" rx="6" ry="6.5" fill="#fff"/>
        <circle cx="71" cy="71" r="3.5" fill="#4338CA"/>
        <circle cx="91" cy="71" r="3.5" fill="#4338CA"/>
        <circle cx="72.5" cy="69.5" r="1.2" fill="#fff"/>
        <circle cx="92.5" cy="69.5" r="1.2" fill="#fff"/>

        <!-- Mouth — neutral/sad arc -->
        <path d="M73 81 Q80 78 87 81" stroke="#4338CA" stroke-width="2" stroke-linecap="round" fill="none"/>

        <!-- Arms -->
        <rect x="36" y="76" width="18" height="8" rx="4" fill="#818CF8"/>
        <rect x="106" y="76" width="18" height="8" rx="4" fill="#818CF8"/>
        <circle cx="34" cy="80" r="5" fill="#A5B4FC"/>
        <circle cx="126" cy="80" r="5" fill="#A5B4FC"/>

        <!-- Legs -->
        <rect x="62" y="120" width="14" height="22" rx="7" fill="#6366F1"/>
        <rect x="84" y="120" width="14" height="22" rx="7" fill="#6366F1"/>
        <rect x="59" y="136" width="20" height="10" rx="5" fill="#4338CA"/>
        <rect x="81" y="136" width="20" height="10" rx="5" fill="#4338CA"/>

        <!-- Chest panel -->
        <rect x="66" y="84" width="28" height="14" rx="5" fill="#6366F1"/>
        <circle cx="74" cy="91" r="2.5" fill="#A5B4FC"/>
        <circle cx="80" cy="91" r="2.5" fill="#818CF8"/>
        <circle cx="86" cy="91" r="2.5" fill="#C7D2FE"/>
      </svg>
    </div>
    <p class="state-title">No news to show yet</p>
    <p class="state-body">Your AI news feed is empty right now. Check back later or reload to fetch the latest headlines.</p>
    <button class="state-cta" onclick="reloadFeed()">
      <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M13 2.5 A7 7 0 1 0 14.5 8"/><polyline points="10.5 2 13 2.5 12.5 5"/>
      </svg>
      Reload Feed
    </button>
  </div>

  <!-- ERROR STATE -->
  <div id="state-error" class="state-panel" hidden>
    <div class="state-illustration">
      <!-- Broken/sad robot SVG illustration -->
      <svg width="160" height="160" viewBox="0 0 160 160" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <!-- Warning lightning bolts -->
        <path d="M25 30 L20 45 L27 45 L22 60 L32 42 L25 42 L30 30Z" fill="#FCD34D" opacity="0.7"/>
        <path d="M135 20 L131 32 L136 32 L132 44 L140 30 L135 30 L139 20Z" fill="#FCD34D" opacity="0.6"/>

        <!-- Robot body (tilted slightly, distressed) -->
        <rect x="52" y="72" width="56" height="52" rx="12" fill="#EF4444" transform="rotate(-3 80 98)"/>
        <rect x="58" y="78" width="44" height="28" rx="7" fill="#DC2626" transform="rotate(-3 80 92)"/>

        <!-- Cracked antenna -->
        <line x1="80" y1="50" x2="78" y2="56" stroke="#F87171" stroke-width="3" stroke-linecap="round"/>
        <line x1="78" y1="56" x2="82" y2="60" stroke="#F87171" stroke-width="3" stroke-linecap="round"/>
        <circle cx="80" cy="47" r="7" fill="#FCA5A5"/>
        <circle cx="80" cy="47" r="4" fill="#EF4444"/>
        <!-- X on antenna ball -->
        <path d="M77 44 L83 50M83 44 L77 50" stroke="#fff" stroke-width="1.5" stroke-linecap="round"/>

        <!-- Head (tilted) -->
        <rect x="57" y="56" width="46" height="36" rx="13" fill="#F87171" transform="rotate(-3 80 74)"/>

        <!-- X eyes -->
        <path d="M64 65 L71 72M71 65 L64 72" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/>
        <path d="M84 65 L91 72M91 65 L84 72" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/>

        <!-- Sad mouth -->
        <path d="M70 82 Q80 76 90 82" stroke="#fff" stroke-width="2" stroke-linecap="round" fill="none"/>

        <!-- Arms drooping -->
        <rect x="34" y="80" width="20" height="7" rx="3.5" fill="#F87171" transform="rotate(20 44 83)"/>
        <rect x="106" y="80" width="20" height="7" rx="3.5" fill="#F87171" transform="rotate(-20 116 83)"/>

        <!-- Legs (wonky) -->
        <rect x="62" y="120" width="14" height="20" rx="7" fill="#EF4444" transform="rotate(-5 69 130)"/>
        <rect x="84" y="120" width="14" height="20" rx="7" fill="#EF4444" transform="rotate(5 91 130)"/>

        <!-- Sparks / error lines -->
        <path d="M102 62 L108 55" stroke="#FCD34D" stroke-width="2" stroke-linecap="round"/>
        <path d="M105 70 L113 68" stroke="#FCD34D" stroke-width="1.5" stroke-linecap="round"/>
        <path d="M100 77 L107 78" stroke="#FCD34D" stroke-width="1.5" stroke-linecap="round"/>
      </svg>
    </div>
    <p class="state-title">Couldn't load feed</p>
    <p class="state-body">Something went wrong while loading the AI news feed. Check your connection and try again.</p>
    <div style="display:flex;gap:0.6rem;flex-wrap:wrap;justify-content:center">
      <button class="state-cta" onclick="reloadFeed()">
        <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M13 2.5 A7 7 0 1 0 14.5 8"/><polyline points="10.5 2 13 2.5 12.5 5"/>
        </svg>
        Try Again
      </button>
    </div>
  </div>

  <!-- SUCCESS / FEED STATE -->
  <div id="state-feed" hidden>
    <div class="feed" id="feed-list">
      {% for item in news %}
      <article
        class="card"
        style="--card-accent: {{ item.source_color }}"
        data-category="{{ item.category }}"
        data-headline="{{ item.headline | lower }}"
        data-source="{{ item.source | lower }}"
        data-hidden="false"
      >
        <a class="card-link" href="{{ item.url }}" target="_blank" rel="noopener noreferrer">
          <div class="card-top">
            <div class="source-logo" aria-label="{{ item.source }} logo">
              {{ item.logo_svg | safe }}
            </div>
            <div class="card-body">
              <div class="card-meta-row">
                <span class="source-name">{{ item.source }}</span>
                <div class="card-badges">
                  <span class="category-badge">{{ item.category }}</span>
                  <span class="timestamp">{{ item.timestamp }}</span>
                </div>
              </div>
              <div class="headline">{{ item.headline }}</div>
              <div class="snippet">{{ item.snippet }}</div>
            </div>
          </div>
        </a>
        <div class="card-footer">
          <a class="read-more" href="{{ item.url }}" target="_blank" rel="noopener noreferrer">
            opens in new tab
            <svg viewBox="0 0 24 24"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
          </a>
        </div>
      </article>
      {% endfor %}
    </div>
    <div class="no-results" id="no-results">No headlines match your search.</div>
  </div>

</div>

<script>
  // ── State machine ──────────────────────────────────
  function showState(name) {
    ['loading','empty','error','feed'].forEach(function(s) {
      document.getElementById('state-' + s).hidden = (s !== name);
    });
  }

  function reloadFeed() {
    showState('loading');
    setTimeout(function() {
      showState('feed');
      applyFilters();
    }, 700);
  }

  // Simulate page load: show loading briefly then reveal feed
  window.addEventListener('DOMContentLoaded', function() {
    showState('loading');
    setTimeout(function() {
      showState('feed');
    }, 900);
  });

  // ── Search + Filter ────────────────────────────────
  var currentCategory = 'all';

  function applyFilters() {
    var query = document.getElementById('search-input').value.toLowerCase().trim();
    var cards = document.querySelectorAll('#feed-list .card');
    var visible = 0;
    cards.forEach(function(card) {
      var catMatch = currentCategory === 'all' || card.dataset.category === currentCategory;
      var searchMatch = !query ||
        card.dataset.headline.includes(query) ||
        card.dataset.source.includes(query);
      var show = catMatch && searchMatch;
      card.dataset.hidden = show ? 'false' : 'true';
      if (show) visible++;
    });
    document.getElementById('no-results').style.display = visible === 0 ? 'block' : 'none';
  }

  document.getElementById('search-input').addEventListener('input', applyFilters);

  // ── Filter dropdown ────────────────────────────────
  var filterBtn = document.getElementById('filter-btn');
  var filterDropdown = document.getElementById('filter-dropdown');

  filterBtn.addEventListener('click', function(e) {
    e.stopPropagation();
    var isOpen = filterDropdown.classList.toggle('open');
    filterBtn.classList.toggle('active', isOpen);
  });

  document.querySelectorAll('.filter-option').forEach(function(opt) {
    opt.addEventListener('click', function(e) {
      e.stopPropagation();
      document.querySelectorAll('.filter-option').forEach(function(o) { o.classList.remove('selected'); });
      opt.classList.add('selected');
      currentCategory = opt.dataset.cat;
      filterDropdown.classList.remove('open');
      filterBtn.classList.remove('active');
      applyFilters();
    });
  });

  document.addEventListener('click', function() {
    filterDropdown.classList.remove('open');
    filterBtn.classList.remove('active');
  });

  // ── Settings (stub — shows a quick toast) ─────────
  document.getElementById('settings-btn').addEventListener('click', function() {
    this.classList.toggle('active');
  });
</script>
</body>
</html>"""


def _enrich(items):
    for item in items:
        item["logo_svg"] = SOURCE_LOGOS.get(item["source"], _fallback_logo(item))
    return items


def _fallback_logo(item):
    initials = "".join(w[0].upper() for w in item["source"].split()[:2])
    color = item.get("source_color", "#6366F1")
    return (
        f'<svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">'
        f'<circle cx="20" cy="20" r="20" fill="{color}"/>'
        f'<text x="20" y="25" text-anchor="middle" font-family="Arial,sans-serif" '
        f'font-weight="700" font-size="13" fill="#fff">{initials}</text></svg>'
    )


@app.route("/")
def index():
    return render_template_string(HTML, news=_enrich(NEWS_ITEMS))


@app.route("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
