#!/usr/bin/env python3
"""Build CSV and HTML flashcards from dutch_verbs_flashcards.tsv.

Front-of-card art uses Twemoji SVGs (Twitter/MIT-style illustrations via jsdelivr);
if an image fails, the raw emoji is shown instead.
"""

import csv
import html as html_lib
import os

from dutch_verbs_french_data import FRENCH_BY_VERB

HERE = os.path.dirname(os.path.abspath(__file__))
TSV_PATH = os.path.join(HERE, "dutch_verbs_flashcards.tsv")
CSV_PATH = os.path.join(HERE, "dutch_verbs_flashcards.csv")
HTML_PATH = os.path.join(HERE, "dutch_verbs_flashcards.html")
HTML_STUDY_PATH = os.path.join(HERE, "dutch_verbs_flashcards_study.html")

# Thematic emoji per infinitive (works offline; swap for images in TSV column "emoji" if you prefer)
VERB_EMOJI = {
    "zijn": "✨",
    "hebben": "🤲",
    "worden": "🦋",
    "gaan": "🚶",
    "komen": "🚪",
    "blijven": "🏠",
    "zitten": "🪑",
    "staan": "🧍",
    "liggen": "🛏️",
    "lopen": "🚶‍♂️",
    "doen": "✅",
    "maken": "🔨",
    "zeggen": "💬",
    "geven": "🎁",
    "nemen": "✋",
    "zien": "👁️",
    "weten": "🧠",
    "vinden": "🔍",
    "denken": "💭",
    "laten": "🔓",
    "willen": "❤️",
    "moeten": "⚠️",
    "kunnen": "💪",
    "mogen": "🎫",
    "brengen": "📦",
    "halen": "🔄",
    "houden": "🤝",
    "kopen": "🛒",
    "verkopen": "🏷️",
    "betalen": "💶",
    "werken": "💼",
    "spelen": "🎮",
    "leren": "📚",
    "studeren": "🎓",
    "wonen": "🏘️",
    "lezen": "📖",
    "schrijven": "✍️",
    "spreken": "🗣️",
    "luisteren": "👂",
    "praten": "💬",
    "bellen": "📞",
    "zoeken": "🔎",
    "krijgen": "📥",
    "gebruiken": "🔧",
    "proberen": "🧪",
    "hopen": "🤞",
    "geloven": "⛪",
    "begrijpen": "💡",
    "vergeten": "🌫️",
    "beginnen": "▶️",
    "eten": "🍽️",
    "drinken": "☕",
    "slapen": "😴",
    "koken": "🍳",
    "helpen": "🆘",
    "vragen": "❓",
    "antwoorden": "💬",
    "vertellen": "📜",
    "horen": "👂",
    "noemen": "🏷️",
    "kiezen": "🤔",
    "verliezen": "📉",
    "winnen": "🏆",
    "trekken": "🪢",
    "dragen": "👕",
    "breken": "💔",
    "snijden": "✂️",
    "vliegen": "✈️",
    "zwemmen": "🏊",
    "rijden": "🚗",
    "fietsen": "🚲",
    "reizen": "🧳",
    "bezoeken": "🏛️",
    "ontmoeten": "🤝",
    "bedanken": "🙏",
    "passen": "📏",
    "missen": "🎯",
    "wachten": "⏳",
    "lijken": "👥",
    "voelen": "❤️‍🩹",
    "leven": "❤️",
    "sterven": "⚰️",
    "trouwen": "💒",
    "lachen": "😂",
    "dansen": "💃",
    "zingen": "🎤",
    "springen": "🤸",
    "vallen": "⬇️",
    "opstaan": "⏰",
    "aankomen": "🛬",
    "weggaan": "👋",
    "meenemen": "🎒",
    "verstaan": "👂",
    "herinneren": "🧩",
    "oefenen": "🏋️",
    "dromen": "💤",
    "bestellen": "📋",
    "bereiken": "🎯",
    "beslissen": "⚖️",
    "bouwen": "🏗️",
}


def load_rows():
    with open(TSV_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader)


def enrich_rows(rows):
    for r in rows:
        inf = r.get("infinitive", "")
        if not (r.get("emoji") or "").strip():
            r["emoji"] = VERB_EMOJI.get(inf, "📘")
        fr = FRENCH_BY_VERB.get(inf)
        if fr:
            r["french"], r["sentence_singular_fr"], r["sentence_plural_fr"] = fr
        else:
            r.setdefault("french", "")
            r.setdefault("sentence_singular_fr", "")
            r.setdefault("sentence_plural_fr", "")
    return rows


def write_csv(rows):
    fieldnames = [
        "emoji",
        "infinitive",
        "english",
        "french",
        "perfectum",
        "imperfectum",
        "sentence_singular_nl",
        "sentence_singular_en",
        "sentence_singular_fr",
        "sentence_plural_nl",
        "sentence_plural_en",
        "sentence_plural_fr",
    ]
    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def esc(s):
    return html_lib.escape(s, quote=True)


# Twemoji = flat SVG “clipart” for each emoji; needs network unless cached by browser
TWEMOJI_VERSION = "14.0.2"
TWEMOJI_SVG_BASE = (
    f"https://cdn.jsdelivr.net/gh/twitter/twemoji@{TWEMOJI_VERSION}/assets/svg"
)


def twemoji_svg_url(emoji: str) -> str:
    """Map an emoji string to a Twemoji SVG filename (hyphenated code points)."""
    name = "-".join(f"{ord(ch):x}" for ch in emoji)
    return f"{TWEMOJI_SVG_BASE}/{name}.svg"


def card_front_html(i: int, r: dict) -> str:
    em = r.get("emoji", "📘") or "📘"
    url = twemoji_svg_url(em)
    url_esc = esc(url)
    em_esc = esc(em)
    clipart = (
        f'<div class="clipart" aria-hidden="true">'
        f'<img class="clipart-img" src="{url_esc}" alt="" width="96" height="96" '
        f'decoding="async" loading="lazy" '
        f'onerror="this.style.display=\'none\';var f=this.nextElementSibling;if(f)f.style.display=\'block\'"/>'
        f'<span class="clipart-fallback" style="display:none">{em_esc}</span>'
        f"</div>"
    )
    return (
        f'<div class="num">{i}/100</div>'
        f"{clipart}"
        f'<div class="lemma" lang="nl">{esc(r["infinitive"])}</div>'
        '<div class="glosses">'
        f'<p class="gloss-line" lang="en"><span class="lang">EN</span> {esc(r["english"])}</p>'
        f'<p class="gloss-line" lang="fr"><span class="lang">FR</span> {esc(r.get("french", ""))}</p>'
        "</div>"
    )


def card_back_html(r: dict) -> str:
    return (
        '<div class="tense-grid">'
        '<div class="tense-box vtt">'
        '<div class="tense-head">'
        '<span class="tense-name">Perfectum</span>'
        '<span class="tense-abbr">VTT</span>'
        "</div>"
        f'<p class="tense-value">{esc(r["perfectum"])}</p>'
        "</div>"
        '<div class="tense-box ovt">'
        '<div class="tense-head">'
        '<span class="tense-name">Imperfectum</span>'
        '<span class="tense-abbr">OVT</span>'
        "</div>"
        f'<p class="tense-value">{esc(r["imperfectum"])}</p>'
        "</div>"
        "</div>"
        '<div class="sentences">'
        '<div class="sent-box">'
        '<div class="sent-label">Enkelvoud</div>'
        f'<p class="sent-nl" lang="nl">{esc(r["sentence_singular_nl"])}</p>'
        '<div class="sent-trans">'
        f'<p class="sent-en" lang="en">{esc(r["sentence_singular_en"])}</p>'
        f'<p class="sent-fr" lang="fr">{esc(r.get("sentence_singular_fr", ""))}</p>'
        "</div>"
        "</div>"
        '<div class="sent-box">'
        '<div class="sent-label">Meervoud</div>'
        f'<p class="sent-nl" lang="nl">{esc(r["sentence_plural_nl"])}</p>'
        '<div class="sent-trans">'
        f'<p class="sent-en" lang="en">{esc(r["sentence_plural_en"])}</p>'
        f'<p class="sent-fr" lang="fr">{esc(r.get("sentence_plural_fr", ""))}</p>'
        "</div>"
        "</div>"
        "</div>"
    )


# Mobile: Android Chrome + iPhone Safari — theme bar, installability, home-screen icon
HEAD_MOBILE_EXTRAS = """  <meta name="theme-color" content="#2c6aa0"/>
  <meta name="mobile-web-app-capable" content="yes"/>
  <meta name="apple-mobile-web-app-status-bar-style" content="default"/>
  <meta name="apple-mobile-web-app-title" content="Dutch verbs"/>
  <meta name="format-detection" content="telephone=no"/>
  <link rel="manifest" href="manifest.webmanifest"/>
  <link rel="icon" href="icons/icon.svg" type="image/svg+xml"/>
  <link rel="apple-touch-icon" href="icons/icon.svg"/>
"""

# Shared CSS for Twemoji images + tense layout (injected into both HTML outputs)
CSS_ENHANCEMENTS = """
    .clipart {
      display: flex;
      justify-content: center;
      align-items: center;
      margin: 0 0 0.35rem 0;
      min-height: 100px;
      user-select: none;
    }
    .clipart-img {
      width: 96px;
      height: 96px;
      object-fit: contain;
      filter: drop-shadow(0 2px 6px rgba(0,0,0,.14));
    }
    .clipart-fallback {
      font-size: 3.5rem;
      line-height: 1;
      filter: drop-shadow(0 2px 4px rgba(0,0,0,.1));
    }
    .face.front {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: flex-start;
      text-align: center;
    }
    .face.front .num {
      width: 100%;
      text-align: center;
    }
    .face.front .lemma {
      width: 100%;
      text-align: center;
    }
    .face.front .glosses {
      margin-top: 0.3rem;
      width: 100%;
      text-align: center;
    }
    .face.front .gloss-line {
      margin: 0.4rem 0 0 0;
      font-size: 1.2rem;
      line-height: 1.45;
      text-align: center;
    }
    .face.front .gloss-line .lang {
      display: inline-block;
      min-width: 1.85rem;
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--muted);
      vertical-align: baseline;
    }
    .tense-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.45rem;
      margin-bottom: 0.55rem;
    }
    @media (max-width: 360px) {
      .tense-grid { grid-template-columns: 1fr; }
    }
    .tense-box {
      border-radius: 8px;
      padding: 0.45rem 0.55rem;
      border: 1px solid #9ec5e0;
      background: linear-gradient(145deg, #e8f4fc 0%, #f9fcfe 100%);
    }
    .tense-box.ovt {
      border-color: #b5c9a3;
      background: linear-gradient(145deg, #eef4e6 0%, #fafcf7 100%);
    }
    .tense-head {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      gap: 0.35rem;
      margin-bottom: 0.2rem;
    }
    .tense-name {
      font-weight: 700;
      font-size: 0.68rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--ink);
    }
    .tense-abbr {
      font-size: 0.65rem;
      font-weight: 700;
      color: var(--muted);
    }
    .tense-value {
      margin: 0;
      font-size: 0.86rem;
      line-height: 1.35;
      word-break: break-word;
    }
    .sentences {
      display: grid;
      gap: 0.4rem;
    }
    .sent-box {
      padding: 0.4rem 0.5rem;
      border-radius: 6px;
      border-left: 3px solid var(--accent);
      background: rgba(255,255,255,0.55);
    }
    .sent-label {
      font-size: 0.65rem;
      font-weight: 700;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-bottom: 0.15rem;
    }
    .sent-nl { margin: 0 0 0.25rem 0; font-size: 0.86rem; font-weight: 500; }
    .sent-trans { margin: 0; padding-left: 0.35rem; border-left: 2px solid #dde8f2; }
    .sent-en { margin: 0; font-size: 0.78rem; color: var(--muted); }
    .sent-fr { margin: 0.2rem 0 0 0; font-size: 0.78rem; color: #4a5f6e; }
"""


def write_html(rows):
    cards_html = []
    for i, r in enumerate(rows, 1):
        front = card_front_html(i, r)
        back = card_back_html(r)
        cards_html.append(
            f'<div class="card" data-i="{i}">'
            f'<div class="inner" onclick="this.classList.toggle(\'flipped\')">'
            f'<div class="face front">{front}</div>'
            f'<div class="face back">{back}</div>'
            f"</div></div>"
        )

    doc = f"""<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
  <meta name="color-scheme" content="light"/>
  <meta name="apple-mobile-web-app-capable" content="yes"/>
{HEAD_MOBILE_EXTRAS}  <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin/>
  <title>100 Dutch verbs — flashcards</title>
  <style>
    :root {{
      --bg: #f4f7fb;
      --ink: #1a2b3c;
      --muted: #5a6b7c;
      --accent: #2c6aa0;
      --card: #fff;
      --border: #c8d8e8;
    }}
    html {{
      -webkit-text-size-adjust: 100%;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
      background: var(--bg);
      color: var(--ink);
      margin: 0;
      padding: max(1rem, env(safe-area-inset-top, 0px)) max(1rem, env(safe-area-inset-right, 0px)) max(1rem, env(safe-area-inset-bottom, 0px)) max(1rem, env(safe-area-inset-left, 0px));
      line-height: 1.45;
    }}
    h1 {{
      font-size: 1.3rem;
      font-weight: 600;
      margin: 0 0 0.5rem 0;
      color: var(--accent);
    }}
    .hint {{ font-size: 0.88rem; color: var(--muted); margin-bottom: 1rem; }}
    .footer-note {{ font-size: 0.72rem; color: var(--muted); text-align: center; margin-top: 1.5rem; max-width: 1200px; margin-left: auto; margin-right: auto; }}
    .footer-note a {{ color: var(--accent); }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr));
      gap: 1rem;
      max-width: 1200px;
      margin: 0 auto;
    }}
    .card {{
      perspective: 900px;
      min-height: 0;
    }}
    .inner {{
      position: relative;
      width: 100%;
      min-height: 320px;
      transition: transform 0.55s ease;
      transform-style: preserve-3d;
      cursor: pointer;
      touch-action: manipulation;
      -webkit-tap-highlight-color: transparent;
    }}
    .inner.flipped {{
      transform: rotateY(180deg);
    }}
    .face {{
      position: absolute;
      inset: 0;
      backface-visibility: hidden;
      -webkit-backface-visibility: hidden;
      border-radius: 10px;
      border: 1px solid var(--border);
      background: var(--card);
      padding: 1rem;
      box-shadow: 0 2px 8px rgba(0,0,0,.06);
      overflow: auto;
      -webkit-overflow-scrolling: touch;
    }}
    .back {{
      transform: rotateY(180deg);
      font-size: 0.88rem;
    }}
    .num {{ font-size: 0.75rem; color: var(--muted); margin-bottom: 0.35rem; }}
    .lemma {{ font-size: 1.45rem; font-weight: 700; color: var(--accent); }}
{CSS_ENHANCEMENTS}
  </style>
</head>
<body>
  <h1>100 veelvoorkomende werkwoorden</h1>
  <p class="hint">Klik op een kaart om te draaien — EN &amp; FR op de voorkant; achterkant: VTT / OVT en zinnen (NL / EN / FR). Twemoji: internet nodig. Werkt op telefoon en tablet.</p>
  <div class="grid">
{chr(10).join(cards_html)}
  </div>
  <p class="footer-note">Illustraties: <a href="https://twemoji.twitter.com/" rel="noopener noreferrer">Twemoji</a> (CC-BY 4.0), geladen via jsDelivr.</p>
</body>
</html>
"""
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(doc)


def write_html_study(rows):
    n = len(rows)
    slides = []
    for i, r in enumerate(rows, 1):
        front = card_front_html(i, r)
        back = card_back_html(r)
        hidden = "" if i == 1 else ' hidden aria-hidden="true"'
        slides.append(
            f'<div class="slide"{hidden} data-index="{i - 1}">'
            f'<div class="card">'
            f'<div class="inner" onclick="this.classList.toggle(\'flipped\')">'
            f'<div class="face front">{front}</div>'
            f'<div class="face back">{back}</div>'
            f"</div></div></div>"
        )

    doc = f"""<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
  <meta name="color-scheme" content="light"/>
  <meta name="apple-mobile-web-app-capable" content="yes"/>
{HEAD_MOBILE_EXTRAS}  <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin/>
  <title>100 Dutch verbs — study (one card)</title>
  <style>
    :root {{
      --bg: #f4f7fb;
      --ink: #1a2b3c;
      --muted: #5a6b7c;
      --accent: #2c6aa0;
      --card: #fff;
      --border: #c8d8e8;
    }}
    html {{
      -webkit-text-size-adjust: 100%;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
      background: var(--bg);
      color: var(--ink);
      margin: 0;
      padding: max(1rem, env(safe-area-inset-top, 0px)) max(1rem, env(safe-area-inset-right, 0px)) max(1rem, env(safe-area-inset-bottom, 0px)) max(1rem, env(safe-area-inset-left, 0px));
      line-height: 1.45;
      min-height: 100vh;
      min-height: 100dvh;
      display: flex;
      flex-direction: column;
      align-items: center;
    }}
    h1 {{
      font-size: 1.3rem;
      font-weight: 600;
      margin: 0 0 0.35rem 0;
      color: var(--accent);
    }}
    .hint {{ font-size: 0.88rem; color: var(--muted); margin-bottom: 1rem; text-align: center; max-width: 36rem; }}
    .toolbar {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
      flex-wrap: wrap;
      justify-content: center;
      margin-bottom: 1rem;
    }}
    .toolbar button {{
      font: inherit;
      font-size: 1rem;
      padding: 0.65rem 1.15rem;
      min-height: 48px;
      min-width: 48px;
      border-radius: 10px;
      border: 1px solid var(--border);
      background: var(--card);
      color: var(--ink);
      cursor: pointer;
      touch-action: manipulation;
      -webkit-tap-highlight-color: transparent;
    }}
    .toolbar button:hover:not(:disabled) {{
      background: #e8f0f8;
    }}
    #counter {{
      min-width: 5rem;
      text-align: center;
      font-variant-numeric: tabular-nums;
      color: var(--muted);
      font-size: 0.95rem;
    }}
    .footer-note {{ font-size: 0.72rem; color: var(--muted); text-align: center; margin-top: 1rem; max-width: 36rem; }}
    .footer-note a {{ color: var(--accent); }}
    .viewer {{
      width: 100%;
      max-width: min(480px, 100vw - 2rem);
      flex: 1;
      display: flex;
      align-items: flex-start;
      justify-content: center;
    }}
    .slide {{
      width: 100%;
    }}
    .slide[hidden] {{
      display: none !important;
    }}
    .card {{
      perspective: 900px;
      min-height: 0;
    }}
    .inner {{
      position: relative;
      width: 100%;
      min-height: 400px;
      transition: transform 0.55s ease;
      transform-style: preserve-3d;
      cursor: pointer;
      touch-action: manipulation;
      -webkit-tap-highlight-color: transparent;
    }}
    .inner.flipped {{
      transform: rotateY(180deg);
    }}
    .face {{
      position: absolute;
      inset: 0;
      backface-visibility: hidden;
      -webkit-backface-visibility: hidden;
      border-radius: 10px;
      border: 1px solid var(--border);
      background: var(--card);
      padding: 1.1rem 1.15rem;
      box-shadow: 0 4px 16px rgba(0,0,0,.08);
      overflow: auto;
      -webkit-overflow-scrolling: touch;
    }}
    .back {{
      transform: rotateY(180deg);
      font-size: 0.9rem;
    }}
    .num {{ font-size: 0.75rem; color: var(--muted); margin-bottom: 0.35rem; }}
    .lemma {{ font-size: 1.55rem; font-weight: 700; color: var(--accent); }}
{CSS_ENHANCEMENTS}
  </style>
</head>
<body>
  <h1>100 veelvoorkomende werkwoorden</h1>
  <p class="hint">Eén kaart per keer — EN &amp; FR op de voorkant; achterkant NL/EN/FR. Twemoji (internet). Grote knoppen voor mobiel. Pijltjes of knoppen; tik op de kaart om te draaien.</p>
  <div class="toolbar">
    <button type="button" id="prev" aria-label="Vorige kaart">← Vorige</button>
    <span id="counter">1 / {n}</span>
    <button type="button" id="next" aria-label="Volgende kaart">Volgende →</button>
  </div>
  <div class="viewer" id="viewer">
{chr(10).join(slides)}
  </div>
  <script>
(function() {{
  const total = {n};
  const slides = Array.from(document.querySelectorAll(".slide"));
  const counter = document.getElementById("counter");
  let idx = 0;

  function resetFlip(slide) {{
    const inner = slide.querySelector(".inner");
    if (inner) inner.classList.remove("flipped");
  }}

  function show(at) {{
    const next = ((at % total) + total) % total;
    slides.forEach((el, i) => {{
      const on = i === next;
      el.hidden = !on;
      el.setAttribute("aria-hidden", on ? "false" : "true");
      if (!on) resetFlip(el);
    }});
    idx = next;
    counter.textContent = (idx + 1) + " / " + total;
  }}

  document.getElementById("prev").addEventListener("click", () => show(idx - 1));
  document.getElementById("next").addEventListener("click", () => show(idx + 1));

  let touchStartX = null;
  const viewer = document.getElementById("viewer");
  viewer.addEventListener("touchstart", (e) => {{
    touchStartX = e.changedTouches[0].screenX;
  }}, {{ passive: true }});
  viewer.addEventListener("touchend", (e) => {{
    if (touchStartX === null) return;
    const dx = e.changedTouches[0].screenX - touchStartX;
    if (Math.abs(dx) > 56) {{ if (dx < 0) show(idx + 1); else show(idx - 1); }}
    touchStartX = null;
  }}, {{ passive: true }});

  document.addEventListener("keydown", (e) => {{
    if (e.key === "ArrowLeft") {{ e.preventDefault(); show(idx - 1); }}
    if (e.key === "ArrowRight") {{ e.preventDefault(); show(idx + 1); }}
    if (e.key === " " || e.key === "Enter") {{
      const vis = slides[idx];
      const inner = vis && vis.querySelector(".inner");
      if (inner) {{
        e.preventDefault();
        inner.classList.toggle("flipped");
      }}
    }}
  }});

  show(0);
}})();
  </script>
  <p class="footer-note">Illustraties: <a href="https://twemoji.twitter.com/" rel="noopener noreferrer">Twemoji</a> (CC-BY 4.0), geladen via jsDelivr.</p>
</body>
</html>
"""
    with open(HTML_STUDY_PATH, "w", encoding="utf-8") as f:
        f.write(doc)


def main():
    rows = enrich_rows(load_rows())
    if len(rows) != 100:
        raise SystemExit(f"Expected 100 verbs, found {len(rows)}")
    write_csv(rows)
    write_html(rows)
    write_html_study(rows)
    print(f"Wrote {CSV_PATH}")
    print(f"Wrote {HTML_PATH}")
    print(f"Wrote {HTML_STUDY_PATH}")


if __name__ == "__main__":
    main()
