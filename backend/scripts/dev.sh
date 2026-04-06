#!/data/data/com.termux/files/usr/bin/bash
set -e
cd "$(dirname "$0")/.."
echo "Starting Kessel Bounty Command on port 8020..."
[ -d .venv ] || python -m venv .venv
. .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
export PYTHONPATH="$PWD"
echo "Server ready at http://127.0.0.1:8020"
exec python -m uvicorn app.main:app --host 127.0.0.1 --port 8020 --reload
