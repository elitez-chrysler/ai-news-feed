from flask import Flask, request
import json

app = Flask(__name__)

NEWS_ARTICLES = [
    {
        "id": "a1",
        "category": "tech",
        "headline": "OpenAI Ships GPT-5 With Native Reasoning and 1M-Token Context Window",
        "source": "OpenAI Blog",
        "snippet": "The latest flagship model introduces chain-of-thought reasoning as a first-class primitive, alongside a one-million token context window enabling full codebase ingestion in a single pass.",
        "timestamp": "1H AGO",
        "read_time": "3 MIN",
    },
    {
        "id": "a2",
        "category": "world",
        "headline": "EU AI Act Enforcement Begins — First Fines Issued to High-Risk Biometric Systems",
        "source": "Reuters",
        "snippet": "European regulators issued the first wave of penalties under the AI Act, targeting biometric surveillance systems deployed without required conformity assessments and human oversight logs.",
        "timestamp": "3H AGO",
        "read_time": "5 MIN",
    },
    {
        "id": "a3",
        "category": "tech",
        "headline": "Apple Intelligence Expands to 40 Languages with On-Device Model Upgrades",
        "source": "9to5Mac",
        "snippet": "iOS 19.2 ships upgraded on-device models for Siri, Writing Tools, and Image Playground, with hardware-optimised inference pathways reducing generation latency by 60% on A18 chips.",
        "timestamp": "5H AGO",
        "read_time": "4 MIN",
    },
    {
        "id": "a4",
        "category": "business",
        "headline": "Goldman Sachs: AI Automation to Add $7 Trillion to Global GDP by 2030",
        "source": "Financial Times",
        "snippet": "A new Goldman Sachs research report projects AI-driven automation could lift global labour productivity by 1.5 percentage points annually, compounding over the next five years.",
        "timestamp": "7H AGO",
        "read_time": "6 MIN",
    },
    {
        "id": "a5",
        "category": "design",
        "headline": "Nothing Phone 3 Renders Leaked — Dot Matrix Interface Evolves Beyond the Back Panel",
        "source": "The Verge",
        "snippet": "Exclusive renders of the Nothing Phone 3 reveal an evolved Ndot system with adaptive dot-matrix displays extending throughout OS-level interface elements, from the lock screen to notification drawers.",
        "timestamp": "9H AGO",
        "read_time": "3 MIN",
    },
    {
        "id": "a6",
        "category": "world",
        "headline": "Huawei Ships Kirin 9030, Closing the Gap with TSMC 3nm Through Advanced Packaging",
        "source": "SCMP",
        "snippet": "Huawei's Kirin 9030 achieves 5nm-equivalent performance through multi-die chiplet packaging, marking a milestone in China's domestic semiconductor self-sufficiency push.",
        "timestamp": "11H AGO",
        "read_time": "7 MIN",
    },
    {
        "id": "a7",
        "category": "tech",
        "headline": "Anthropic Claude 4 Sets New SOTA on Multi-Step Reasoning — 92.3% on GPQA Diamond",
        "source": "Anthropic Research",
        "snippet": "Claude 4 tops ARC-AGI-2 and GPQA Diamond benchmarks, with researchers attributing gains to Constitutional AI 2.0 training and improved self-critique loops during post-training.",
        "timestamp": "13H AGO",
        "read_time": "5 MIN",
    },
    {
        "id": "a8",
        "category": "business",
        "headline": "Microsoft AI Division Hits $50B Annual Revenue Run Rate, Beats Analyst Guidance by 12%",
        "source": "Bloomberg",
        "snippet": "Microsoft's AI Cloud segment exceeded analyst consensus driven by Azure OpenAI enterprise adoption and Copilot seat growth now exceeding 400 million monthly active users globally.",
        "timestamp": "15H AGO",
        "read_time": "4 MIN",
    },
]

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<script>
(function(){var t=localStorage.getItem('ndotnews:theme')||'dark';document.documentElement.setAttribute('data-theme',t);})();
</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>N·FEED — AI News</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Doto:wght@400;700&family=DotGothic16&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
button{background:none;border:none;cursor:pointer;font:inherit;color:inherit;}
input{font:inherit;}
a{color:inherit;text-decoration:none;}

:root{
  --accent:#D71921;
  --tr:0.2s ease;
  --bg:#ffffff;
  --surface:#f5f5f5;
  --text-1:#000000;
  --text-2:#555555;
  --text-3:#999999;
  --border:#e0e0e0;
  --border-2:#eeeeee;
  --skel-a:#ebebeb;
  --skel-b:#f8f8f8;
}
[data-theme="dark"]{
  --bg:#000000;
  --surface:#111111;
  --text-1:#ffffff;
  --text-2:#aaaaaa;
  --text-3:#555555;
  --border:#222222;
  --border-2:#191919;
  --skel-a:#1a1a1a;
  --skel-b:#2a2a2a;
}

html,body{
  height:100%;
  font-family:'Inter',system-ui,sans-serif;
  background:var(--bg);
  color:var(--text-1);
  transition:background var(--tr),color var(--tr);
  -webkit-font-smoothing:antialiased;
  overflow:hidden;
}

.dot{font-family:'Doto','DotGothic16',monospace;letter-spacing:0.06em;}

@keyframes shimmer{0%{background-position:-600px 0}100%{background-position:600px 0}}
.skel{
  background:linear-gradient(90deg,var(--skel-a) 25%,var(--skel-b) 50%,var(--skel-a) 75%);
  background-size:1200px 100%;
  animation:shimmer 1.6s linear infinite;
}

/* ── LAYOUT ────────────────────────────── */
.app{display:flex;height:100vh;overflow:hidden;}

/* ── LEFT RAIL ─────────────────────────── */
.rail{
  display:none;
  width:220px;
  flex-shrink:0;
  flex-direction:column;
  border-right:1px solid var(--border);
  padding:28px 20px 20px;
  gap:32px;
  transition:border-color var(--tr);
}
@media(min-width:768px){.rail{display:flex;}}

.rail-logo{
  font-family:'Doto','DotGothic16',monospace;
  font-size:18px;
  font-weight:700;
  letter-spacing:0.1em;
  color:var(--text-1);
}
.rail-logo .dot-red{color:var(--accent);}

.rail-nav{display:flex;flex-direction:column;gap:2px;flex:1;}

.rail-item{
  display:flex;align-items:center;gap:10px;
  padding:9px 10px;
  font-family:'Doto','DotGothic16',monospace;
  font-size:10px;letter-spacing:0.1em;
  color:var(--text-3);
  border:1px solid transparent;
  transition:color var(--tr),border-color var(--tr);
}
.rail-item.active{color:var(--text-1);border-color:var(--border);}
.rail-item:hover:not(.active){color:var(--text-2);}

.rail-divider{height:1px;background:var(--border);margin:6px 0;transition:background var(--tr);}

/* ── MAIN ──────────────────────────────── */
.main{flex:1;display:flex;flex-direction:column;overflow:hidden;min-width:0;}

/* ── MOBILE HEADER ─────────────────────── */
.mob-header{
  display:flex;align-items:center;justify-content:space-between;
  padding:14px 18px;
  border-bottom:1px solid var(--border);
  flex-shrink:0;
  transition:border-color var(--tr);
}
@media(min-width:768px){.mob-header{display:none;}}

.mob-logo{
  font-family:'Doto','DotGothic16',monospace;
  font-size:17px;font-weight:700;letter-spacing:0.1em;
}
.mob-logo .dot-red{color:var(--accent);}

.mob-actions{display:flex;align-items:center;gap:14px;}

/* ── DESKTOP TOPBAR ────────────────────── */
.desk-top{
  display:none;align-items:center;gap:16px;
  padding:16px 28px;
  border-bottom:1px solid var(--border);
  flex-shrink:0;
  transition:border-color var(--tr);
}
@media(min-width:768px){.desk-top{display:flex;}}

/* ── SEARCH ────────────────────────────── */
.search-wrap{flex:1;position:relative;}
.search-icon{position:absolute;left:11px;top:50%;transform:translateY(-50%);color:var(--text-3);pointer-events:none;}
.search-inp{
  width:100%;
  background:var(--surface);
  border:1px solid var(--border);
  color:var(--text-1);
  padding:9px 14px 9px 36px;
  font-family:'Doto','DotGothic16',monospace;
  font-size:11px;letter-spacing:0.08em;
  outline:none;
  transition:border-color var(--tr),background var(--tr),color var(--tr);
}
.search-inp::placeholder{color:var(--text-3);}
.search-inp:focus{border-color:var(--text-2);}

/* ── MOBILE SEARCH ─────────────────────── */
.mob-search{
  padding:10px 18px;
  border-bottom:1px solid var(--border);
  flex-shrink:0;
  transition:border-color var(--tr);
}
@media(min-width:768px){.mob-search{display:none;}}

/* ── DARK MODE TOGGLE ──────────────────── */
.toggle-wrap{display:flex;align-items:center;gap:7px;cursor:pointer;flex-shrink:0;user-select:none;}
.toggle-label{
  font-family:'Doto','DotGothic16',monospace;
  font-size:9px;letter-spacing:0.12em;
  color:var(--text-2);white-space:nowrap;
  transition:color var(--tr);
}
.toggle-track{
  width:34px;height:18px;
  border:1px solid var(--border);
  position:relative;
  background:var(--surface);
  flex-shrink:0;
  transition:border-color var(--tr),background var(--tr);
}
.toggle-knob{
  position:absolute;top:3px;left:3px;
  width:10px;height:10px;
  background:var(--text-3);
  transition:left 0.2s ease,background 0.2s ease;
}
[data-theme="dark"] .toggle-knob{left:19px;background:var(--accent);}

/* ── DOT MENU ICON ─────────────────────── */
.dot-menu{
  display:grid;
  grid-template-columns:repeat(3,4px);
  grid-template-rows:repeat(3,4px);
  gap:3px;padding:3px;
  color:var(--text-1);
}
.dot-menu span{width:4px;height:4px;background:currentColor;border-radius:50%;}

/* ── TABS BAR ──────────────────────────── */
.tabs{
  display:flex;
  border-bottom:1px solid var(--border);
  overflow-x:auto;scrollbar-width:none;
  flex-shrink:0;
  transition:border-color var(--tr);
}
.tabs::-webkit-scrollbar{display:none;}
.tab{
  flex-shrink:0;
  padding:11px 18px;
  font-family:'Doto','DotGothic16',monospace;
  font-size:10px;letter-spacing:0.1em;
  color:var(--text-3);
  border-bottom:2px solid transparent;
  white-space:nowrap;
  transition:color var(--tr),border-color var(--tr);
}
.tab.active{color:var(--text-1);border-bottom-color:var(--accent);}
.tab:hover:not(.active){color:var(--text-2);}
@media(min-width:768px){.tab{padding:13px 22px;}}

/* ── FEED AREA ─────────────────────────── */
.feed{flex:1;overflow-y:auto;overflow-x:hidden;padding-bottom:72px;}
@media(min-width:768px){.feed{padding-bottom:20px;}}

/* ── CARD ──────────────────────────────── */
.card{border-bottom:1px solid var(--border);padding:18px 18px 14px;transition:border-color var(--tr);}
@media(min-width:768px){.card{padding:22px 28px 18px;}}

.card-meta{display:flex;justify-content:space-between;align-items:center;margin-bottom:9px;}
.card-source{
  display:flex;align-items:center;gap:6px;
  font-family:'Doto','DotGothic16',monospace;
  font-size:8px;letter-spacing:0.12em;
  color:var(--text-3);transition:color var(--tr);
}
.dot-red-sm{width:5px;height:5px;background:var(--accent);border-radius:50%;flex-shrink:0;}
.card-time{
  font-family:'Doto','DotGothic16',monospace;
  font-size:8px;letter-spacing:0.08em;color:var(--text-3);
  transition:color var(--tr);
}

.card-body{display:flex;gap:14px;align-items:flex-start;}
.card-text{flex:1;min-width:0;}
.card-headline{
  font-size:14px;font-weight:500;line-height:1.35;
  color:var(--text-1);margin-bottom:5px;
  transition:color var(--tr);
}
@media(min-width:768px){.card-headline{font-size:15px;}}
.card-snippet{
  font-size:12px;font-weight:300;line-height:1.55;
  color:var(--text-2);transition:color var(--tr);
}

.card-thumb{
  width:68px;height:68px;flex-shrink:0;
  border:1px solid var(--border);overflow:hidden;
  transition:border-color var(--tr);
}
@media(min-width:768px){.card-thumb{width:84px;height:84px;}}
.card-thumb svg{display:block;width:100%;height:100%;}

.card-foot{display:flex;align-items:center;justify-content:space-between;margin-top:10px;}
.card-cat{
  display:flex;align-items:center;gap:5px;
  font-family:'Doto','DotGothic16',monospace;
  font-size:8px;letter-spacing:0.12em;color:var(--text-3);
  transition:color var(--tr);
}
.cat-dot{width:4px;height:4px;background:var(--accent);border-radius:50%;}
.bk-btn{padding:3px;color:var(--text-3);transition:color var(--tr);line-height:1;}
.bk-btn.saved{color:var(--text-1);}
.bk-btn:hover{color:var(--text-1);}

/* ── SKELETON CARD ─────────────────────── */
.sk-line{height:10px;border-radius:1px;margin-bottom:7px;}
.sk-s{width:28%}.sk-m{width:55%}.sk-l{width:82%}.sk-f{width:100%}
.sk-thumb{width:68px;height:68px;flex-shrink:0;border-radius:1px;}
@media(min-width:768px){.sk-thumb{width:84px;height:84px;}}

/* ── STATE VIEWS ───────────────────────── */
.state-view{
  display:flex;flex-direction:column;align-items:center;
  justify-content:center;padding:60px 28px;text-align:center;gap:18px;
}
.state-glyph{color:var(--text-3);transition:color var(--tr);}
.state-hl{
  font-family:'Doto','DotGothic16',monospace;
  font-size:18px;letter-spacing:0.15em;
  color:var(--text-1);transition:color var(--tr);
}
.state-copy{
  font-size:12px;font-weight:300;line-height:1.65;
  color:var(--text-2);max-width:280px;transition:color var(--tr);
}
.cta-row{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;}
.cta-p{
  background:var(--accent);color:#fff;
  padding:11px 22px;
  font-family:'Doto','DotGothic16',monospace;
  font-size:10px;letter-spacing:0.12em;
  transition:opacity 0.2s;
}
.cta-p:hover{opacity:0.85;}
.cta-s{
  background:transparent;color:var(--text-1);
  padding:11px 22px;
  font-family:'Doto','DotGothic16',monospace;
  font-size:10px;letter-spacing:0.12em;
  border:1px solid var(--border);
  transition:border-color var(--tr),color var(--tr);
}
.cta-s:hover{border-color:var(--text-2);}

/* ── CONNECTION HELP ───────────────────── */
.conn-help{
  border:1px solid var(--border);padding:14px 18px;
  text-align:left;width:100%;max-width:300px;
  transition:border-color var(--tr);
}
.conn-help.hidden{display:none;}
.conn-title{
  font-family:'Doto','DotGothic16',monospace;
  font-size:9px;letter-spacing:0.1em;color:var(--text-2);margin-bottom:10px;
  transition:color var(--tr);
}
.conn-row{
  display:flex;align-items:center;gap:8px;
  font-size:11px;color:var(--text-2);line-height:1.8;
  transition:color var(--tr);
}
.conn-dot{width:3px;height:3px;background:var(--text-3);border-radius:50%;flex-shrink:0;}

/* ── BOTTOM NAV ────────────────────────── */
.bnav{
  position:fixed;bottom:0;left:0;right:0;
  border-top:1px solid var(--border);background:var(--bg);
  display:flex;z-index:100;
  transition:border-color var(--tr),background var(--tr);
}
@media(min-width:768px){.bnav{display:none;}}
.bnav-item{
  flex:1;display:flex;flex-direction:column;align-items:center;gap:3px;
  padding:10px 4px 14px;
  font-family:'Doto','DotGothic16',monospace;
  font-size:7px;letter-spacing:0.1em;color:var(--text-3);
  transition:color var(--tr);
}
.bnav-item.active{color:var(--text-1);}
.bnav-item:hover:not(.active){color:var(--text-2);}

.hidden{display:none!important;}
</style>
</head>
<body>

<div class="app">
  <!-- LEFT RAIL (desktop) -->
  <nav class="rail" id="rail">
    <div class="rail-logo dot">N<span class="dot-red">·</span>FEED</div>
    <div class="rail-nav">
      <button class="rail-item active" data-nav="feed">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <circle cx="3" cy="3" r="1.5" fill="currentColor"/>
          <circle cx="7" cy="3" r="1.5" fill="currentColor"/>
          <circle cx="11" cy="3" r="1.5" fill="currentColor"/>
          <circle cx="3" cy="7" r="1.5" fill="currentColor"/>
          <circle cx="7" cy="7" r="1.5" fill="currentColor"/>
          <circle cx="11" cy="7" r="1.5" fill="currentColor"/>
          <circle cx="3" cy="11" r="1.5" fill="currentColor"/>
          <circle cx="7" cy="11" r="1.5" fill="currentColor"/>
          <circle cx="11" cy="11" r="1.5" fill="currentColor"/>
        </svg>
        FEED
      </button>
      <button class="rail-item" data-nav="discover">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <circle cx="7" cy="7" r="5.5" stroke="currentColor" stroke-width="1"/>
          <circle cx="7" cy="7" r="1.5" fill="currentColor"/>
          <circle cx="7" cy="2" r="1" fill="currentColor"/>
          <circle cx="12" cy="7" r="1" fill="currentColor"/>
          <circle cx="7" cy="12" r="1" fill="currentColor"/>
          <circle cx="2" cy="7" r="1" fill="currentColor"/>
        </svg>
        DISCOVER
      </button>
      <button class="rail-item" data-nav="saved">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <circle cx="3" cy="2" r="1" fill="currentColor"/>
          <circle cx="7" cy="2" r="1" fill="currentColor"/>
          <circle cx="11" cy="2" r="1" fill="currentColor"/>
          <circle cx="3" cy="6" r="1" fill="currentColor"/>
          <circle cx="11" cy="6" r="1" fill="currentColor"/>
          <circle cx="3" cy="10" r="1" fill="currentColor"/>
          <circle cx="11" cy="10" r="1" fill="currentColor"/>
          <circle cx="5" cy="13" r="1" fill="currentColor"/>
          <circle cx="9" cy="13" r="1" fill="currentColor"/>
          <circle cx="7" cy="11" r="1.5" fill="currentColor"/>
        </svg>
        SAVED
      </button>
      <button class="rail-item" data-nav="profile">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <circle cx="7" cy="4" r="2.5" stroke="currentColor" stroke-width="1"/>
          <path d="M2 13 C2 9.5 12 9.5 12 13" stroke="currentColor" stroke-width="1" fill="none"/>
          <circle cx="7" cy="4" r="1" fill="currentColor"/>
        </svg>
        PROFILE
      </button>
      <div class="rail-divider"></div>
      <button class="rail-item" data-nav="settings">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <circle cx="7" cy="7" r="2" stroke="currentColor" stroke-width="1"/>
          <circle cx="7" cy="1.5" r="1" fill="currentColor"/>
          <circle cx="7" cy="12.5" r="1" fill="currentColor"/>
          <circle cx="12.5" cy="7" r="1" fill="currentColor"/>
          <circle cx="1.5" cy="7" r="1" fill="currentColor"/>
          <circle cx="11" cy="3" r="1" fill="currentColor"/>
          <circle cx="3" cy="11" r="1" fill="currentColor"/>
          <circle cx="11" cy="11" r="1" fill="currentColor"/>
          <circle cx="3" cy="3" r="1" fill="currentColor"/>
        </svg>
        SETTINGS
      </button>
      <button class="rail-item" data-nav="signout">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <circle cx="3" cy="2" r="1" fill="currentColor"/>
          <circle cx="3" cy="5" r="1" fill="currentColor"/>
          <circle cx="3" cy="8" r="1" fill="currentColor"/>
          <circle cx="3" cy="11" r="1" fill="currentColor"/>
          <circle cx="6" cy="7" r="1" fill="currentColor"/>
          <circle cx="9" cy="7" r="1" fill="currentColor"/>
          <circle cx="12" cy="7" r="1" fill="currentColor"/>
          <circle cx="10" cy="5" r="1" fill="currentColor"/>
          <circle cx="10" cy="9" r="1" fill="currentColor"/>
        </svg>
        SIGN OUT
      </button>
    </div>
  </nav>

  <!-- MAIN -->
  <main class="main">

    <!-- MOBILE HEADER -->
    <header class="mob-header">
      <div class="mob-logo dot">N<span class="dot-red">·</span>FEED</div>
      <div class="mob-actions">
        <label class="toggle-wrap" id="toggle-mob" aria-label="Toggle dark mode">
          <span class="toggle-label dot">DARK MODE</span>
          <div class="toggle-track"><div class="toggle-knob"></div></div>
        </label>
        <button class="dot-menu" id="menu-btn" aria-label="Menu" aria-expanded="false">
          <span></span><span></span><span></span>
          <span></span><span></span><span></span>
          <span></span><span></span><span></span>
        </button>
      </div>
    </header>

    <!-- DESKTOP TOPBAR -->
    <div class="desk-top">
      <div class="search-wrap">
        <svg class="search-icon" width="13" height="13" viewBox="0 0 13 13" fill="none">
          <circle cx="5.5" cy="5.5" r="4" stroke="currentColor" stroke-width="1.2"/>
          <path d="M8.5 8.5 L11.5 11.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
        </svg>
        <input type="search" class="search-inp dot" placeholder="SEARCH AI NEWS..." id="search-desk" autocomplete="off" aria-label="Search articles"/>
      </div>
      <label class="toggle-wrap" id="toggle-desk" aria-label="Toggle dark mode">
        <span class="toggle-label dot">DARK MODE</span>
        <div class="toggle-track"><div class="toggle-knob"></div></div>
      </label>
    </div>

    <!-- MOBILE SEARCH -->
    <div class="mob-search">
      <div class="search-wrap">
        <svg class="search-icon" width="13" height="13" viewBox="0 0 13 13" fill="none">
          <circle cx="5.5" cy="5.5" r="4" stroke="currentColor" stroke-width="1.2"/>
          <path d="M8.5 8.5 L11.5 11.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
        </svg>
        <input type="search" class="search-inp dot" placeholder="SEARCH AI NEWS..." id="search-mob" autocomplete="off" aria-label="Search articles"/>
      </div>
    </div>

    <!-- TABS -->
    <div class="tabs" id="tabs" role="tablist" aria-label="News categories">
      <button class="tab dot active" data-tab="all" role="tab" aria-selected="true">FOR YOU</button>
      <button class="tab dot" data-tab="tech" role="tab" aria-selected="false">TECH</button>
      <button class="tab dot" data-tab="world" role="tab" aria-selected="false">WORLD</button>
      <button class="tab dot" data-tab="business" role="tab" aria-selected="false">BUSINESS</button>
      <button class="tab dot" data-tab="design" role="tab" aria-selected="false">DESIGN</button>
    </div>

    <!-- FEED -->
    <div class="feed" id="feed" role="main" aria-live="polite"></div>

  </main>
</div>

<!-- BOTTOM NAV (mobile) -->
<nav class="bnav" id="bnav">
  <button class="bnav-item dot active" data-nav="feed">
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
      <circle cx="4" cy="4" r="2" fill="currentColor"/>
      <circle cx="9" cy="4" r="2" fill="currentColor"/>
      <circle cx="14" cy="4" r="2" fill="currentColor"/>
      <circle cx="4" cy="9" r="2" fill="currentColor"/>
      <circle cx="9" cy="9" r="2" fill="currentColor"/>
      <circle cx="14" cy="9" r="2" fill="currentColor"/>
      <circle cx="4" cy="14" r="2" fill="currentColor"/>
      <circle cx="9" cy="14" r="2" fill="currentColor"/>
      <circle cx="14" cy="14" r="2" fill="currentColor"/>
    </svg>
    FEED
  </button>
  <button class="bnav-item dot" data-nav="discover">
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
      <circle cx="9" cy="9" r="7" stroke="currentColor" stroke-width="1.2"/>
      <circle cx="9" cy="9" r="2" fill="currentColor"/>
      <circle cx="9" cy="3" r="1" fill="currentColor"/>
      <circle cx="15" cy="9" r="1" fill="currentColor"/>
      <circle cx="9" cy="15" r="1" fill="currentColor"/>
      <circle cx="3" cy="9" r="1" fill="currentColor"/>
    </svg>
    DISCOVER
  </button>
  <button class="bnav-item dot" data-nav="saved">
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
      <circle cx="4" cy="2" r="1.2" fill="currentColor"/>
      <circle cx="9" cy="2" r="1.2" fill="currentColor"/>
      <circle cx="14" cy="2" r="1.2" fill="currentColor"/>
      <circle cx="4" cy="7" r="1.2" fill="currentColor"/>
      <circle cx="14" cy="7" r="1.2" fill="currentColor"/>
      <circle cx="4" cy="12" r="1.2" fill="currentColor"/>
      <circle cx="14" cy="12" r="1.2" fill="currentColor"/>
      <circle cx="6.5" cy="16" r="1.2" fill="currentColor"/>
      <circle cx="11.5" cy="16" r="1.2" fill="currentColor"/>
      <circle cx="9" cy="14" r="1.8" fill="currentColor"/>
    </svg>
    SAVED
  </button>
  <button class="bnav-item dot" data-nav="profile">
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
      <circle cx="9" cy="6" r="3.5" stroke="currentColor" stroke-width="1.2"/>
      <path d="M2 17 C2 12 16 12 16 17" stroke="currentColor" stroke-width="1.2" fill="none" stroke-linecap="round"/>
    </svg>
    PROFILE
  </button>
</nav>

<script>
(function(){
'use strict';

var ARTICLES = __ARTICLES_JSON__;
var FORCED = '__FORCED_STATE__';

var state = {
  tab: 'all',
  query: '',
  feed: 'loading',
  nav: 'feed',
  bookmarks: [],
  connHelp: false
};

try { state.bookmarks = JSON.parse(localStorage.getItem('ndotnews:bookmarks') || '[]'); } catch(e) {}

// ── THEME ──────────────────────────────────
function applyTheme(t) {
  document.documentElement.setAttribute('data-theme', t);
  try { localStorage.setItem('ndotnews:theme', t); } catch(e) {}
}
function toggleTheme() {
  applyTheme(document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
}
document.getElementById('toggle-mob').addEventListener('click', function(e){ e.preventDefault(); toggleTheme(); });
document.getElementById('toggle-desk').addEventListener('click', function(e){ e.preventDefault(); toggleTheme(); });

// ── TABS ───────────────────────────────────
document.getElementById('tabs').addEventListener('click', function(e) {
  var tab = e.target.closest('.tab');
  if (!tab) return;
  document.querySelectorAll('.tab').forEach(function(t) {
    t.classList.remove('active'); t.setAttribute('aria-selected','false');
  });
  tab.classList.add('active'); tab.setAttribute('aria-selected','true');
  state.tab = tab.dataset.tab;
  state.query = '';
  document.getElementById('search-mob').value = '';
  document.getElementById('search-desk').value = '';
  if (state.feed !== 'loading') renderFeed();
});

// ── NAV ────────────────────────────────────
function setupNav(el) {
  if (!el) return;
  el.addEventListener('click', function(e) {
    var item = e.target.closest('[data-nav]');
    if (!item) return;
    var id = item.dataset.nav;
    state.nav = id;
    document.querySelectorAll('[data-nav]').forEach(function(n){ n.classList.remove('active'); });
    document.querySelectorAll('[data-nav="'+id+'"]').forEach(function(n){ n.classList.add('active'); });
    if (id === 'saved') { renderSaved(); return; }
    if (id === 'feed') {
      state.tab = 'all';
      state.query = '';
      document.getElementById('search-mob').value = '';
      document.getElementById('search-desk').value = '';
      document.querySelectorAll('.tab').forEach(function(t){
        t.classList.toggle('active', t.dataset.tab === 'all');
        t.setAttribute('aria-selected', t.dataset.tab === 'all' ? 'true' : 'false');
      });
      loadFeed();
    }
  });
}
setupNav(document.getElementById('rail'));
setupNav(document.getElementById('bnav'));

// ── SEARCH ─────────────────────────────────
function onSearch(val) {
  state.query = val.toLowerCase().trim();
  var other = document.getElementById(this === document.getElementById('search-mob') ? 'search-desk' : 'search-mob');
  other.value = val;
  if (state.feed !== 'loading') renderFeed();
}
function bindSearch(id) {
  var inp = document.getElementById(id);
  var timer;
  inp.addEventListener('input', function() {
    var v = inp.value;
    clearTimeout(timer);
    timer = setTimeout(function() { onSearch.call(inp, v); }, 280);
  });
  inp.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') { clearTimeout(timer); onSearch.call(inp, inp.value); }
  });
}
bindSearch('search-mob');
bindSearch('search-desk');

// ── BOOKMARKS ──────────────────────────────
function saveBookmarks() {
  try { localStorage.setItem('ndotnews:bookmarks', JSON.stringify(state.bookmarks)); } catch(e) {}
}
function toggleBookmark(id) {
  var idx = state.bookmarks.indexOf(id);
  if (idx === -1) state.bookmarks.push(id); else state.bookmarks.splice(idx, 1);
  saveBookmarks();
  var btn = document.querySelector('[data-bk="'+id+'"]');
  if (btn) {
    var saved = state.bookmarks.indexOf(id) !== -1;
    btn.classList.toggle('saved', saved);
    btn.innerHTML = bkIcon(saved);
    btn.setAttribute('aria-label', saved ? 'Remove bookmark' : 'Add bookmark');
  }
}

// ── FEED EVENTS (delegated) ─────────────────
document.getElementById('feed').addEventListener('click', function(e) {
  var bk = e.target.closest('[data-bk]');
  if (bk) { e.preventDefault(); toggleBookmark(bk.dataset.bk); return; }

  var retry = e.target.closest('#retry-btn');
  if (retry) { loadFeed(); return; }

  var conn = e.target.closest('#conn-btn');
  if (conn) {
    state.connHelp = !state.connHelp;
    var help = document.getElementById('conn-help');
    if (help) help.classList.toggle('hidden', !state.connHelp);
    return;
  }

  var explore = e.target.closest('#explore-btn');
  if (explore) {
    state.tab = 'all';
    state.query = '';
    document.getElementById('search-mob').value = '';
    document.getElementById('search-desk').value = '';
    document.querySelectorAll('.tab').forEach(function(t){
      t.classList.toggle('active', t.dataset.tab === 'all');
      t.setAttribute('aria-selected', t.dataset.tab === 'all' ? 'true' : 'false');
    });
    renderFeed();
    return;
  }
});

// ── RENDER HELPERS ──────────────────────────
function esc(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function bkIcon(saved) {
  if (saved) return '<svg width="15" height="15" viewBox="0 0 15 15" fill="none"><path d="M3 2H12V14L7.5 10.5L3 14Z" stroke="currentColor" stroke-width="1.2" fill="currentColor"/></svg>';
  return '<svg width="15" height="15" viewBox="0 0 15 15" fill="none"><path d="M3 2H12V14L7.5 10.5L3 14Z" stroke="currentColor" stroke-width="1.2" fill="none"/></svg>';
}

function thumb(id) {
  var map = {
    a1: '<rect width="88" height="88" fill="#2a2a2a"/><circle cx="44" cy="44" r="22" stroke="#555" stroke-width="1.5"/><circle cx="44" cy="44" r="12" stroke="#666" stroke-width="1"/><circle cx="44" cy="44" r="4" fill="#777"/>',
    a2: '<rect width="88" height="88" fill="#222"/><line x1="10" y1="28" x2="78" y2="28" stroke="#555" stroke-width="1"/><line x1="10" y1="44" x2="78" y2="44" stroke="#444" stroke-width="1"/><line x1="10" y1="60" x2="78" y2="60" stroke="#555" stroke-width="1"/><circle cx="44" cy="44" r="10" stroke="#666" stroke-width="1" fill="none"/>',
    a3: '<rect width="88" height="88" fill="#1e1e1e"/><path d="M10 44 Q44 12 78 44 Q44 76 10 44Z" stroke="#555" stroke-width="1.5" fill="none"/><circle cx="44" cy="44" r="5" fill="#666"/>',
    a4: '<rect width="88" height="88" fill="#2d2d2d"/><rect x="14" y="50" width="8" height="28" fill="#444"/><rect x="26" y="36" width="8" height="42" fill="#555"/><rect x="38" y="22" width="8" height="56" fill="#666"/><rect x="50" y="32" width="8" height="46" fill="#555"/><rect x="62" y="44" width="8" height="34" fill="#444"/>',
    a5: '<rect width="88" height="88" fill="#1a1a1a"/>'+dotGrid(88,88,10,'#3a3a3a'),
    a6: '<rect width="88" height="88" fill="#282828"/><path d="M12 76 L44 12 L76 76Z" stroke="#555" stroke-width="1.5" fill="none"/><circle cx="44" cy="40" r="4" fill="#666"/>',
    a7: '<rect width="88" height="88" fill="#1e1e1e"/><circle cx="44" cy="44" r="28" stroke="#444" stroke-width="1"/><circle cx="44" cy="44" r="18" stroke="#555" stroke-width="1"/><circle cx="44" cy="44" r="8" stroke="#666" stroke-width="1"/><circle cx="44" cy="44" r="3" fill="#777"/>',
    a8: '<rect width="88" height="88" fill="#2a2a2a"/><line x1="10" y1="10" x2="78" y2="78" stroke="#444" stroke-width="1"/><line x1="78" y1="10" x2="10" y2="78" stroke="#444" stroke-width="1"/><circle cx="44" cy="44" r="18" stroke="#666" stroke-width="1.5" fill="none"/>'
  };
  var inner = map[id] || '<rect width="88" height="88" fill="#333"/>';
  return '<svg viewBox="0 0 88 88" fill="none" xmlns="http://www.w3.org/2000/svg">'+inner+'</svg>';
}

function dotGrid(w, h, spacing, color) {
  var out = '';
  for (var x = spacing; x < w; x += spacing)
    for (var y = spacing; y < h; y += spacing)
      out += '<circle cx="'+x+'" cy="'+y+'" r="1.5" fill="'+color+'"/>';
  return out;
}

function cardHtml(a) {
  var saved = state.bookmarks.indexOf(a.id) !== -1;
  return '<article class="card" data-id="'+a.id+'">' +
    '<div class="card-meta">' +
      '<div class="card-source dot"><span class="dot-red-sm"></span>AI CURATED · '+esc(a.source.toUpperCase())+'</div>' +
      '<span class="card-time dot">'+esc(a.timestamp)+' · '+esc(a.read_time)+'</span>' +
    '</div>' +
    '<div class="card-body">' +
      '<div class="card-text">' +
        '<h2 class="card-headline">'+esc(a.headline)+'</h2>' +
        '<p class="card-snippet">'+esc(a.snippet)+'</p>' +
      '</div>' +
      '<div class="card-thumb">'+thumb(a.id)+'</div>' +
    '</div>' +
    '<div class="card-foot">' +
      '<div class="card-cat dot"><span class="cat-dot"></span>'+esc(a.category.toUpperCase())+'</div>' +
      '<button class="bk-btn'+(saved?' saved':'')+'" data-bk="'+a.id+'" aria-label="'+(saved?'Remove bookmark':'Add bookmark')+'">'+bkIcon(saved)+'</button>' +
    '</div>' +
  '</article>';
}

function skelCard() {
  return '<article class="card">' +
    '<div class="card-meta">' +
      '<div class="sk-line sk-s skel"></div>' +
      '<div class="sk-line skel" style="width:18%;height:8px;"></div>' +
    '</div>' +
    '<div class="card-body">' +
      '<div class="card-text">' +
        '<div class="sk-line sk-l skel"></div>' +
        '<div class="sk-line sk-f skel"></div>' +
        '<div class="sk-line sk-m skel"></div>' +
      '</div>' +
      '<div class="sk-thumb skel"></div>' +
    '</div>' +
    '<div class="card-foot" style="margin-top:10px"><div class="sk-line sk-s skel"></div></div>' +
  '</article>';
}

function emptyGlyph() {
  return '<svg width="60" height="60" viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg">' +
    '<rect x="10" y="6" width="40" height="48" stroke="currentColor" stroke-width="1.2"/>' +
    '<circle cx="21" cy="20" r="2" fill="currentColor"/>' +
    '<circle cx="30" cy="20" r="2" fill="currentColor"/>' +
    '<circle cx="39" cy="20" r="2" fill="currentColor"/>' +
    '<circle cx="21" cy="30" r="2" fill="currentColor"/>' +
    '<circle cx="30" cy="30" r="2" fill="currentColor"/>' +
    '<circle cx="39" cy="30" r="2" fill="currentColor"/>' +
    '<circle cx="21" cy="40" r="2" fill="currentColor"/>' +
    '<circle cx="30" cy="40" r="2" fill="currentColor"/>' +
    '<circle cx="39" cy="40" r="2" fill="currentColor"/>' +
  '</svg>';
}

function errorGlyph() {
  return '<svg width="64" height="56" viewBox="0 0 64 56" fill="none" xmlns="http://www.w3.org/2000/svg">' +
    '<path d="M12 38 C10 32 13 24 20 22 C20 14 26 8 34 8 C42 8 48 14 48 22 C54 23 58 28 58 34 C58 42 52 46 46 46 H16 C13 46 10 43 12 38Z" stroke="currentColor" stroke-width="1.2" fill="none"/>' +
    '<circle cx="24" cy="30" r="2" fill="currentColor"/>' +
    '<circle cx="32" cy="24" r="2" fill="currentColor"/>' +
    '<circle cx="40" cy="30" r="2" fill="currentColor"/>' +
    '<circle cx="24" cy="24" r="2" fill="currentColor"/>' +
    '<circle cx="40" cy="24" r="2" fill="currentColor"/>' +
    '<circle cx="32" cy="36" r="2" fill="currentColor"/>' +
  '</svg>';
}

function emptyHtml() {
  return '<div class="state-view" role="status">' +
    '<div class="state-glyph">'+emptyGlyph()+'</div>' +
    '<h2 class="state-hl dot">NO NEWS YET</h2>' +
    '<p class="state-copy">No articles match your current filters. Try a different category or check back soon.</p>' +
    '<button class="cta-p dot" id="explore-btn">EXPLORE CATEGORIES</button>' +
  '</div>';
}

function errorHtml() {
  return '<div class="state-view" role="alert">' +
    '<div class="state-glyph">'+errorGlyph()+'</div>' +
    '<h2 class="state-hl dot">SOMETHING WENT WRONG</h2>' +
    '<p class="state-copy">We couldn\'t load the latest news. Please check your connection and try again.</p>' +
    '<div class="cta-row">' +
      '<button class="cta-p dot" id="retry-btn">RETRY</button>' +
      '<button class="cta-s dot" id="conn-btn">CHECK CONNECTION</button>' +
    '</div>' +
    '<div class="conn-help hidden" id="conn-help">' +
      '<p class="conn-title dot">CONNECTIVITY GUIDE</p>' +
      '<div class="conn-row"><span class="conn-dot"></span>Check your Wi-Fi or mobile data connection</div>' +
      '<div class="conn-row"><span class="conn-dot"></span>Toggle airplane mode on then off</div>' +
      '<div class="conn-row"><span class="conn-dot"></span>Restart your router or access point</div>' +
      '<div class="conn-row"><span class="conn-dot"></span>Open your device network settings</div>' +
    '</div>' +
  '</div>';
}

function getFiltered() {
  return ARTICLES.filter(function(a) {
    if (state.tab !== 'all' && a.category !== state.tab) return false;
    if (!state.query) return true;
    return a.headline.toLowerCase().indexOf(state.query) !== -1 ||
           a.snippet.toLowerCase().indexOf(state.query) !== -1 ||
           a.source.toLowerCase().indexOf(state.query) !== -1;
  });
}

function renderFeed() {
  var feed = document.getElementById('feed');
  if (state.feed === 'loading') {
    var sk = ''; for (var i=0;i<4;i++) sk += skelCard();
    feed.innerHTML = sk;
    return;
  }
  if (state.feed === 'error') { state.connHelp = false; feed.innerHTML = errorHtml(); return; }
  var arts = getFiltered();
  if (arts.length === 0 || state.feed === 'empty') { feed.innerHTML = emptyHtml(); return; }
  feed.innerHTML = arts.map(cardHtml).join('');
}

function renderSaved() {
  var feed = document.getElementById('feed');
  var arts = ARTICLES.filter(function(a){ return state.bookmarks.indexOf(a.id) !== -1; });
  if (arts.length === 0) { feed.innerHTML = emptyHtml(); return; }
  feed.innerHTML = arts.map(cardHtml).join('');
}

function loadFeed() {
  state.feed = 'loading';
  state.connHelp = false;
  renderFeed();

  if (FORCED === 'loading') return;

  var target = FORCED || 'success';
  var start = Date.now();

  setTimeout(function() {
    var elapsed = Date.now() - start;
    var wait = Math.max(0, 300 - elapsed);
    setTimeout(function() {
      if (target === 'error') state.feed = 'error';
      else if (target === 'empty') state.feed = 'empty';
      else state.feed = 'success';
      renderFeed();
    }, wait);
  }, 900 + Math.floor(Math.random() * 400));
}

loadFeed();

})();
</script>
</body>
</html>
"""


@app.route("/")
def index():
    forced = request.args.get("state", "")
    safe_forced = forced if forced in ("loading", "empty", "error") else "success"
    html = HTML_TEMPLATE.replace("__ARTICLES_JSON__", json.dumps(NEWS_ARTICLES))
    html = html.replace("__FORCED_STATE__", safe_forced)
    return html


if __name__ == "__main__":
    app.run(debug=True, port=5000)
