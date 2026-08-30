#!/bin/bash
# Runs the listings refresh locally (no git commit/push — just updates
# working-tree files). Triggered by launchd at 7:00, 12:00, and 19:00.
set -uo pipefail

REPO_DIR="/Users/max/Desktop/2027-internship-tracker"
LOG_DIR="$REPO_DIR/scripts/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/local_refresh.log"

VIEW_DIR="$REPO_DIR/scripts/logs/view"

cd "$REPO_DIR" || exit 1

{
  echo "===== $(date '+%Y-%m-%d %H:%M:%S') ====="
  /usr/bin/python3 scripts/scrape.py
  /usr/bin/python3 scripts/recommend.py

  /usr/bin/python3 scripts/render_html.py listings/software-engineering.md "$VIEW_DIR/software-engineering.html"
  /usr/bin/python3 scripts/render_html.py listings/data-science-ai-machine-learning.md "$VIEW_DIR/data-science-ai-machine-learning.html"
  open "$VIEW_DIR/software-engineering.html" "$VIEW_DIR/data-science-ai-machine-learning.html"

  echo "Done."
} >> "$LOG_FILE" 2>&1
