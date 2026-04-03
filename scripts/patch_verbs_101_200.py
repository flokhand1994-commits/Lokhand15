#!/usr/bin/env python3
"""Append slides 101–200 to index.html and set total to 200."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

TW = "https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/{}.svg"
IMG_ONERR = (
    'onerror="this.style.display=\'none\';var f=this.nextElementSibling;if(f)f.style.display=\'block\'"'
)

# Each tuple: lemma, en, fr, vtt, ovt, vtt_sg_nl, vtt_sg_en, vtt_sg_fr, vtt_pl_nl, vtt_pl_en, vtt_pl_fr,
#             ovt_sg_nl, ovt_sg_en, ovt_sg_fr, ovt_pl_nl, ovt_pl_en, ovt_pl_fr, twemoji_hex, emoji_fb
VERBS: list[tuple[str, ...]] = []


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def slide_html(
    data_index: int,
    card_num: int,
    total: int,
    lemma: str,
    en: str,
    fr: str,
    vtt: str,
    ovt: str,
    vtt_sg_nl: str,
    vtt_sg_en: str,
    vtt_sg_fr: str,
    vtt_pl_nl: str,
    vtt_pl_en: str,
    vtt_pl_fr: str,
    ovt_sg_nl: str,
    ovt_sg_en: str,
    ovt_sg_fr: str,
    ovt_pl_nl: str,
    ovt_pl_en: str,
    ovt_pl_fr: str,
    tw_hex: str,
    emoji_fb: str,
) -> str:
    # All appended slides (101–200) are hidden like slides 2–100
    hidden = " hidden aria-hidden=\"true\""
    return (
        f'<div class="slide"{hidden} data-index="{data_index}"><div class="card"><div class="inner" onclick="this.classList.toggle(\'flipped\')">'
        f'<div class="face front"><div class="num">{card_num}/{total}</div>'
        f'<div class="clipart" aria-hidden="true">'
        f'<img class="clipart-img" src="{TW.format(tw_hex)}" alt="" width="96" height="96" decoding="async" loading="lazy" {IMG_ONERR}/>'
        f'<span class="clipart-fallback" style="display:none">{esc(emoji_fb)}</span></div>'
        f'<div class="lemma" lang="nl">{esc(lemma)}</div>'
        f'<div class="glosses"><p class="gloss-line" lang="en"><span class="lang">EN</span> {esc(en)}</p>'
        f'<p class="gloss-line" lang="fr"><span class="lang">FR</span> {esc(fr)}</p></div></div>'
        f'<div class="face back"><div class="tense-grid">'
        f'<div class="tense-box vtt"><div class="tense-head"><span class="tense-name">Perfectum</span><span class="tense-abbr">VTT</span></div>'
        f'<p class="tense-value">{esc(vtt)}</p></div>'
        f'<div class="tense-box ovt"><div class="tense-head"><span class="tense-name">Imperfectum</span><span class="tense-abbr">OVT</span></div>'
        f'<p class="tense-value">{esc(ovt)}</p></div></div>'
        f'<div class="sentences sent-two-col">'
        f'<div class="sent-col sent-col-vtt"><div class="sent-col-head">Perfectum (VTT)</div>'
        f'<div class="sent-box"><div class="sent-label">Enkelvoud</div><p class="sent-nl" lang="nl">{esc(vtt_sg_nl)}</p>'
        f'<div class="sent-trans"><p class="sent-en" lang="en">{esc(vtt_sg_en)}</p><p class="sent-fr" lang="fr">{esc(vtt_sg_fr)}</p></div></div>'
        f'<div class="sent-box"><div class="sent-label">Meervoud</div><p class="sent-nl" lang="nl">{esc(vtt_pl_nl)}</p>'
        f'<div class="sent-trans"><p class="sent-en" lang="en">{esc(vtt_pl_en)}</p><p class="sent-fr" lang="fr">{esc(vtt_pl_fr)}</p></div></div></div>'
        f'<div class="sent-col sent-col-ovt"><div class="sent-col-head">Imperfectum (OVT)</div>'
        f'<div class="sent-box"><div class="sent-label">Enkelvoud</div><p class="sent-nl" lang="nl">{esc(ovt_sg_nl)}</p>'
        f'<div class="sent-trans"><p class="sent-en" lang="en">{esc(ovt_sg_en)}</p><p class="sent-fr" lang="fr">{esc(ovt_sg_fr)}</p></div></div>'
        f'<div class="sent-box"><div class="sent-label">Meervoud</div><p class="sent-nl" lang="nl">{esc(ovt_pl_nl)}</p>'
        f'<div class="sent-trans"><p class="sent-en" lang="en">{esc(ovt_pl_en)}</p><p class="sent-fr" lang="fr">{esc(ovt_pl_fr)}</p></div></div></div>'
        f"</div></div></div></div></div>"
    )


def load_verbs() -> None:
    global VERBS
    import importlib.util

    data_path = Path(__file__).resolve().parent / "verbs_101_200_data.py"
    spec = importlib.util.spec_from_file_location("verbs_101_200_data", data_path)
    if spec is None or spec.loader is None:
        raise SystemExit("Cannot load verbs_101_200_data.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    VERBS = list(mod.VERBS)


def main() -> None:
    load_verbs()
    if len(VERBS) != 100:
        raise SystemExit(f"Expected 100 verbs, got {len(VERBS)}")
    if 'data-index="199"' in INDEX.read_text(encoding="utf-8"):
        raise SystemExit("Slides 101–200 already present; aborting to avoid duplicates.")
    lemmas_existing = set(
        re.findall(
            r'<div class="lemma" lang="nl">([^<]+)</div>',
            INDEX.read_text(encoding="utf-8"),
        )
    )
    new_lemmas = [v[0].strip().lower() for v in VERBS]
    if len(new_lemmas) != len(set(new_lemmas)):
        raise SystemExit("Duplicate lemma in new list")
    overlap = lemmas_existing & set(new_lemmas)
    if overlap:
        raise SystemExit(f"Lemma overlap with existing cards: {sorted(overlap)}")

    total = 200
    twemoji_cycle = [
        ("1f4d6", "📖"),
        ("1f4dd", "📝"),
        ("270f-fe0f", "✏️"),
        ("1f4da", "📚"),
        ("1f4d3", "📓"),
        ("1f4c4", "📄"),
        ("1f9e0", "🧠"),
        ("1f3af", "🎯"),
        ("2728", "✨"),
        ("1f31f", "🌟"),
        ("1f4a1", "💡"),
        ("1f50d", "🔍"),
        ("1f465", "👥"),
        ("1f3e2", "🏢"),
        ("1f6e3-fe0f", "🛣️"),
        ("1f4e6", "📦"),
        ("1f4b3", "💳"),
        ("1f4bb", "💻"),
        ("1f4f1", "📱"),
        ("1f310", "🌐"),
    ]

    blocks = []
    for i, row in enumerate(VERBS):
        if len(row) != 17:
            raise SystemExit(f"Bad row length {len(row)} for {row[0]!r}")
        tw_hex, emoji_fb = twemoji_cycle[i % len(twemoji_cycle)]
        idx = 100 + i
        blocks.append(
            slide_html(
                idx,
                101 + i,
                total,
                *row,
                tw_hex,
                emoji_fb,
            )
        )

    text = INDEX.read_text(encoding="utf-8")
    text = text.replace('<input type="number" id="goto-input" min="1" max="100"', f'<input type="number" id="goto-input" min="1" max="{total}"')
    text = text.replace("<title>100 Dutch verbs — study (one card)</title>", f"<title>{total} Dutch verbs — study (one card)</title>")
    text = text.replace("<h1>100 veelvoorkomende werkwoorden</h1>", f"<h1>{total} veelvoorkomende werkwoorden</h1>")

    insert = "\n" + "\n".join(blocks) + "\n"
    marker = "  </div>\n  <script>\n(function() {"
    if marker not in text:
        raise SystemExit("Could not find viewer close before main script")
    text = text.replace(
        marker,
        insert + "  </div>\n  <script>\n(function() {",
        1,
    )

    INDEX.write_text(text, encoding="utf-8")
    print("Patched", INDEX, "— added 100 slides; total", total)


if __name__ == "__main__":
    main()
