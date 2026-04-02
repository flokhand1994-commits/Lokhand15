#!/bin/bash
# Double-click this file (Mac) to get a shareable link that works on iPhone and Android.
cd "$(dirname "$0")"
printf "%s" "$PWD" | pbcopy
osascript <<'END'
display dialog "HOW TO GET A LINK FOR PHONES

① Your browser will open a site called Netlify.
② Finder will open — use that folder (the whole folder, not one file).
③ Drag that folder onto the Netlify page.

④ Netlify will give you a link (it ends in .netlify.app).
   Copy that link and send it by text, WhatsApp, or email.

First time only: Netlify may ask you to sign in — a free account is fine.

Your folder location is already copied — you can paste it (⌘V) if Finder asks." with title "Dutch flashcards — share on phones" buttons {"Open browser & Finder"} default button "Open browser & Finder"
END
open "https://app.netlify.com/drop"
open .
