#!/usr/bin/env python3
"""Build top10k/<code>.js — the 10,000 most common words (and short phrases)
of a language, each with an English meaning and an example sentence.

Sources
- Word frequency: hermitdave/FrequencyWords (OpenSubtitles 2018), CC BY-SA 4.0
- Example sentences + their English translations: Tatoeba (tatoeba.org), CC BY 2.0 FR
- Word meanings: Wiktionary (via kaikki.org), CC BY-SA 4.0 — hand corrections
  for the most common words live in OVERRIDES below.

Usage:  python3 scripts/build_top10k.py <cache_dir> nl fr
"""
import bz2
import collections
import gzip
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "top10k")
UA = "Mozilla/5.0 (LokhandLearning study list builder)"
COUNT = 10000

TATOEBA = {"nl": "nld", "fr": "fra"}
WIKT = {"nl": "Dutch", "fr": "French"}
LETTERS = "a-zà-ÿœæ"
TOKEN = re.compile(rf"aujourd'hui|[{LETTERS}]+(?:-[{LETTERS}]+)*'?")

# Subtitle lists contain English interjections and swear words; leave them out.
SKIP = {
    "nl": {"oh", "hey", "okay", "ok", "uh", "um", "hmm", "huh", "wow", "yeah", "yo", "whoa", "oeps",
           "kut", "klootzak", "fuck", "shit", "godverdomme", "kanker", "lul", "teef", "hoer", "neuken"},
    "fr": {"oh", "hey", "okay", "ok", "uh", "um", "hmm", "huh", "wow", "yeah", "yo", "whoa",
           "putain", "merde", "connard", "salope", "enculé", "pute", "bordel", "baiser", "foutre", "con",
           "conne", "fuck", "shit"},
}
SINGLE_LETTERS_OK = {"nl": {"u"}, "fr": {"a", "à", "y"}}
# Real words that are often written with a capital, so the name filter keeps them
CAPITALISED_WORDS = {"god", "dieu", "monsieur", "madame", "mademoiselle", "meneer", "mevrouw"}

# Hand-checked meanings for the most common words, where Wiktionary's first
# meaning isn't the everyday one or is buried in grammar terms.
OVERRIDES = {
    "fr": {
        "c'": "it, that (ce before a vowel)", "j'": "I (je before a vowel)",
        "l'": "the; him, her, it (le/la before a vowel)", "d'": "of, from (de before a vowel)",
        "qu'": "that, what (que before a vowel)", "n'": "not (ne before a vowel)",
        "t'": "you (te before a vowel)", "m'": "me (me before a vowel)",
        "s'": "oneself; if (se/si before a vowel)", "quelqu'": "some (quelque before a vowel)",
        "jusqu'": "until (jusque before a vowel)", "lorsqu'": "when (lorsque before a vowel)",
        "puisqu'": "since (puisque before a vowel)",
        "de": "of, from; some", "je": "I", "pas": "not (ne … pas); step", "le": "the; him, it",
        "que": "that; what; than", "la": "the; her, it", "un": "a, an; one", "à": "to, at, in",
        "il": "he, it", "a": "has (form of avoir, to have)", "ne": "not (ne … pas)",
        "les": "the (plural); them", "en": "in, to, by; of it, some", "ça": "that, it, this",
        "une": "a, an; one (feminine)", "ce": "this, that; it", "des": "some; of the",
        "mais": "but", "tu": "you (informal)", "y": "there; it", "tout": "all, everything; very",
        "fait": "done, made (form of faire); fact", "as": "have (form of avoir: tu as); ace",
        "dit": "said; says (form of dire, to say)", "est-ce": "is it …? (est-ce que = question marker)",
        "lui": "him, her (to him / to her)", "sur": "on, about", "suis": "am (form of être); follow (form of suivre)",
        "va": "goes, go (form of aller, to go)", "vais": "go (je vais, form of aller); going to",
        "peux": "can (form of pouvoir)", "peut": "can (form of pouvoir)", "faut": "must, it is necessary (il faut)",
        "été": "been (form of être); summer", "fais": "do, make (form of faire)", "aussi": "also, too",
        "vu": "seen (form of voir)", "veut": "wants (form of vouloir)", "sont": "are (form of être)",
        "avez": "have (vous avez, form of avoir)", "ont": "have (ils ont, form of avoir)", "ai": "have (j'ai, form of avoir)",
        "sais": "know (je sais / tu sais, form of savoir)", "allez": "go (vous allez, form of aller); come on!",
        "êtes": "are (vous êtes, form of être)", "sommes": "are (nous sommes, form of être)",
        "avons": "have (nous avons, form of avoir)", "es": "are (tu es, form of être)",
        "était": "was (form of être)", "étais": "was (form of être)", "avait": "had (form of avoir)",
        "fût": "were (form of être)", "bon": "good; well, OK", "bien": "well, good; really",
        "alors": "so, then", "plus": "more; no longer (ne … plus)", "rien": "nothing",
        "très": "very", "ici": "here", "là": "there; here", "comme": "like, as", "toujours": "always; still",
        "encore": "again; still; more", "juste": "just; fair, right", "vraiment": "really", "même": "same; even",
        "dois": "must (form of devoir)", "doit": "must (form of devoir)", "vas": "go (tu vas, form of aller)",
        "vient": "comes (form of venir)", "viens": "come (form of venir)", "parce": "because (parce que)",
        "si": "if; so; yes (to a negative question)", "quand": "when", "merci": "thank you",
        "oui": "yes", "non": "no", "on": "we; one, people", "mal": "bad, badly; pain",
        "mien": "mine (le mien)", "mienne": "mine (la mienne)", "miens": "mine (les miens)", "miennes": "mine (les miennes)",
        "tien": "yours (le tien)", "tienne": "yours (la tienne)", "sien": "his, hers (le sien)", "sienne": "his, hers (la sienne)",
        "siens": "his, hers (les siens)", "nôtre": "ours (le/la nôtre)", "nôtres": "ours (les nôtres)",
        "vôtre": "yours (le/la vôtre)", "vôtres": "yours (les vôtres)", "auprès": "near, next to (auprès de)",
        "accord": "agreement; OK (d'accord)", "son": "his, her, its; sound", "hé": "hey!",
        "désolé": "sorry", "désolée": "sorry (feminine)", "bonne": "good (feminine of bon); maid",
        "gens": "people", "coup": "blow, hit; go, time (un coup); (a) drink", "du": "some; of the (de + le)",
        "partie": "part; game, match; party", "dû": "had to (form of devoir); due", "devrais": "should (form of devoir)",
        "devrait": "should (form of devoir)", "pu": "been able to (form of pouvoir)",
    },
    "nl": {
        "ik": "I", "je": "you (informal); your", "het": "the (neuter); it", "de": "the",
        "dat": "that", "is": "is (form of zijn, to be)", "een": "a, an; one", "niet": "not",
        "en": "and", "van": "of, from", "wat": "what; something", "we": "we", "in": "in, into",
        "ze": "they, them; she, her", "hij": "he", "te": "to; too (too much)",
        "zijn": "to be; his, its", "op": "on, up", "maar": "but; just", "er": "there; of it (often not translated)",
        "met": "with", "voor": "for; before; in front of", "die": "that, those; who, which",
        "heb": "have (form of hebben)", "me": "me, myself", "als": "if, when; as, like",
        "was": "was (form of zijn); laundry", "ben": "am, are (form of zijn)", "om": "to, in order to; at; around",
        "dit": "this", "mijn": "my", "aan": "on, at, to", "u": "you (polite)", "dan": "then; than",
        "naar": "to, towards", "weet": "know (form of weten)", "hier": "here", "zo": "so, like this; soon",
        "jij": "you (informal, stressed)", "kan": "can (form of kunnen)", "geen": "no, not a, not any",
        "nog": "still, yet; more", "ja": "yes", "hem": "him", "heeft": "has (form of hebben)",
        "wel": "certainly, indeed (adds emphasis); well", "moet": "must, have to (form of moeten)",
        "wil": "want (form of willen)", "hebben": "to have", "goed": "good; well; right",
        "haar": "her; hair", "nee": "no", "hoe": "how", "nu": "now", "waar": "where; true",
        "over": "about; over", "ook": "also, too", "doen": "to do", "uit": "out, from; off",
        "zou": "would, should (form of zullen)", "ga": "go (form of gaan)", "of": "or; whether, if",
        "gaan": "to go", "bent": "are (form of zijn)", "mij": "me", "bij": "at, near, with",
        "al": "already; all", "ons": "us; our", "had": "had (form of hebben)", "iets": "something; a little",
        "kunnen": "can, to be able to", "kom": "come (form of komen)", "zal": "will, shall (form of zullen)",
        "daar": "there", "toch": "still, yet; after all, right?", "zei": "said (form of zeggen)",
        "zij": "she; they", "jou": "you (informal, object)", "doe": "do (form of doen)", "gaat": "goes (form of gaan)",
        "laat": "let (form of laten); late", "mag": "may, can (form of mogen)", "kun": "can (form of kunnen)",
        "dus": "so, therefore", "meer": "more; lake", "jullie": "you (plural); your", "alles": "everything",
        "wie": "who", "waarom": "why", "even": "just, for a moment; even (numbers)", "echt": "real, really",
        "heel": "very; whole", "nooit": "never", "wordt": "becomes, is (form of worden)", "komt": "comes (form of komen)",
        "denk": "think (form of denken)", "weg": "away, gone; road, way", "moeten": "must, to have to",
        "zien": "to see", "hebt": "have (form of hebben)", "wilt": "want (form of willen)", "mee": "along, with (me)",
        "werd": "became, was (form of worden)", "gewoon": "just, simply; normal", "misschien": "maybe, perhaps",
        "willen": "to want", "kijk": "look (form of kijken)", "terug": "back", "heen": "away, there (to)",
        "stond": "stood (form of staan)", "ziens": "tot ziens = goodbye", "nachts": "'s nachts = at night",
        "avonds": "'s avonds = in the evening", "morgens": "'s morgens = in the morning",
        "ochtends": "'s ochtends = in the morning", "middags": "'s middags = in the afternoon",
        "alsjeblief": "please; here you are (informal)", "alstublieft": "please; here you are (polite)",
        "okee": "okay", "ofzo": "or something (of zo)", "leve": "long live …!", "bestwil": "for your own good (voor je eigen bestwil)",
        "dusver": "so far (tot dusver)", "voorschijn": "out, into view (tevoorschijn)", "opzichte": "with regard to (ten opzichte van)",
        "slotte": "finally (ten slotte)", "weldra": "soon", "aldoor": "all the time",
        "net": "just, just now; neat, decent; net", "dood": "dead; death", "mensen": "people (plural of mens)",
        "dingen": "things (plural of ding)", "kinderen": "children (plural of kind)",
        "wilde": "wanted (past of willen); wild", "keer": "time (een keer = once); turn (form of keren)",
    },
}

PRONOUNS = {"moi": "me", "toi": "you, yourself", "lui": "him, her", "le": "it, him", "la": "it, her", "les": "them",
            "nous": "us, we", "vous": "you", "leur": "them", "en": "some, of it", "y": "there", "je": "I",
            "tu": "you", "il": "he, it", "elle": "she, it", "on": "we, one", "ils": "they", "elles": "they", "ce": "it, that"}
SUBJECTS = {"je", "tu", "il", "elle", "on", "ils", "elles", "ce"}
OBJECTS = {"moi", "toi", "lui", "le", "la", "les", "leur", "en", "y"}
SKIP_TAGS = {"obsolete", "archaic", "dated", "rare", "historical", "nonstandard", "misspelling"}
GRAMMAR = re.compile(r"\b(person|pronoun|article|determiner|possessive|subjective|objective|singular|plural)\b", re.I)


def fetch(url, path):
    if not os.path.exists(path):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=300) as r, open(path, "wb") as f:
            f.write(r.read())
    return path


def load_sentences(cache, lang):
    """{id: text} for the language, plus (sentence, English translation) pairs."""
    code = TATOEBA[lang]
    base = "https://downloads.tatoeba.org/exports/per_language"
    def read(name, url):
        return bz2.open(fetch(url, os.path.join(cache, name)), "rt", encoding="utf-8")
    src = {}
    for line in read(f"{code}_sentences.tsv.bz2", f"{base}/{code}/{code}_sentences.tsv.bz2"):
        sid, _, text = line.rstrip("\n").split("\t", 2)
        src[sid] = text
    links = collections.defaultdict(list)
    for line in read(f"{code}-eng_links.tsv.bz2", f"{base}/{code}/{code}-eng_links.tsv.bz2"):
        a, b = line.split()
        links[a].append(b)
    wanted = {e for ids in links.values() for e in ids}
    eng = {}
    for line in read("eng_sentences.tsv.bz2", f"{base}/eng/eng_sentences.tsv.bz2"):
        sid, _, text = line.rstrip("\n").split("\t", 2)
        if sid in wanted:
            eng[sid] = text
    pairs = []
    for sid, text in src.items():
        en = sorted((eng[e] for e in links.get(sid, []) if e in eng), key=len)
        if en:
            pairs.append((text, en[0]))
    return src, pairs


def tokens(text):
    return TOKEN.findall(text.lower().replace("’", "'"))


def corpus_stats(src):
    """Token counts, and mid-sentence capitalised vs lowercase counts (to spot names)."""
    seen = collections.Counter()
    upper_mid = collections.Counter()
    lower_mid = collections.Counter()
    for text in src.values():
        words = re.findall(rf"[{LETTERS}A-ZÀ-ÝŒÆ'’-]+", text)
        for i, w in enumerate(words):
            low = w.lower()
            for t in tokens(low):
                seen[t] += 1
            if i > 0:
                (upper_mid if w[0].isupper() else lower_mid)[low] += 1
    return seen, upper_mid, lower_mid


def candidates(cache, lang, seen, upper_mid, lower_mid):
    path = fetch(f"https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/{lang}/{lang}_50k.txt",
                 os.path.join(cache, f"{lang}_50k.txt"))
    out, have = [], set()
    for line in open(path, encoding="utf-8"):
        w = line.split(" ")[0].strip()
        if not re.fullmatch(rf"[{LETTERS}]+(?:['-][{LETTERS}]+)*'?", w) or "-t'" in w:
            continue
        if len(w.strip("'")) == 1 and w not in SINGLE_LETTERS_OK[lang]:
            continue
        if w in SKIP[lang] or w in have:
            continue
        if seen[w] == 0 and w not in OVERRIDES[lang]:
            continue                                  # not real target-language text (typos, English, mojibake)
        if upper_mid[w] >= 2 and upper_mid[w] > 3 * lower_mid[w] and w not in CAPITALISED_WORDS:
            continue                                  # nearly always written with a capital: a name
        out.append(w)
        have.add(w)
        if len(out) == COUNT + 4000:
            break
    return out


# ── Meanings from Wiktionary ─────────────────────────────────────────────────

def load_wiktionary(cache, lang):
    """{word: [entries]}, plus {inflected form: base word} from the entries' form tables
    (Dutch adjective forms like 'brave' only appear under 'braaf')."""
    name = WIKT[lang]
    path = fetch(f"https://kaikki.org/dictionary/{name}/kaikki.org-dictionary-{name}.jsonl.gz",
                 os.path.join(cache, f"wikt-{name}.jsonl.gz"))
    entries = collections.defaultdict(list)
    form_of = {}
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            e = json.loads(line)
            w = e.get("word", "")
            if not w or w != w.lower():
                continue
            entries[w].append(e)
            for form in e.get("forms", []):
                fw = form.get("form", "")
                if fw and fw != w and " " not in fw and fw not in form_of and "table-tags" not in form.get("tags", []):
                    form_of[fw] = w
    return entries, form_of


def _senses(entries, word):
    for e in entries.get(word, []):
        for sense in e.get("senses", []):
            glosses = sense.get("glosses") or []
            if glosses:
                yield sense, glosses


def _short(gloss):
    """Drop grammar descriptions: 'it; third-person singular neuter pronoun' → 'it'."""
    parts = [p.strip() for p in gloss.split(";")]
    keep = [p for p in parts if not GRAMMAR.search(p)] or parts[:1]
    return "; ".join(keep).strip().rstrip(".")


def _lemma_meaning(entries, lemma, pos=None):
    """First everyday meaning of a base word; with pos, prefer that part of speech
    (a form of the verb devoir means "must", not the noun "duty")."""
    best = ""
    ordered = sorted(entries.get(lemma, []), key=lambda e: e.get("pos") != pos) if pos else entries.get(lemma, [])
    for e in ordered:
        for sense in e.get("senses", []):
            glosses = sense.get("glosses")
            if not glosses or sense.get("form_of") or sense.get("alt_of"):
                continue
            m = _short(glosses[-1]).split(",")[0].split(";")[0].strip()
            if m.count("(") != m.count(")"):            # cut off a half-open bracket left by the split
                m = m.split("(")[0].strip() if m.count("(") > m.count(")") else m.replace(")", "").strip()
            if not SKIP_TAGS & set(sense.get("tags", [])):
                return m
            best = best or m
    return best


def _is_letter_name(g):
    return bool(re.search(r"\bletter\b|\balphabet\b|Latin script", g))


def gloss(word, entries, rank):
    forms, verb_forms, plain, minor = {}, set(), [], []
    senses = [(e.get("pos"), s, s.get("glosses")) for e in entries.get(word, []) for s in e.get("senses", []) if s.get("glosses")]
    for pos, sense, glosses in senses:
        old = bool(SKIP_TAGS & set(sense.get("tags", [])))
        if sense.get("form_of") and not old:
            lemma = sense["form_of"][0].get("word", "")
            if lemma in forms:
                continue
            if pos == "verb":
                verb_forms.add(lemma)
            detail = glosses[-1]
            detail = re.sub(r"\s*of\s+" + re.escape(lemma) + r"\b.*$", "", detail).strip(" :")
            detail = (detail.replace("first-person", "1st person").replace("second-person", "2nd person")
                      .replace("third-person", "3rd person").replace(" indicative", ""))
            meaning = _lemma_meaning(entries, lemma, pos)
            forms[lemma] = (f"form of {lemma}" + (f" ({meaning})" if meaning else "")
                            + (f" — {detail}" if detail and "inflection" not in detail else ""))
        elif sense.get("alt_of") and not plain:
            target = sense["alt_of"][0].get("word", "")
            m = _lemma_meaning(entries, target)
            minor.append(f"{m} (usually written {target})" if m else _short(glosses[-1]))
        elif not sense.get("form_of"):
            g = _short(glosses[-1])
            (minor if old or sense.get("alt_of") or _is_letter_name(g) or g.startswith("Used ") else plain).append(g)
    # A form of a common verb usually beats the word's own rarer meaning (est → être, not "east"),
    # but a noun or adjective form doesn't (laten is "to let", not the plural of laat)
    own = rank.get(word, 10 ** 6)
    first = {l for l in forms if l in verb_forms and rank.get(l, 10 ** 6) < 1500}
    common = [t for l, t in forms.items() if l in first]
    rare = [t for l, t in forms.items() if l not in first]
    out = []
    for t in common + plain + rare + minor:
        t = re.sub(r"\s+", " ", t).strip()
        if len(t) > 80:
            t = t[:77].rsplit(" ", 1)[0] + "…"
        if t and t not in out:
            out.append(t)
        if len(out) == 3:
            break
    return "; ".join(out)


def _part(entries, rank, w):
    if w in PRONOUNS:
        return f"{w} ({PRONOUNS[w]})"
    for sense, glosses in _senses(entries, w):
        if sense.get("form_of"):
            lemma = sense["form_of"][0].get("word", "")
            meaning = _lemma_meaning(entries, lemma)
            return f"{lemma} ({meaning})" if meaning else lemma
    m = _lemma_meaning(entries, w)
    return f"{w} ({m})" if m else ""


def phrase_gloss(word, entries, rank):
    """French inverted questions and commands: 'avez-vous' → 'avoir (to have) + vous (you) · question form'."""
    parts = [p for p in word.split("-") if p != "t"]
    if len(parts) < 2:
        return ""
    glossed = [_part(entries, rank, p) for p in parts]
    if not all(glossed):
        return ""
    last = parts[-1]
    kind = (" · question form" if last in SUBJECTS else " · command form" if last in OBJECTS
            else " · question or command form" if last in ("nous", "vous") else "")
    return " + ".join(glossed) + kind


def variants(word, lang):
    yield word
    if lang == "fr":
        yield word.replace("oe", "œ")
        if word.startswith("e"):
            yield "é" + word[1:]
    else:
        yield word.replace("eén", "één")
        yield word.translate(str.maketrans("áéíóú", "aeiou"))   # stressed spellings: vóór, écht, wél


def meaning(word, lang, wikt, rank):
    entries, form_of = wikt
    if word in OVERRIDES[lang]:
        return OVERRIDES[lang][word]
    for v in variants(word, lang):
        g = gloss(v, entries, rank)
        if not g and v in form_of:
            base = form_of[v]
            m = _lemma_meaning(entries, base)
            g = f"form of {base}" + (f" ({m})" if m else "")
        if g:
            if v == word:
                return g
            return f"{g} (stressed form)" if lang == "nl" and "één" not in v else f"{g} (usually written {v})"
    return phrase_gloss(word, entries, rank) if "-" in word else ""


def pick_examples(words, pairs):
    rank = {w: i for i, w in enumerate(words)}
    index = collections.defaultdict(list)
    toks = []
    for n, (text, _) in enumerate(pairs):
        t = tokens(text)
        toks.append(t)
        if 3 <= len(t) <= 12:
            for w in set(t):
                if w in rank:
                    index[w].append(n)
    used = collections.Counter()
    out = {}
    for w in words:
        best, best_score = None, None
        for n in index.get(w, ()):
            t = toks[n]
            hard = sum(1 for x in t if rank.get(x, COUNT) > max(2000, rank[w] + 500))
            score = abs(len(t) - 6) + 3 * hard + 4 * used[n]
            if best_score is None or score < best_score:
                best, best_score = n, score
        if best is not None:
            used[best] += 1
            out[w] = pairs[best]
    return out


def main():
    cache = sys.argv[1]
    os.makedirs(OUT, exist_ok=True)
    for lang in sys.argv[2:] or ["nl", "fr"]:
        src, pairs = load_sentences(cache, lang)
        seen, upper_mid, lower_mid = corpus_stats(src)
        cands = candidates(cache, lang, seen, upper_mid, lower_mid)
        wikt = load_wiktionary(cache, lang)
        rank = {w: i for i, w in enumerate(cands)}
        words, meanings, dropped = [], {}, []
        for w in cands:
            m = meaning(w, lang, wikt, rank)
            if not m:
                dropped.append(w)              # no dictionary entry: names, English, typos
                continue
            words.append(w)
            meanings[w] = m
            if len(words) == COUNT:
                break
        examples = pick_examples(words, pairs)
        items = [[w, meanings[w]] + list(examples.get(w, ())) for w in words]
        path = os.path.join(OUT, f"{lang}.js")
        with open(path, "w", encoding="utf-8") as f:
            f.write("// 10,000 most common words — generated by scripts/build_top10k.py\n")
            f.write("// [word, English meaning, example sentence, example English]\n")
            f.write("window.TOP10K = ")
            json.dump(items, f, ensure_ascii=False, separators=(",", ":"))
            f.write(";\n")
        with_ex = sum(1 for x in items if len(x) == 4)
        print(f"{lang}: {len(items)} words, {with_ex} with example sentences; "
              f"dropped {len(dropped)} without a dictionary entry, e.g. {' '.join(dropped[:25])}")


if __name__ == "__main__":
    main()
