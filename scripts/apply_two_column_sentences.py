#!/usr/bin/env python3
"""Rewrite index.html sentence blocks: two columns (VTT + OVT)."""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vtt_manual import VTT_MANUAL  # noqa: E402


def extract_sentences_inner(line: str) -> tuple[str, int, int] | None:
    token = '<div class="sentences">'
    i = line.find(token)
    if i == -1:
        return None
    start = i + len(token)
    depth = 1
    j = start
    while j < len(line) and depth > 0:
        if line[j : j + 4] == "<div" and (j + 4 == len(line) or line[j + 4] in " >"):
            depth += 1
            j = line.find(">", j) + 1
        elif line[j : j + 6] == "</div>":
            depth -= 1
            j += 6
            if depth == 0:
                inner = line[start : j - 6]
                return inner, i, j
        else:
            j += 1
    return None


def extract_sent_boxes(inner: str) -> list[str]:
    boxes: list[str] = []
    pos = 0
    while True:
        p = inner.find('<div class="sent-box">', pos)
        if p == -1:
            break
        i = p + len('<div class="sent-box">')
        depth = 1
        while i < len(inner) and depth > 0:
            if inner[i : i + 4] == "<div" and (i + 4 == len(inner) or inner[i + 4] in " >"):
                depth += 1
                i = inner.find(">", i) + 1
            elif inner[i : i + 6] == "</div>":
                depth -= 1
                i += 6
            else:
                i += 1
        boxes.append(inner[p:i])
        pos = i
    return boxes


def lemma_from_slide(line: str) -> str | None:
    m = re.search(r'<div class="lemma" lang="nl">([^<]+)</div>', line)
    return m.group(1).strip() if m else None


def sent_box_html(label: str, nl: str, en: str, fr: str) -> str:
    return (
        '<div class="sent-box">'
        f'<div class="sent-label">{label}</div>'
        f'<p class="sent-nl" lang="nl">{html.escape(nl)}</p>'
        '<div class="sent-trans">'
        f'<p class="sent-en" lang="en">{html.escape(en)}</p>'
        f'<p class="sent-fr" lang="fr">{html.escape(fr)}</p>'
        "</div></div>"
    )


def build_sentences_two_col(vtt: tuple[str, str, str, str, str, str], ovt_box0: str, ovt_box1: str) -> str:
    sg_nl, sg_en, sg_fr, pl_nl, pl_en, pl_fr = vtt
    vtt0 = sent_box_html("Enkelvoud", sg_nl, sg_en, sg_fr)
    vtt1 = sent_box_html("Meervoud", pl_nl, pl_en, pl_fr)
    return (
        '<div class="sentences sent-two-col">'
        '<div class="sent-col sent-col-vtt">'
        '<div class="sent-col-head">Perfectum (VTT)</div>'
        f"{vtt0}{vtt1}"
        "</div>"
        '<div class="sent-col sent-col-ovt">'
        '<div class="sent-col-head">Imperfectum (OVT)</div>'
        f"{ovt_box0}{ovt_box1}"
        "</div></div>"
    )


def process_line(line: str) -> str:
    if 'class="slide"' not in line or '<div class="sentences">' not in line:
        return line
    lemma = lemma_from_slide(line)
    if not lemma or lemma not in VTT_MANUAL:
        raise SystemExit(f"Missing VTT_MANUAL entry for lemma: {lemma!r}")
    ext = extract_sentences_inner(line)
    if not ext:
        return line
    inner, sent_start, sent_end = ext
    boxes = extract_sent_boxes(inner)
    if len(boxes) != 2:
        raise SystemExit(f"Expected 2 sent-box, got {len(boxes)} for {lemma!r}")
    new_inner = build_sentences_two_col(VTT_MANUAL[lemma], boxes[0], boxes[1])
    return line[:sent_start] + new_inner + line[sent_end:]


def main() -> None:
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    out: list[str] = []
    for line in lines:
        if 'class="slide"' in line and '<div class="sentences">' in line:
            out.append(process_line(line))
        else:
            out.append(line)
    path.write_text("\n".join(out) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
    print("Updated", path)


if __name__ == "__main__":
    main()
