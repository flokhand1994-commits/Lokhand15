# Dutch verb flashcards

Practice **100 Dutch verbs** in your browser. Works on **iPhone, Android, and computers**.  
Pictures (Twemoji) load from the internet — you need Wi‑Fi or mobile data.

---

## The easy way: one link for everyone’s phone

**On a Mac:** double‑click **`Share_on_phones.command`**. A small window explains the steps and opens what you need.

**In short:**

1. You use a free website called **Netlify** ([open it here](https://app.netlify.com/drop)).
2. You drag **this whole project folder** onto the page — not a single file inside it, the **folder itself**.
3. Netlify gives you a **link** (it looks like `https://something.netlify.app`).
4. You send that link by text, WhatsApp, or email. Anyone can open it on **Safari** (iPhone) or **Chrome** (Android).

The first time, Netlify may ask you to **sign in** (email or Google is fine).  
You do **not** need to understand “hosting” or “HTTPS” — dragging the folder is enough.

---

## Email a zip instead of a link

**On a Mac:** double‑click **`Make_zip_to_share.command`**. It creates **`dutch_verbs_for_sharing.zip`** in this folder.

Send that zip like any file. The person who gets it should **unzip** it, then use **the same Netlify steps** as above (drag the folder to Netlify) so the flashcards work on phones.

---

## If you don’t use a Mac

1. Open **[app.netlify.com/drop](https://app.netlify.com/drop)** in Chrome or Edge.
2. Sign in if asked.
3. Drag **this entire folder** from File Explorer onto the page.
4. Copy and share the link Netlify shows you.

---

## Optional: add to your home screen (app icon)

After you open the link on your phone:

- **iPhone:** tap **Share** → **Add to Home Screen**.  
- **Android:** tap the **menu (⋮)** → **Install app** or **Add to Home screen** (wording varies).

---

## Practice at home (iPhone on the same Wi‑Fi as your Mac)

Double‑click **`Open_on_iPhone.command`**. It starts a small local server and shows a QR code so you can open the flashcards on your phone on the same network.

---

## Advanced: put the project on GitHub (optional)

Only if you already use Git/GitHub:

1. Create an empty repo at [github.com/new](https://github.com/new).
2. In Terminal:

```bash
cd /path/to/this/folder
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

**GitHub Pages** (optional): Repo → **Settings → Pages → Branch: `main`**, folder **`/` (root)**.  
Your site address will look like `https://YOUR_USERNAME.github.io/YOUR_REPO/`.

---

## What’s inside

- **`index.html`** — simple landing page with links to the flashcards.  
- **`dutch_verbs_flashcards_study.html`** — one card at a time (good for study).  
- **`dutch_verbs_flashcards.html`** — all cards in a grid.  
- **`manifest.webmanifest`** and **`icons/`** — help phones show a nice icon when you “add to home screen” (keep them next to the HTML when you deploy).

---

## Regenerating flashcards after you edit the data

If you change the spreadsheet or scripts:

```bash
python3 dutch_verbs_flashcards_generate.py
```

---

## Plain-text help

See **`START_HERE.txt`** for a short copy‑paste friendly version of the same steps.
