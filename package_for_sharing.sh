#!/bin/bash
# Creates dutch_verbs_for_sharing.zip for email / Drive / Netlify Drop.
# Run from this directory: chmod +x package_for_sharing.sh && ./package_for_sharing.sh

set -e
cd "$(dirname "$0")"
OUT="dutch_verbs_for_sharing.zip"
rm -f "$OUT"

zip -r "$OUT" \
  index.html \
  dutch_verbs_flashcards.html \
  dutch_verbs_flashcards_study.html \
  Open_on_iPhone.command \
  dutch_verbs_flashcards.tsv \
  dutch_verbs_flashcards.csv \
  dutch_verbs_flashcards_generate.py \
  dutch_verbs_french_data.py \
  README.md \
  -x "*.DS_Store" -x "__pycache__/*"

echo "Created: $(pwd)/$OUT ($(du -h "$OUT" | cut -f1))"
