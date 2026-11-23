#!/usr/bin/env python3
"""Build lang/<code>_stories.js — public domain stories for the extra languages.

Sources: Project Gutenberg (via the pglaf.org mirror), Aozora Bunko (Japanese)
and Wikisource (Russian, Korean — Gutenberg has almost nothing in those).

Usage:  python3 scripts/build_lang_stories.py <cache_dir>
Downloads are cached in <cache_dir> so re-running is fast.
"""
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "lang")
UA = "LokhandLearning/1.0 (free language study site)"


# ── Downloading ──────────────────────────────────────────────────────────────

def fetch(url, cache, name):
    path = os.path.join(cache, name)
    if not os.path.exists(path):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
        with open(path, "wb") as f:
            f.write(data)
    with open(path, "rb") as f:
        return f.read()


def gutenberg(book_id, cache):
    s = str(book_id)
    base = "https://gutenberg.pglaf.org/" + "/".join(s[:-1]) + f"/{s}/"
    listing = fetch(base, cache, f"pg{s}_index.html").decode("utf-8", "replace")
    files = sorted(set(re.findall(rf'href="({s}(?:-0|-8)?\.txt)"', listing)))
    name = files[0]
    raw = fetch(base + name, cache, f"pg{s}.txt")
    text = raw.decode("utf-8-sig") if not name.endswith("-8.txt") else raw.decode("latin-1")
    return text.replace("\r\n", "\n")


def wikisource(wiki, title, cache):
    q = urllib.parse.urlencode({"action": "parse", "page": title, "prop": "text",
                                "format": "json", "formatversion": "2"})
    raw = fetch(f"https://{wiki}.wikisource.org/w/api.php?{q}", cache,
                f"ws_{wiki}_{abs(hash(title)) % 10**8}_{len(title)}.json")
    return json.loads(raw)["parse"]["text"]


# ── Text helpers ─────────────────────────────────────────────────────────────

def lines_between(text, start, end_pred):
    """Lines after the heading `start` (an exact stripped line, first match after
    the table of contents is skipped by `skip`), until end_pred(line) is true."""
    lines = text.split("\n")
    out = []
    for i, ln in enumerate(lines[start:], start):
        if i > start and end_pred(ln):
            break
        out.append(ln)
    return out[1:]


def find_line(text, heading, after=0):
    for i, ln in enumerate(text.split("\n")):
        if i >= after and ln.strip().rstrip(".") == heading:
            return i
    raise ValueError(f"heading not found: {heading}")


def blank_line_paras(lines):
    """Latin-script Gutenberg text: paragraphs separated by blank lines."""
    paras, cur = [], []
    for ln in lines + [""]:
        if ln.strip():
            cur.append(ln.strip())
        elif cur:
            paras.append(" ".join(cur))
            cur = []
    clean = []
    for p in paras:
        p = re.sub(r"_([^_]+)_", r"\1", p)        # _italics_
        p = p.replace("--", "—")
        p = re.sub(r"\[\d+\]", "", p)              # footnote markers
        clean.append(p.strip())
    return [p for p in clean if p]


def cjk_paras(lines, width):
    """CJK text hard-wrapped at `width` chars: a short line ends a paragraph."""
    paras, cur = [], ""
    for ln in lines:
        s = ln.strip().lstrip("　")
        if not s:
            continue
        cur += s
        if len(ln.strip()) < width - 2:
            paras.append(cur)
            cur = ""
    if cur:
        paras.append(cur)
    return paras


class _Collect(HTMLParser):
    """Collect paragraph text from HTML, dropping ruby readings and footnotes."""

    def __init__(self, para_tags, skip_classes=()):
        super().__init__()
        self.para_tags = para_tags
        self.skip_classes = skip_classes
        self.paras, self.buf = [], []
        self.skip = 0
        self.stack = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class", "") or ""
        skipping = tag in ("rt", "rp", "sup", "style", "script") or any(c in cls for c in self.skip_classes)
        if tag in ("br",):
            if "br" in self.para_tags:
                self.flush()
            return
        self.stack.append(skipping)
        if skipping:
            self.skip += 1
        if tag in self.para_tags:
            self.flush()

    def handle_endtag(self, tag):
        if tag == "br":
            return
        if self.stack:
            if self.stack.pop():
                self.skip -= 1
        if tag in self.para_tags:
            self.flush()

    def handle_data(self, data):
        if not self.skip:
            self.buf.append(data)

    def flush(self):
        t = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        if t:
            self.paras.append(t)
        self.buf = []


def html_paras(markup, para_tags=("p",), skip_classes=()):
    c = _Collect(set(para_tags), skip_classes)
    c.feed(markup)
    c.flush()
    return c.paras


# ── Per-language builders ────────────────────────────────────────────────────

def build_fr(cache):
    t = gutenberg(15626, cache)
    src = "Contes et historiettes à l'usage des jeunes enfants — Zulma Carraud (1853)"
    picks = [
        ("L'IMPRUDENCE", "A little girl learns why her mother's warnings matter."),
        ("LA MOUCHE", "A child discovers that even a small fly deserves kindness."),
        ("LA PARESSE", "A lazy morning teaches a lesson about effort."),
        ("LE LOUP", "A shepherd boy, a wolf and a lesson about telling the truth."),
        ("LE SERIN", "A pet canary and the responsibility of caring for it."),
        ("LE FEU", "Why children should never play with fire."),
        ("LA PETITE MAMAN", "A girl takes care of her little brother like a grown-up."),
        ("LE PETIT AGNEAU", "A child and a little lamb in the countryside."),
        ("LA PETITE GOURMANDE", "A greedy little girl learns to share."),
        ("LES TARTELETTES", "A story about tarts, temptation and honesty."),
    ]
    heads = [p[0] for p in picks] + ["LA PETITE CURIEUSE"]
    start_at = find_line(t, "L'IMPRUDENCE")
    out = []
    for title, desc in picks:
        i = find_line(t, title, start_at)
        body = lines_between(t, i, lambda ln: ln.strip().rstrip(".") in heads or re.fullmatch(r"[A-ZÉÈ' -]{6,}\.?", ln.strip() or "x") is not None)
        out.append(story(title.capitalize(), desc, src, blank_line_paras(body)))
    return out


def build_es(cache):
    t = gutenberg(19898, cache)
    src = "La Edad de Oro — José Martí (1889)"
    picks = [
        ("Meñique", "A clever little boy outwits a giant with magic tools he finds in the mountains."),
        ("Bebé y el señor don Pomposo", "Little Bebé shares a gift with his poor cousin, to the annoyance of a pompous uncle."),
        ("Nené traviesa", "Curious Nené tears a precious book while trying to help her father."),
        ("La muñeca negra", "Piedad's birthday — and the old black doll she loves more than any new present."),
        ("Los dos ruiseñores", "An emperor, a mechanical nightingale and a real one (after Andersen)."),
    ]
    toc = t.split("\n")[find_line(t, "Tres héroes"):]
    titles = set()
    for ln in toc:                       # table of contents, until the "* * *" line
        if "*" in ln:
            break
        if ln.strip():
            titles.add(ln.strip())
    body_start = find_line(t, "Tres héroes", 100)
    out = []
    for title, desc in picks:
        i = find_line(t, title, body_start)
        body = lines_between(t, i, lambda ln: ln.strip() in titles or "END OF TH" in ln)
        paras = [p for p in blank_line_paras(body) if not p.startswith("Cuento de magia")]
        out.append(story(title, desc, src, paras))
    return out


def build_it(cache):
    t = gutenberg(52484, cache)
    src = "Le avventure di Pinocchio — Carlo Collodi (1883)"
    descs = [
        "Mastro Ciliegia finds a piece of wood that laughs and cries like a child.",
        "Geppetto receives the talking piece of wood and decides to make a puppet.",
        "Geppetto carves Pinocchio, who starts causing mischief straight away.",
        "Pinocchio meets the Talking Cricket — and does not like its advice.",
        "Hungry Pinocchio finds an egg, but the egg flies away.",
        "Pinocchio falls asleep with his feet on the stove.",
    ]
    numerals = ["I", "II", "III", "IV", "V", "VI", "VII"]
    out = []
    for n, desc in enumerate(descs):
        i = find_line(t, numerals[n], 30)
        body = lines_between(t, i, lambda ln: ln.strip() == numerals[n + 1] + ".")
        paras = blank_line_paras(body)
        summary = paras.pop(0) if paras else ""
        out.append(story(f"Capitolo {numerals[n]}", summary or desc, src, paras, en=desc))
    return out


def build_zh(cache):
    t = gutenberg(27166, cache)
    src = "吶喊 (Call to Arms) — 魯迅 Lu Xun (1923)"
    picks = [
        ("一件小事", "A small incident with a rickshaw puller changes how the narrator sees himself."),
        ("孔乙己", "A poor scholar who drinks at a village tavern and is laughed at by everyone."),
        ("故鄉", "The narrator returns to his hometown and meets his childhood friend Runtu."),
        ("鴨的喜劇", "A blind Russian poet, tadpoles and ducklings in a Beijing courtyard."),
    ]
    title_line = re.compile(r"^ ?[^\s，。、：；“”？！]{2,10}$")
    out = []
    for title, desc in picks:
        i = find_line(t, title, 200)
        body = lines_between(t, i, lambda ln: bool(title_line.match(ln)) or "注釋" in ln or "START OF" in ln or "End of" in ln)
        paras = [re.sub(r"[ぁ-ん]", "", p) for p in cjk_paras(body, 38)]   # footnote markers
        out.append(story(title, desc, src, paras))
    return out


def build_ja(cache):
    out = []
    t = gutenberg(1982, cache)
    i = find_line(t, "芥川龍之介")
    body = lines_between(t, i, lambda ln: "END OF" in ln.upper())
    paras = cjk_paras(body, 40)
    paras = [re.sub(r"\([ぁ-んァ-ヶー]+\)", "", p) for p in paras]   # digitizer's readings
    out.append(story("羅生門", "A servant sheltering from the rain at Kyoto's ruined Rashōmon gate faces a choice.",
                     "羅生門 Rashōmon — 芥川龍之介 Akutagawa Ryūnosuke (1915) · Project Gutenberg", paras))
    aozora = [
        ("000879/files/92_14545.html", "蜘蛛の糸", "The Buddha lowers a spider's thread to a robber in hell.",
         "蜘蛛の糸 — 芥川龍之介 Akutagawa Ryūnosuke (1918)"),
        ("000121/files/628_14895.html", "ごん狐", "Gon, a mischievous little fox, tries to make up for a prank.",
         "ごん狐 — 新美南吉 Niimi Nankichi (1932)"),
        ("000081/files/43754_17659.html", "注文の多い料理店", "Two hunters find a strange restaurant in the mountains with many requests.",
         "注文の多い料理店 — 宮沢賢治 Miyazawa Kenji (1924)"),
    ]
    for path, title, desc, src in aozora:
        raw = fetch("https://www.aozora.gr.jp/cards/" + path, cache, "aoz_" + path.split("/")[-1])
        doc = raw.decode("shift_jis", "replace")
        main = doc.split('<div class="main_text">', 1)[1].split('<div class="bibliographical_information">', 1)[0]
        lines = html_paras(main, para_tags=("br", "div", "h3", "h4"), skip_classes=("notes",))
        paras = [ln.lstrip("　 ") for ln in lines if ln.strip() and not re.fullmatch(r"[一二三四五六七八九十]+", ln.strip(" 　"))]
        out.append(story(title, desc, src + " · Aozora Bunko", paras))
    return out


def build_ru(cache):
    src_book = "Л. Н. Толстой — рассказы для детей (1870-е) · Wikisource"
    picks = [
        ("Филипок (Толстой)", "Филипок", "Little Filipok really wants to go to school with the big children."),
        ("Лев и собачка (Толстой)", "Лев и собачка", "A little dog is thrown into a lion's cage — and they become friends."),
        ("Прыжок (Толстой)", "Прыжок", "A monkey steals a boy's hat on a ship and he climbs the mast after it."),
        ("Корова (Толстой)", "Корова", "A boy breaks a glass, stays silent, and the family's cow pays the price."),
        ("Два брата и золото (Толстой)", "Два брата и золото", "Two brothers find gold — and must decide what to do with it."),
    ]
    out = []
    for page, title, desc in picks:
        paras = html_paras(wikisource("ru", page, cache), skip_classes=("reference", "noprint", "mw-editsection", "ws-noexport", "header"))
        paras = [p for p in paras if len(p) > 1 and not p.startswith("←") and "Толстой" not in p[:20]]
        paras = until(paras, "Примечания")
        out.append(story(title, desc, src_book, paras))
    return out


def build_ko(cache):
    picks = [
        ("만년 셔츠", "만년 셔츠", "Changnam, a cheerful poor boy, gives away his clothes to help others.",
         "만년 셔츠 — 방정환 Bang Jeong-hwan (1927) · Wikisource"),
        ("운수 좋은 날", "운수 좋은 날", "A rickshaw puller has his luckiest day ever — while his wife lies ill at home.",
         "운수 좋은 날 — 현진건 Hyeon Jin-geon (1924) · Wikisource"),
        ("감자", "감자", "Bok-nyeo's life changes after poverty drives her family to the edge of Pyongyang.",
         "감자 — 김동인 Kim Dong-in (1925) · Wikisource"),
    ]
    out = []
    for page, title, desc, src in picks:
        paras = html_paras(wikisource("ko", page, cache), para_tags=("p", "dd", "br"),
                           skip_classes=("reference", "noprint", "mw-editsection", "ws-noexport", "header", "licenseContainer"))
        paras = [p for p in until(paras, "라이선스") if len(p) > 1 and "저작권" not in p and "퍼블릭 도메인" not in p and p != "🙝🙟"]
        out.append(story(title, desc, src, paras))
    return out


def until(paras, marker):
    return paras[:paras.index(marker)] if marker in paras else paras


def story(title, desc, source, paras, en=None):
    paras = [html.unescape(p) for p in paras if p.strip()]
    if not paras:
        raise ValueError(f"empty story: {title}")
    return {"title": title, "desc": desc, "source": source, "paras": paras}


BUILDERS = {"fr": build_fr, "es": build_es, "it": build_it, "ru": build_ru,
            "zh": build_zh, "ja": build_ja, "ko": build_ko}


def main():
    cache = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, ".cache")
    os.makedirs(cache, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[2:] or list(BUILDERS)
    for code in only:
        stories = BUILDERS[code](cache)
        path = os.path.join(OUT, f"{code}_stories.js")
        with open(path, "w", encoding="utf-8") as f:
            f.write("// Public domain stories — generated by scripts/build_lang_stories.py\n")
            f.write("const LANG_STORIES = ")
            json.dump(stories, f, ensure_ascii=False, indent=1)
            f.write(";\n")
        sizes = ", ".join(f"{s['title']}({len(s['paras'])}p)" for s in stories)
        print(f"{code}: {len(stories)} stories → {os.path.relpath(path, ROOT)}  [{sizes}]")


if __name__ == "__main__":
    main()
