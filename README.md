# Dutch verb flashcards (shareable)

Static HTML flashcards: **Study** (one card) or **grid** (all cards). Twemoji illustrations load from the internet.

## Push to GitHub (this folder is a git repo)

If you have not added a remote yet:

1. Create an **empty** repository at [github.com/new](https://github.com/new) (no README/license—avoid merge conflicts).
2. In Terminal:

```bash
cd /path/to/dutch_verbs
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

Use **SSH** if you prefer: `git@github.com:YOUR_USERNAME/YOUR_REPO.git`

3. **GitHub Pages** (optional): Repo → **Settings → Pages → Build and deployment → Branch: `main`**, folder **`/ (root)`**.  
   Your site will be at `https://YOUR_USERNAME.github.io/YOUR_REPO/` (or the URL shown on the Pages settings page).

To use your real email on commits: `git config user.email "you@example.com"` in this folder (or set globally).

## Share with a public link (recommended)

### Netlify (about 1 minute)

1. Go to [https://app.netlify.com/drop](https://app.netlify.com/drop) and sign in (free).
2. Drag this entire **`dutch_verbs`** folder onto the page.
3. You get a URL like `https://something.netlify.app` — share that with anyone.
4. Optional: **Site settings → Domain** to rename the site.

Visitors open `/` for the landing page (QR + links) or go directly to `/dutch_verbs_flashcards_study.html`.

### GitHub Pages

1. Create a new GitHub repository.
2. Upload **all contents** of this folder to the repo root (or use Git).
3. **Settings → Pages → Build and deployment → Branch: `main`**, folder **`/ (root)`**.
4. After a few minutes, the site is at `https://<username>.github.io/<repo>/`.

If you put files in a subfolder, set Pages to that folder or move `index.html` to the published root.

## Share as a file

- Run **`./package_for_sharing.sh`** in this folder (see script header). It creates **`dutch_verbs_for_sharing.zip`**.
- Send the zip by email, AirDrop, Google Drive, etc.
- Recipients unzip and either:
  - Upload the **unzipped folder** to Netlify Drop (same as above), or
  - Open `index.html` in a browser (Twemoji still needs internet; some browsers restrict `file://`).

## What to include

**For viewing only:** all `*.html` files in this folder (including `index.html`).

**To regenerate PDFs/CSV from data:** also include `dutch_verbs_flashcards.tsv`, `dutch_verbs_flashcards_generate.py`, and `dutch_verbs_french_data.py`.

## iPhone on the same Wi‑Fi as a Mac

Double‑click **`Open_on_iPhone.command`** (macOS) to start a local server and open the QR landing page.
