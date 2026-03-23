#!/bin/bash
# commit-cathedral.sh - Quick commit helper for GLYF Cathedral
# Usage: ./commit-cathedral.sh "TYPE: Description"

if [ -z "$1" ]; then
    echo "Usage: $0 \"TYPE: Description\""
    echo "Types: FEAT, FIX, DOCS, REFACT, SEC, WIP"
    exit 1
fi

git add -A
git commit -m "$1"
git push

echo "✅ Committed and pushed: $1"