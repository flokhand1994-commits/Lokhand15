#!/bin/bash
# Single-file share: only the self-contained study flashcards HTML (no scripts/data/readme).
# Opens in Safari/Chrome on iPhone and Android; for “Add to Home Screen” + icon, use
# package_for_sharing.sh (HTTPS + manifest + icons) instead.
# Change SINGLE_HTML if you want the grid view instead: dutch_verbs_flashcards.html
set -e
cd "$(dirname "$0")"
SINGLE_HTML="dutch_verbs_flashcards_study.html"
OUT="dutch_verbs_flashcards_study_only.zip"
rm -f "$OUT"
zip -j "$OUT" "$SINGLE_HTML"
echo "Created: $(pwd)/$OUT ($(du -h "$OUT" | cut -f1)) — contains only $SINGLE_HTML"
