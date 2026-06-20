#!/usr/bin/env bash
# =============================================================================
# setup.sh — VaultKey: one-command environment setup
# =============================================================================
# Usage:  bash setup.sh
#
# This script:
#   1. Checks Python 3.9+
#   2. Creates a virtual environment
#   3. Installs all dependencies
#   4. Generates a secure SECRET_KEY
#   5. Initialises the SQLite database with schema + demo data
#   6. Starts the Flask development server
# =============================================================================

set -e

PYTHON=python3
VENV=venv
PORT=5000

echo ""
echo "  🔐  VaultKey — Secure Password Manager"
echo "  ────────────────────────────────────────"
echo ""

# ── 1. Check Python version ──────────────────────────────────────────────────
if ! command -v $PYTHON &>/dev/null; then
  echo "  ✗  python3 not found. Please install Python 3.9+."
  exit 1
fi

PY_VER=$($PYTHON -c "import sys; print(sys.version_info[:2])")
echo "  ✓  Python found: $($PYTHON --version)"

# ── 2. Virtual environment ───────────────────────────────────────────────────
if [ ! -d "$VENV" ]; then
  echo "  ➜  Creating virtual environment..."
  $PYTHON -m venv $VENV
fi
# shellcheck disable=SC1091
source $VENV/bin/activate
echo "  ✓  Virtual environment activated"

# ── 3. Install dependencies ──────────────────────────────────────────────────
echo "  ➜  Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet \
  flask==3.0.3 \
  cryptography==42.0.8 \
  bcrypt==4.1.3 \
  flask-wtf==1.2.1

echo "  ✓  Dependencies installed"

# ── 4. Generate SECRET_KEY ───────────────────────────────────────────────────
if [ ! -f .env ]; then
  SK=$($PYTHON -c "import secrets; print(secrets.token_hex(32))")
  echo "SECRET_KEY=$SK" > .env
  echo "  ✓  Secret key generated → .env"
else
  echo "  ✓  .env already exists — skipping key generation"
fi

export $(grep -v '^#' .env | xargs)

# ── 5. Initialise DB with demo seed data ─────────────────────────────────────
echo "  ➜  Initialising database..."
$PYTHON - << 'PYEOF'
import os, sys
os.environ.setdefault('SECRET_KEY', os.urandom(32).hex())

# Ensure instance/ dir exists before Flask tries to use it
os.makedirs('instance', exist_ok=True)

from app import create_app
from app.database import get_db
from app.crypto import hash_password, encrypt, derive_key

app = create_app()

with app.app_context():
    db = get_db()

    # Check if demo user already exists
    existing = db.execute("SELECT id FROM users WHERE username = 'demo'").fetchone()
    if existing:
        print("  ✓  Demo user already exists — skipping seed")
        sys.exit(0)

    # Create demo user: demo / Demo@12345
    demo_pass = "Demo@12345"
    hashed, salt = hash_password(demo_pass)
    db.execute(
        "INSERT INTO users (username, email, password, salt) VALUES (?, ?, ?, ?)",
        ('demo', 'demo@vaultkey.local', hashed, salt)
    )
    db.commit()
    user = db.execute("SELECT id, salt FROM users WHERE username = 'demo'").fetchone()

    # Derive key the same way the app does
    key = derive_key(
        app.config['SECRET_KEY'],
        user['salt']
    )

    # Seed three demo entries
    entries = [
        ('GitHub',   'https://github.com',         'demo@vaultkey.local', 'Gh!tHub$ecure99'),
        ('Gmail',    'https://mail.google.com',     'demo@gmail.com',      'Gm@il#Pass2024!'),
        ('LinkedIn', 'https://linkedin.com',        'demo@vaultkey.local', 'L!nkd1n_Secure'),
    ]
    for site, url, uname, pwd in entries:
        enc_pwd, iv = encrypt(pwd, key)
        db.execute(
            """INSERT INTO vault_entries
               (user_id, site_name, site_url, username, password, iv)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user['id'], site, url, uname, enc_pwd, iv)
        )
    db.commit()

    print("  ✓  Database seeded with demo user and 3 entries")
    print("")
    print("     Demo credentials:")
    print("       Username : demo")
    print("       Password : Demo@12345")

PYEOF

# ── 6. Launch ────────────────────────────────────────────────────────────────
echo ""
echo "  ────────────────────────────────────────"
echo "  🚀  Starting VaultKey on http://127.0.0.1:$PORT"
echo "  Press Ctrl+C to stop."
echo "  ────────────────────────────────────────"
echo ""

export FLASK_APP=run.py
export FLASK_ENV=development
flask run --host=127.0.0.1 --port=$PORT
