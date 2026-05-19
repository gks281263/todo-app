#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"

# ── Backend ─────────────────────────────────────────────────
echo "Setting up backend..."

if [ ! -d "$BACKEND_DIR/venv" ]; then
    python3 -m venv "$BACKEND_DIR/venv"
fi
source "$BACKEND_DIR/venv/bin/activate"
pip install -q -r "$BACKEND_DIR/requirements.txt"

cd "$BACKEND_DIR"
alembic upgrade head
echo "Backend ready. Migrations applied."

uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!
cd "$PROJECT_DIR"

# ── Frontend ────────────────────────────────────────────────
echo ""
echo "Setting up frontend..."

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

cd "$FRONTEND_DIR"
if [ ! -d "node_modules" ]; then
    npm install
fi

npm run dev &
FRONTEND_PID=$!
cd "$PROJECT_DIR"

# ── Cleanup on exit ─────────────────────────────────────────
cleanup() {
    echo ""
    echo "Shutting down..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    wait 2>/dev/null
}
trap cleanup EXIT INT TERM

echo ""
echo "──────────────────────────────────────"
echo "  Backend:  http://localhost:8000"
echo "  API docs: http://localhost:8000/docs"
echo "  Frontend: http://localhost:5173"
echo "  Database: $BACKEND_DIR/todo.db"
echo "──────────────────────────────────────"
echo "Press Ctrl+C to stop."
echo ""

wait
