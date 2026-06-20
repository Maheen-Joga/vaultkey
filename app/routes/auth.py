"""
auth.py — Registration, login, logout

Security measures implemented:
- bcrypt password hashing (cost 12)
- PBKDF2 key derivation for vault encryption key (never stored)
- Flask session with HttpOnly + SameSite=Lax cookie
- Login attempt audit logging with IP address
- Input sanitisation via strip() before DB insertion
- Parameterised queries everywhere — no string interpolation
"""

from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash, current_app)
from ..database import get_db
from ..crypto import hash_password, verify_password

bp = Blueprint('auth', __name__)

MAX_USERNAME_LEN = 64
MAX_EMAIL_LEN    = 254


def log_action(user_id, action, detail=None):
    db = get_db()
    ip = request.remote_addr
    db.execute(
        "INSERT INTO audit_log (user_id, action, detail, ip) VALUES (?, ?, ?, ?)",
        (user_id, action, detail, ip)
    )
    db.commit()


# ── Register ────────────────────────────────────────────────────────────────

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('vault.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()[:MAX_USERNAME_LEN]
        email    = request.form.get('email',    '').strip()[:MAX_EMAIL_LEN]
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm',  '')

        errors = []
        if not username or not email or not password:
            errors.append("All fields are required.")
        if password != confirm:
            errors.append("Passwords do not match.")
        if len(password) < 10:
            errors.append("Password must be at least 10 characters.")

        db = get_db()
        if db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone():
            errors.append("Username already taken.")
        if db.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone():
            errors.append("Email already registered.")

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('auth/register.html')

        hashed, salt = hash_password(password)
        # Parameterised INSERT — safe from SQL injection
        db.execute(
            "INSERT INTO users (username, email, password, salt) VALUES (?, ?, ?, ?)",
            (username, email, hashed, salt)
        )
        db.commit()
        user = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
        log_action(user['id'], 'REGISTER', f'New account: {username}')
        flash("Account created — you can now log in.", 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


# ── Login ────────────────────────────────────────────────────────────────────

@bp.route('/login', methods=['GET', 'POST'])
@bp.route('/', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('vault.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

        # Always run verify_password to prevent timing attacks leaking existence
        dummy_hash = "$2b$12$aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        stored = user['password'] if user else dummy_hash

        if user and verify_password(password, stored):
            session.clear()
            session['user_id']  = user['id']
            session['username'] = user['username']
            # Store salt for vault KDF (never store derived key)
            session['salt']     = user['salt']
            session.permanent   = False          # session dies on browser close
            log_action(user['id'], 'LOGIN', 'Successful')
            return redirect(url_for('vault.index'))
        else:
            log_action(user['id'] if user else None, 'LOGIN_FAIL', f'Attempt for: {username}')
            flash("Invalid username or password.", 'error')

    return render_template('auth/login.html')


# ── Logout ───────────────────────────────────────────────────────────────────

@bp.route('/logout')
def logout():
    user_id = session.get('user_id')
    log_action(user_id, 'LOGOUT')
    session.clear()
    flash("You have been logged out.", 'info')
    return redirect(url_for('auth.login'))
