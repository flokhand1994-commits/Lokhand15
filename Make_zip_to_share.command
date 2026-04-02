#!/bin/bash
# Double-click this file (Mac) to create a zip you can email or upload to Google Drive.
cd "$(dirname "$0")"
if [[ ! -x ./package_for_sharing.sh ]]; then chmod +x ./package_for_sharing.sh; fi
./package_for_sharing.sh
ZIP="dutch_verbs_for_sharing.zip"
if [[ -f "$ZIP" ]]; then
  open -R "$ZIP"
  osascript <<END
display dialog "Done.

A file named:
  ${ZIP}

is in this folder (Finder should show it).

Send that zip by email, AirDrop, or Google Drive.

The person who receives it should:
  • unzip it
  • then use “Share on phones” (or drag the folder to Netlify the same way you would).

Twemoji pictures still need internet when someone opens the flashcards." with title "Zip created" buttons {"OK"} default button "OK"
END
else
  osascript -e 'display dialog "Something went wrong creating the zip." with title "Error" buttons {"OK"} default button "OK"'
fi
