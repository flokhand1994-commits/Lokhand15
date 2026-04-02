# Dutch verb flashcards (study)

Single-page app: open **`index.html`** in a browser, or deploy this folder to **Netlify** / **GitHub Pages**.

Includes **`manifest.webmanifest`** and **`icons/`** for “Add to Home Screen” on phones. Twemoji images load from jsDelivr (internet required).

## Preview on your Mac (before GitHub)

1. Double‑click **`preview.command`** (or in Terminal: `cd` to this folder, then `./preview.command`).
2. Your browser opens **http://127.0.0.1:8765/** — you should see the flashcards.
3. Edit **`index.html`**, save, then **refresh** the browser to see changes.
4. Close the Terminal window (or press **Ctrl+C**) to stop the server.

**If the page says it can’t connect:** wait a second and refresh, or in Terminal run `cd` to this folder and `PORT=8777 ./preview.command` (another app may be using port 8765).

*(Opening `index.html` directly with File → Open sometimes breaks paths; the small server avoids that.)*

## Adding more cards

All cards live in **`index.html`** inside `<div class="viewer" id="viewer">` … `</div>`.

1. **Copy** one full `<div class="slide" …> … </div>` block (the last card is a good template).
2. Paste it **after** the last slide, **before** the closing `</div>` of `#viewer`.
3. Set **`data-index="100"`**, **`data-index="101"`**, … in order (0-based).
4. On the **first** slide only: **no** `hidden` / `aria-hidden="true"`. On **every other** slide: keep `hidden` and `aria-hidden="true"` like the others.
5. Edit the **lemma**, glosses, tenses, and example sentences inside your new block. For Twemoji, copy another card’s `<img class="clipart-img" src="https://cdn.jsdelivr.net/...">` pattern or pick an emoji SVG from [Twemoji on jsDelivr](https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/).

The page **counts slides automatically** and fixes “1 / N” labels, the **h1**, and the **title** when it loads—you do **not** need to change `100` in those by hand.

### Back of the card (two columns)

Example sentences are in **two columns**: **Perfectum (VTT)** and **Imperfectum (OVT)**. Each column has **Enkelvoud** and **Meervoud** Dutch lines with **EN** and **FR** under them.

The **Perfectum** Dutch text is stored in **`scripts/vtt_part1.py`** and **`scripts/vtt_part2.py`** (merged by **`scripts/vtt_manual.py`**). After editing those files, run:

```bash
python3 scripts/apply_two_column_sentences.py
```

to regenerate the sentence blocks inside **`index.html`**.

## Netlify

Connect this repo or drag the folder to [Netlify Drop](https://app.netlify.com/drop).

If builds fail with **“Build image no longer supported”**: **Site configuration → Build & deploy → Build image** → select the latest default image (not an old Ubuntu).

**Build settings:** leave **Build command** empty; **Publish directory** is `.` (root), matching `netlify.toml`.
