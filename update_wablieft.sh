#!/bin/bash
set -e
cd "$(dirname "$0")"

# Create .env if it doesn't exist yet
if [ ! -f .env ]; then
  echo ""
  echo "Enter your wablieft.be login details:"
  read -p "  Email: " email
  read -s -p "  Password: " password
  echo ""
  printf "WABLIEFT_EMAIL=%s\nWABLIEFT_PASSWORD=%s\n" "$email" "$password" > .env
  echo "  ✓ Credentials saved to .env"
fi

# Install Python deps quietly
python3 -m pip install -q requests beautifulsoup4 python-dotenv

# Fetch articles
python3 fetch_wablieft.py
