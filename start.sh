#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

if command -v python3 >/dev/null 2>&1; then
    python3 a.py
elif command -v python >/dev/null 2>&1; then
    python a.py
else
    echo "Python was not found. Please install Python 3 and try again."
    exit 1
fi
