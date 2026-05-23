#!/usr/bin/env python3
"""
Wablieft Article Fetcher
Logs into wablieft.be and downloads full article content for all sections.
Requires a paid wablieft.be subscription.

Setup:
  1. Create a .env file in this folder:
       WABLIEFT_EMAIL=your@email.com
       WABLIEFT_PASSWORD=yourpassword
  2. pip install requests beautifulsoup4 python-dotenv
  3. python fetch_wablieft.py

Re-run whenever you want fresh articles.
"""

import os
import sys
import json
import time
import re
from datetime import datetime

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit(
        "Missing dependencies. Run:\n"
        "  pip install requests beautifulsoup4 python-dotenv"
    )

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # fine if python-dotenv not installed and vars set another way

BASE_URL = "https://wablieft.be"

SECTIONS = [
    ("buitenland", "Wereld"),
    ("binnenland", "België"),
    ("sport",      "Sport"),
    ("interview",  "Interview"),
    ("blog",       "Blog"),
    ("mening",     "Mening"),
    ("leuk",       "Leuk"),
    ("ster",       "Ster"),
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "nl-BE,nl;q=0.9,en;q=0.8",
}


# ── Credentials ────────────────────────────────────────────────────────────────

def get_credentials():
    email    = os.environ.get("WABLIEFT_EMAIL", "").strip()
    password = os.environ.get("WABLIEFT_PASSWORD", "").strip()
    if not email or not password:
        sys.exit(
            "\nError: missing credentials.\n"
            "Create a .env file in this folder with:\n\n"
            "  WABLIEFT_EMAIL=your@email.com\n"
            "  WABLIEFT_PASSWORD=yourpassword\n"
        )
    return email, password


# ── Login ───────────────────────────────────────────────────────────────────────

def login(session, email, password):
    print("Logging in to wablieft.be …")
    r = session.get(f"{BASE_URL}/user/login", timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    # Find the login form (Drupal uses different ids across versions)
    form = (
        soup.find("form", id="user-login-form")
        or soup.find("form", id="user-login")
        or soup.find("form", attrs={"action": re.compile(r"login")})
        or soup.find("form")
    )

    # Start with all hidden fields from the form
    data = {}
    if form:
        for inp in form.find_all("input"):
            n = inp.get("name")
            v = inp.get("value", "")
            if n:
                data[n] = v

    data["name"] = email
    data["pass"] = password
    data["op"]   = "Log in"

    r2 = session.post(
        f"{BASE_URL}/user/login",
        data=data,
        allow_redirects=True,
        timeout=20,
    )

    # Still on login page → credentials rejected
    if "/user/login" in r2.url:
        sys.exit(
            "\nLogin failed — please check your credentials in the .env file.\n"
        )

    print("  ✓ Logged in successfully!\n")


# ── Article list ────────────────────────────────────────────────────────────────

def get_article_links(session, section_key):
    url = f"{BASE_URL}/nl/krant/{section_key}"
    r = session.get(url, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    prefix = f"/nl/krant/{section_key}/"
    seen, links = set(), []

    for a in soup.find_all("a", href=True):
        href = a["href"]
        # Normalise to a path
        if href.startswith("http"):
            href = re.sub(r"^https?://wablieft\.be", "", href)
        if not href.startswith("/"):
            href = "/" + href

        if href.startswith(prefix) and href not in seen:
            seen.add(href)
            title = a.get_text(" ", strip=True)
            if len(title) > 3:
                links.append({"slug": href, "title": title})

    return links


# ── Article content ─────────────────────────────────────────────────────────────

def parse_article(soup):
    # Title from <h1>
    title = ""
    h1 = soup.find("h1")
    if h1:
        title = h1.get_text(" ", strip=True)

    # Date — try several common Drupal patterns
    date = ""
    date_candidates = [
        soup.find("time"),
        soup.find(class_=re.compile(r"(date|submitted|posted|pub)", re.I)),
        soup.find(attrs={"datetime": True}),
    ]
    for el in date_candidates:
        if el:
            date = el.get("datetime") or el.get_text(" ", strip=True)
            if date:
                # If it's an ISO datetime, convert to a readable form
                try:
                    dt = datetime.fromisoformat(date.rstrip("Z"))
                    date = dt.strftime("%-d %B %Y")
                except Exception:
                    pass
                break

    # Article body — wablieft uses paragraph blocks inside newspaper-container
    paras = []
    container = soup.find("div", class_="newspaper-container")
    search_root = container if container else soup

    # Primary: field--name-field-text blocks (Drupal paragraph structure)
    text_fields = search_root.find_all("div", class_=re.compile(r"field--name-field-text"))
    for tf in text_fields:
        for p in tf.find_all("p"):
            text = p.get_text(" ", strip=True)
            if text and len(text) > 20:
                paras.append(text)

    # Fallback: any <p> inside node__content within the container
    if not paras:
        node = search_root.find("div", class_="node__content")
        if node:
            for p in node.find_all("p"):
                text = p.get_text(" ", strip=True)
                if text and len(text) > 20:
                    paras.append(text)

    # Image — look in the npa-image or media-image field inside the container
    image = ""
    img_field = (
        search_root.find("div", class_=re.compile(r"field--name-field-npa-image"))
        or search_root.find("div", class_=re.compile(r"field--name-field-media-image"))
        or search_root.find("div", class_=re.compile(r"field--name-field-image"))
    )
    if img_field:
        img_tag = img_field.find("img")
        if img_tag:
            src = img_tag.get("src") or img_tag.get("data-src") or ""
            if src and not src.startswith("data:"):
                if src.startswith("/"):
                    src = BASE_URL + src
                image = src

    return title, date, paras, image


def fetch_article(session, slug):
    url = BASE_URL + slug
    r = session.get(url, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    return parse_article(soup)


# ── Main ────────────────────────────────────────────────────────────────────────

def main():
    email, password = get_credentials()

    session = requests.Session()
    session.headers.update(HEADERS)

    login(session, email, password)

    all_articles = []
    skipped = 0

    for section_key, section_label in SECTIONS:
        print(f"Section: {section_label} ({section_key})")
        try:
            links = get_article_links(session, section_key)
        except Exception as e:
            print(f"  Could not fetch section listing: {e}\n")
            continue

        print(f"  {len(links)} article(s) found")

        for link in links:
            short_title = link["title"][:60]
            print(f"  → {short_title}")
            try:
                title, date, paras, image = fetch_article(session, link["slug"])
                if not paras:
                    print("    (no body content — skipping)")
                    skipped += 1
                    continue
                all_articles.append({
                    "section":      section_key,
                    "sectionLabel": section_label,
                    "title":        title or link["title"],
                    "date":         date,
                    "image":        image,
                    "teaser":       paras[0],
                    "paras":        paras,
                    "url":          BASE_URL + link["slug"],
                })
                time.sleep(0.4)   # polite crawl rate
            except Exception as e:
                print(f"    Error: {e}")
                skipped += 1

        print()

    # ── Write output ────────────────────────────────────────────────────────────
    updated = datetime.now().strftime("%d %b %Y, %H:%M")
    payload = {"updated": updated, "articles": all_articles}

    out = os.path.join(os.path.dirname(__file__), "wablieft_articles.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)

    print("─" * 50)
    print(f"  Saved {len(all_articles)} articles  ({skipped} skipped)")
    print(f"  Output: wablieft_articles.json")
    print(f"  Reload wablieft.html in your browser to see them.")
    print("─" * 50)


if __name__ == "__main__":
    main()
