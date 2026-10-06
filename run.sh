#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
  echo "Virtualenv not found. Run ./setup.sh first."
  exit 1
fi

source venv/bin/activate

if [ ! -f ".env" ]; then
  echo ".env missing. Copy .env.example → .env and add your keys."
  exit 1
fi

echo "Starting Dr. Aisha on http://localhost:${PORT:-5050} ..."
python main.py
