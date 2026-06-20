"""
generate_report.py — VaultKey B207 submission report
Aligned to the exact submission requirements of the assessment brief.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

ACCENT   = colors.HexColor('#1d4ed8')
ACCENT_L = colors.HexColor('#dbeafe')
DARK     = colors.HexColor('#0f172a')
MUTED    = colors.HexColor('#64748b')
BORDER   = colors.HexColor('#cbd5e1')
TEXT     = colors.HexColor('#1e293b')
CODE_BG  = colors.HexColor('#f1f5f9')
GREEN    = colors.HexColor('#15803d')
GREEN_L  = colors.HexColor('#dcfce7')

def S():
    return {
        'h1': ParagraphStyle('h1', fontSize=18, leading=24, fontName='Helvetica-Bold',
            textColor=DARK, spaceBefore=20, spaceAfter=6),
        'h2': ParagraphStyle('h2', fontSize=13, leading=17, fontName='Helvetica-Bold',
            textColor=DARK, spaceBefore=14, spaceAfter=5),
        'h3': ParagraphStyle('h3', fontSize=11, leading=15, fontName='Helvetica-Bold',
            textColor=colors.HexColor('#334155'), spaceBefore=10, spaceAfter=3),
        'body': ParagraphStyle('body', fontSize=10, leading=15, fontName='Helvetica',
            textColor=TEXT, spaceAfter=5, alignment=TA_JUSTIFY),
        'bullet': ParagraphStyle('bullet', fontSize=10, leading=14, fontName='Helvetica',
            textColor=TEXT, leftIndent=14, spaceAfter=3),
        'code': ParagraphStyle('code', fontSize=8.5, leading=12, fontName='Courier',
            textColor=DARK, backColor=CODE_BG, borderPadding=(6,8,6,8), spaceAfter=8),
        'caption': ParagraphStyle('caption', fontSize=8, leading=11,
            fontName='Helvetica-Oblique', textColor=MUTED, spaceAfter=6, alignment=TA_CENTER),
        'title': ParagraphStyle('title', fontSize=28, leading=34, fontName='Helvetica-Bold',
            textColor=DARK, spaceAfter=6),
        'subtitle': ParagraphStyle('subtitle', fontSize=12, leading=16, fontName='Helvetica',
            textColor=MUTED, spaceAfter=4),
        'section_num': ParagraphStyle('section_num', fontSize=8, leading=10,
            fontName='Helvetica-Bold', textColor=ACCENT, spaceAfter=1,
            textTransform='uppercase'),
        'ref': ParagraphStyle('ref', fontSize=9.5, leading=14, fontName='Helvetica',
            textColor=TEXT, spaceAfter=5, leftIndent=18, firstLineIndent=-18),
    }

def hr(color=BORDER, t=0.5):
    return HRFlowable(width='100%', thickness=t, color=color, spaceAfter=6, spaceBefore=2)

def info_box(text, s, bg=ACCENT_L, border=ACCENT):
    t = Table([[Paragraph(text, s['body'])]], colWidths=[15*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), bg),
        ('BOX', (0,0),(-1,-1), 1, border),
        ('TOPPADDING', (0,0),(-1,-1), 8),
        ('BOTTOMPADDING', (0,0),(-1,-1), 8),
        ('LEFTPADDING', (0,0),(-1,-1), 10),
        ('RIGHTPADDING', (0,0),(-1,-1), 10),
        ('ROUNDEDCORNERS', (0,0),(-1,-1), [4]),
    ]))
    return t

def build(output):
    doc = SimpleDocTemplate(output, pagesize=A4,
        leftMargin=2.5*cm, rightMargin=2.5*cm,
        topMargin=2.2*cm, bottomMargin=2.2*cm,
        title='VaultKey — B207 Cyber Security Submission',
        author='Maheen Joga')
    s = S()
    story = []

    # ── COVER ─────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph('VaultKey', s['title']))
    story.append(Paragraph('Secure Password Manager with Encryption and Web Interface', s['subtitle']))
    story.append(Spacer(1, 0.3*cm))
    story.append(hr(ACCENT, 2.5))
    story.append(Spacer(1, 0.4*cm))

    cover = [
        ['Module',      'B207 Cyber Security — GISMA University of Applied Sciences'],
        ['Student',     'Maheen Joga'],
        ['Task',        'Individual Project — Idea 2 (70% of module grade)'],
        ['Tech stack',  'Python 3 · Flask 3.0 · AES-256-GCM · bcrypt · SQLite · Flask-WTF'],
        ['GitHub',      'https://github.com/[your-username]/vaultkey'],
    ]
    ct = Table(cover, colWidths=[3*cm, 12*cm])
    ct.setStyle(TableStyle([
        ('FONTNAME',  (0,0),(0,-1), 'Helvetica-Bold'),
        ('FONTNAME',  (1,0),(1,-1), 'Helvetica'),
        ('FONTSIZE',  (0,0),(-1,-1), 9.5),
        ('TEXTCOLOR', (0,0),(0,-1), MUTED),
        ('TEXTCOLOR', (1,0),(1,-1), TEXT),
        ('ROWBACKGROUNDS',(0,0),(-1,-1),[colors.white, CODE_BG]),
        ('TOPPADDING',   (0,0),(-1,-1), 6),
        ('BOTTOMPADDING',(0,0),(-1,-1), 6),
        ('LEFTPADDING',  (0,0),(-1,-1), 8),
    ]))
    story.append(ct)
    story.append(Spacer(1, 0.8*cm))

    badges = [['AES-256-GCM', 'bcrypt (cost 12)', 'PBKDF2-HMAC-SHA256', 'CSRF · XSS · SQLi · IDOR']]
    bt = Table(badges, colWidths=[3.75*cm]*4)
    bt.setStyle(TableStyle([
        ('FONTNAME', (0,0),(-1,-1), 'Courier-Bold'),
        ('FONTSIZE', (0,0),(-1,-1), 7.5),
        ('TEXTCOLOR',(0,0),(-1,-1), colors.white),
        ('BACKGROUND',(0,0),(-1,-1), DARK),
        ('ALIGN',    (0,0),(-1,-1), 'CENTER'),
        ('TOPPADDING',(0,0),(-1,-1), 6),
        ('BOTTOMPADDING',(0,0),(-1,-1), 6),
        ('GRID',     (0,0),(-1,-1), 0.5, colors.HexColor('#334155')),
    ]))
    story.append(bt)
    story.append(PageBreak())

    # ── 1. INTRODUCTION ───────────────────────────────────────────────────────
    story.append(Paragraph('1.  Introduction', s['h1']))
    story.append(hr())
    story.append(Paragraph(
        'VaultKey is a full-stack secure password manager implemented in Python and Flask. '
        'It solves a fundamental cybersecurity problem: users reuse weak passwords because '
        'remembering many strong ones is cognitively impossible. VaultKey stores an unlimited '
        'number of credentials, each encrypted at rest with AES-256-GCM, and exposes them '
        'through a clean web interface after a single authenticated session. '
        'The master password is never stored — only a bcrypt hash is persisted — and the '
        'vault encryption key is derived from that password at runtime, meaning the database '
        'alone is useless to an attacker without the application secret.', s['body']))

    story.append(Paragraph(
        'The implementation satisfies all Idea 2 requirements: user registration and '
        'authentication, encrypted credential storage (cryptography library, AES-256-GCM), '
        'password generation (secrets module), a Flask web interface, SQLite database, '
        'bcrypt hashing with per-user salts, and defences against SQL injection, XSS, CSRF, '
        'and IDOR. The entire environment — dependencies, database schema, and seed data — '
        'is set up by a single shell script (setup.sh).', s['body']))

    # ── 2. SYSTEM DESIGN & ARCHITECTURE ──────────────────────────────────────
    story.append(Paragraph('2.  System Design and Architecture', s['h1']))
    story.append(hr())
    story.append(Paragraph(
        'VaultKey uses Flask\'s application factory pattern with two blueprints and a shared '
        'database module. This separation keeps authentication logic (auth blueprint) '
        'independent from vault operations (vault blueprint), making the codebase auditable '
        'and maintainable.', s['body']))

    story.append(Paragraph('2.1  Directory structure', s['h2']))
    story.append(Paragraph(
        'vaultkey/\n'
        '├── app/\n'
        '│   ├── __init__.py      # Application factory — registers blueprints, config\n'
        '│   ├── database.py      # SQLite connection, schema init (WAL + FK enforcement)\n'
        '│   ├── crypto.py        # All cryptographic primitives (bcrypt, AES-GCM, PBKDF2)\n'
        '│   └── routes/\n'
        '│       ├── auth.py      # /  /login  /register  /logout\n'
        '│       └── vault.py     # /vault/  /vault/add  /vault/edit  /vault/delete  /vault/generate\n'
        '├── templates/\n'
        '│   ├── base.html        # Nav, CSP/X-Frame headers, flash messages\n'
        '│   ├── auth/            # login.html  register.html\n'
        '│   └── vault/           # index.html (dashboard)  form.html (add/edit)\n'
        '├── run.py               # Entry point\n'
        '├── setup.sh             # Single automation script\n'
        '└── requirements.txt', s['code']))

    story.append(Paragraph('2.2  Database schema', s['h2']))
    story.append(Paragraph(
        'Three tables are defined and created on first run by database.py:', s['body']))

    schema_data = [
        ['Table', 'Columns', 'Purpose'],
        ['users',
         'id, username, email,\npassword (bcrypt hash), salt, created',
         'Account storage.\nNo plaintext passwords ever stored.'],
        ['vault_entries',
         'id, user_id (FK→users), site_name, site_url,\nusername, password (BLOB ciphertext),\niv (BLOB), notes (BLOB), notes_iv, created, updated',
         'Encrypted credentials.\npassword column holds AES-GCM ciphertext + tag.\niv column holds the unique 12-byte IV.'],
        ['audit_log',
         'id, user_id, action, detail, ip, timestamp',
         'Append-only security event trail for forensic audit.'],
    ]
    schema_t = Table(schema_data, colWidths=[3*cm, 7*cm, 4.5*cm])
    schema_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,0), DARK),
        ('TEXTCOLOR',  (0,0),(-1,0), colors.white),
        ('FONTNAME',   (0,0),(-1,0), 'Helvetica-Bold'),
        ('FONTNAME',   (0,1),(-1,-1),'Helvetica'),
        ('FONTSIZE',   (0,0),(-1,-1), 8.5),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, CODE_BG]),
        ('GRID',       (0,0),(-1,-1), 0.3, BORDER),
        ('TOPPADDING', (0,0),(-1,-1), 6),
        ('BOTTOMPADDING',(0,0),(-1,-1), 6),
        ('LEFTPADDING',(0,0),(-1,-1), 7),
        ('VALIGN',     (0,0),(-1,-1), 'TOP'),
    ]))
    story.append(schema_t)
    story.append(Spacer(1, 0.3*cm))

    # ── 3. HOW THE SYSTEM WORKS (submission requirement section) ─────────────
    story.append(Paragraph('3.  How the System Works', s['h1']))
    story.append(hr())
    story.append(Paragraph(
        'This section directly addresses the submission requirements: how data is retrieved '
        'from the backend via browser and database; how data is securely transmitted back to '
        'the user; how data is stored in the database and browser; and who creates and '
        'validates the authentication signatures.', s['body']))

    story.append(Paragraph('3.1  Authentication message exchange', s['h2']))
    story.append(Paragraph(
        '<b>Registration:</b> The user submits a username, email, and master password via '
        'HTTPS POST. Flask passes the plaintext password to bcrypt.hashpw() with a freshly '
        'generated salt (bcrypt.gensalt, cost 12). Only the resulting hash and salt are '
        'written to the users table — the plaintext is discarded immediately. '
        'A bcrypt hash has the form $2b$12$&lt;22-char-salt&gt;&lt;31-char-hash&gt; and is '
        'computationally infeasible to reverse.', s['body']))
    story.append(Paragraph(
        '<b>Login:</b> The user submits credentials via HTTPS POST. Flask calls '
        'bcrypt.checkpw(submitted_password, stored_hash) — a constant-time comparison '
        'that prevents timing side-channel attacks. If successful, Flask sets a server-side '
        'session containing only {user_id, username, salt}; no password or key is stored. '
        'The session ID is sent to the browser as an HttpOnly, SameSite=Lax cookie. '
        '<b>Who creates the session token:</b> Flask\'s session module (using the '
        'application SECRET_KEY for HMAC signing). '
        '<b>Who validates it:</b> Flask verifies the HMAC signature on every subsequent '
        'request before any route handler executes.', s['body']))

    story.append(Paragraph('3.2  Who creates and who validates the signatures?', s['h2']))
    story.append(info_box(
        '<b>Vault data (AES-GCM authentication tag):</b> When a credential is saved, '
        'the Flask backend calls AESGCM.encrypt(), which appends a 128-bit authentication '
        'tag to the ciphertext. <b>Creator: Flask backend at write time.</b> '
        'When retrieved, AESGCM.decrypt() verifies this tag before returning plaintext — '
        'any byte-level tampering raises cryptography.exceptions.InvalidTag. '
        '<b>Validator: Flask backend at read time.</b> '
        'The browser never sees raw ciphertext; it receives only the decrypted plaintext '
        'rendered inside HTML (Jinja2 auto-escaped).<br/><br/>'
        '<b>Session integrity (HMAC-SHA256):</b> Flask signs the session cookie with '
        'HMAC-SHA256 using SECRET_KEY. <b>Creator: Flask on login.</b> '
        '<b>Validator: Flask on every request.</b> A tampered cookie is rejected '
        'and the user is redirected to login.', s, bg=GREEN_L, border=GREEN))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('3.3  How data is retrieved from the backend via browser and database', s['h2']))
    story.append(Paragraph(
        'The sequence for a GET /vault/ request is:', s['body']))
    steps_r = [
        ['Step', 'What happens'],
        ['1', 'Browser sends GET /vault/ with the session cookie.'],
        ['2', 'Flask verifies the HMAC-signed session cookie → extracts user_id.'],
        ['3', 'login_required decorator confirms user_id is in session; otherwise redirects to /login.'],
        ['4', 'get_db() opens a parameterised SELECT on vault_entries WHERE user_id = ? (IDOR scoped).'],
        ['5', 'get_key() derives the 256-bit AES key via PBKDF2-HMAC-SHA256(SECRET_KEY, salt, 600000 iters).'],
        ['6', 'For each row, decrypt(ciphertext, iv, key) → AESGCM.decrypt() verifies tag, returns plaintext.'],
        ['7', 'Jinja2 renders plaintext into HTML (auto-escaped to prevent XSS). Passwords shown as ••••••.'],
        ['8', 'Flask returns a 200 HTML response. No raw ciphertext or keys appear in the HTTP response.'],
    ]
    rt = Table(steps_r, colWidths=[1*cm, 13.5*cm])
    rt.setStyle(TableStyle([
        ('BACKGROUND',  (0,0),(-1,0), DARK),
        ('TEXTCOLOR',   (0,0),(-1,0), colors.white),
        ('FONTNAME',    (0,0),(-1,0), 'Helvetica-Bold'),
        ('FONTNAME',    (0,1),(-1,-1),'Helvetica'),
        ('FONTSIZE',    (0,0),(-1,-1), 8.5),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, CODE_BG]),
        ('GRID',        (0,0),(-1,-1), 0.3, BORDER),
        ('TOPPADDING',  (0,0),(-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ('LEFTPADDING', (0,0),(-1,-1), 7),
        ('VALIGN',      (0,0),(-1,-1), 'TOP'),
    ]))
    story.append(rt)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('3.4  How data is securely transmitted back to the user', s['h2']))
    story.append(Paragraph(
        'All communication between browser and server occurs over HTTPS (TLS 1.2+), '
        'which encrypts the transport layer. Within the application layer:', s['body']))
    for b in [
        'Passwords are <b>not transmitted in URL parameters</b> — only POST bodies (for forms) or JSON (for the generator API), both protected by TLS.',
        'The copy-to-clipboard feature uses <b>navigator.clipboard.writeText()</b> client-side — the plaintext is rendered once into the DOM, never sent back to the server.',
        'The Flask session cookie carrying the session ID has <b>HttpOnly</b> (JavaScript cannot read it) and <b>SameSite=Lax</b> (blocks cross-site request CSRF vectors) attributes set.',
        '<b>Content-Security-Policy: default-src \'self\'</b> is set in base.html, preventing exfiltration via injected scripts.',
        '<b>X-Frame-Options: DENY</b> prevents the page being embedded in an iframe (clickjacking defence).',
    ]:
        story.append(Paragraph(f'• {b}', s['bullet']))
    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph('3.5  How data is stored in the database and in the browser', s['h2']))
    storage_data = [
        ['What', 'Database storage', 'Browser storage'],
        ['Master password', 'bcrypt hash + salt only (users table)', 'Never stored'],
        ['Vault encryption key', 'Never stored — derived on demand', 'Never stored'],
        ['Credential password', 'AES-256-GCM ciphertext + IV (BLOBs)', 'Never stored; rendered to DOM only'],
        ['Notes', 'AES-256-GCM ciphertext + IV (BLOBs)', 'Never stored; rendered to DOM only'],
        ['Session', 'Server-side Flask session (user_id, username, salt)', 'Signed session ID cookie (HttpOnly)'],
        ['CSRF token', 'Not stored — regenerated per form render', 'Hidden <input> in each form'],
    ]
    st = Table(storage_data, colWidths=[3.5*cm, 6*cm, 5*cm])
    st.setStyle(TableStyle([
        ('BACKGROUND',  (0,0),(-1,0), DARK),
        ('TEXTCOLOR',   (0,0),(-1,0), colors.white),
        ('FONTNAME',    (0,0),(-1,0), 'Helvetica-Bold'),
        ('FONTNAME',    (0,1),(-1,-1),'Helvetica'),
        ('FONTSIZE',    (0,0),(-1,-1), 8.5),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, CODE_BG]),
        ('GRID',        (0,0),(-1,-1), 0.3, BORDER),
        ('TOPPADDING',  (0,0),(-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ('LEFTPADDING', (0,0),(-1,-1), 7),
        ('VALIGN',      (0,0),(-1,-1), 'TOP'),
    ]))
    story.append(st)

    story.append(PageBreak())

    # ── 4. SECURITY IMPLEMENTATION ────────────────────────────────────────────
    story.append(Paragraph('4.  Security Implementation', s['h1']))
    story.append(hr())

    security = [
        ('4.1  Password hashing — bcrypt (cost 12)',
         'User master passwords are hashed with bcrypt (Provos and Mazières, 1999) at a '
         'work factor of 12, producing approximately 250 ms per hash on modern hardware. '
         'bcrypt embeds a unique random salt in every hash, making precomputed rainbow-table '
         'attacks infeasible. Verification uses bcrypt.checkpw(), which is constant-time, '
         'preventing timing side-channel attacks that could leak whether a username exists.',
         'hashed, salt = hash_password("MyPassword!")\n'
         '# Stored:  $2b$12$<22-char-salt><31-char-hash>\n'
         'ok = verify_password("MyPassword!", hashed)  # constant-time'),

        ('4.2  Vault encryption — AES-256-GCM',
         'All credential passwords and notes are encrypted with AES-256-GCM (McGrew and '
         'Viega, 2004) before being written to SQLite. GCM is an authenticated encryption '
         'mode: the AESGCM.encrypt() call appends a 128-bit authentication tag to the '
         'ciphertext. At decryption, AESGCM.decrypt() verifies this tag first — any '
         'byte-level modification raises cryptography.exceptions.InvalidTag, meaning '
         'tampered database entries are detected rather than silently decrypted. '
         'A unique 96-bit IV is generated via os.urandom(12) per encryption call, '
         'so identical plaintexts always produce distinct ciphertexts.',
         'ciphertext, iv = encrypt("github_password!", key)\n'
         '# ciphertext includes the 128-bit GCM authentication tag\n'
         'plaintext = decrypt(ciphertext, iv, key)  # raises if tampered'),

        ('4.3  Key derivation — PBKDF2-HMAC-SHA256',
         'The AES-256 key is never stored. It is derived on demand using '
         'PBKDF2-HMAC-SHA256 with 600,000 iterations (OWASP, 2023 minimum for this '
         'algorithm) and the user\'s bcrypt salt as the KDF salt. The derivation is '
         'performed in get_key() within the request context and cached in Flask\'s '
         'request-scoped g object — it is discarded after the response is sent.',
         'key = derive_key(app.config["SECRET_KEY"], session["salt"])\n'
         '# 600,000 PBKDF2-SHA256 iterations → 32-byte AES key\n'
         '# key lives only in memory for the duration of the request'),

        ('4.4  SQL injection prevention',
         'Every database interaction uses SQLite parameterised statements (? placeholders). '
         'String interpolation into SQL is prohibited throughout the codebase. '
         'Foreign key enforcement (PRAGMA foreign_keys = ON) and WAL journalling '
         '(PRAGMA journal_mode = WAL) are set on each connection.',
         '# Safe — parameterised\n'
         'row = db.execute("SELECT * FROM users WHERE username = ?", (username,))\n\n'
         '# Never done — vulnerable\n'
         '# db.execute(f"SELECT * FROM users WHERE username = \'{username}\'")')  ,

        ('4.5  IDOR prevention',
         'Every query against vault_entries includes AND user_id = ? scoped to the '
         'authenticated session\'s user_id. A request for /vault/edit/99 by user A '
         'will return nothing if entry 99 belongs to user B — the route redirects '
         'with an error flash rather than exposing or raising a 500.',
         'row = db.execute(\n'
         '    "SELECT * FROM vault_entries WHERE id = ? AND user_id = ?",\n'
         '    (entry_id, session["user_id"])\n'
         ').fetchone()  # None if wrong user → redirect'),

        ('4.6  XSS prevention',
         'Jinja2 auto-escapes all template variables by default, converting < > " \' & '
         'into HTML entities so user-supplied strings cannot inject script tags. '
         'The Content-Security-Policy header (default-src \'self\') in base.html '
         'provides a second layer, blocking inline scripts from untrusted origins.',
         '<!-- Jinja2 auto-escapes: safe even if site_name = "<script>..." -->\n'
         '<span>{{ e.site_name }}</span>'),

        ('4.7  CSRF protection',
         'Flask-WTF is enabled globally (WTF_CSRF_ENABLED = True). Every state-changing '
         'POST form includes a hidden CSRF token generated server-side. Flask-WTF '
         'validates the token on each POST; a missing or incorrect token returns 400. '
         'The SameSite=Lax cookie attribute provides a complementary browser-level defence.',
         '# app/__init__.py\n'
         'app.config["WTF_CSRF_ENABLED"] = True\n'
         '# Flask-WTF rejects any POST without a valid CSRF token'),

        ('4.8  Audit logging',
         'Every security event — registration, login success, login failure, logout, '
         'add/edit/delete of vault entries — is written to the audit_log table with '
         'the user_id, action type, detail string, client IP, and UTC timestamp. '
         'This append-only log provides a forensic trail for incident response.',
         'log_action(user_id, "LOGIN_FAIL", f"Attempt for: {username}")'),
    ]

    for title, body_text, code_text in security:
        story.append(KeepTogether([
            Paragraph(title, s['h2']),
            Paragraph(body_text, s['body']),
            Paragraph(code_text, s['code']),
        ]))

    story.append(PageBreak())

    # ── 5. HOW TO RUN ─────────────────────────────────────────────────────────
    story.append(Paragraph('5.  How to Run VaultKey (Live Demo Guide)', s['h1']))
    story.append(hr())
    story.append(Paragraph(
        'The assessment brief requires one script to automate everything — setup.sh '
        'fulfils this requirement.', s['body']))

    story.append(Paragraph('5.1  One-command setup', s['h2']))
    story.append(Paragraph(
        'git clone https://github.com/[your-username]/vaultkey\n'
        'cd vaultkey\n'
        'bash setup.sh', s['code']))

    story.append(Paragraph('What setup.sh does (in order):', s['h3']))
    for step in [
        '1. Checks Python 3.9+ is available.',
        '2. Creates a Python virtual environment (venv/).',
        '3. Installs all dependencies from requirements.txt into the venv.',
        '4. Generates a cryptographically random SECRET_KEY and writes it to .env.',
        '5. Exports SECRET_KEY into the environment.',
        '6. Calls create_app() — which runs database.py, creating the SQLite schema (users, vault_entries, audit_log) in instance/vaultkey.db.',
        '7. Seeds a demo user (username: demo, password: Demo@12345) and three encrypted vault entries (GitHub, Gmail, LinkedIn).',
        '8. Starts Flask on http://127.0.0.1:5000.',
    ]:
        story.append(Paragraph(step, s['bullet']))

    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph('5.2  User walkthrough', s['h2']))

    walkthrough = [
        ['Step', 'URL', 'Action'],
        ['1 — Login',     '/',              'Enter demo / Demo@12345 → click "Unlock vault"'],
        ['2 — Dashboard', '/vault/',        'Three pre-seeded entries visible. Passwords hidden by default (••••••).'],
        ['3 — Reveal',    '/vault/',        'Click 👁 on any row to reveal the decrypted password.'],
        ['4 — Copy',      '/vault/',        'Click Copy — password is written to clipboard; never sent to server.'],
        ['5 — Search',    '/vault/',        'Type in the search bar to filter entries client-side instantly.'],
        ['6 — Add entry', '/vault/add',     'Fill site name, username, password. Click "Generate ⚡" for a secure random password.'],
        ['7 — Edit',      '/vault/edit/N',  'Click Edit on any row, modify fields, save. New AES-GCM ciphertext + IV stored.'],
        ['8 — Delete',    '/vault/delete/N','Click Delete → confirm dialog → entry removed (scoped to your user).'],
        ['9 — Register',  '/register',      'Create a second account to verify isolation — each user has a separate vault.'],
        ['10 — Logout',   '/logout',        'Session cleared. Browser cookie invalidated.'],
    ]
    wt = Table(walkthrough, colWidths=[2.8*cm, 3.5*cm, 8.2*cm])
    wt.setStyle(TableStyle([
        ('BACKGROUND',  (0,0),(-1,0), DARK),
        ('TEXTCOLOR',   (0,0),(-1,0), colors.white),
        ('FONTNAME',    (0,0),(-1,0), 'Helvetica-Bold'),
        ('FONTNAME',    (0,1),(-1,-1),'Helvetica'),
        ('FONTSIZE',    (0,0),(-1,-1), 8.5),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, CODE_BG]),
        ('GRID',        (0,0),(-1,-1), 0.3, BORDER),
        ('TOPPADDING',  (0,0),(-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ('LEFTPADDING', (0,0),(-1,-1), 7),
        ('VALIGN',      (0,0),(-1,-1), 'TOP'),
    ]))
    story.append(wt)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('5.3  Dependencies', s['h2']))
    deps = [
        ['Package', 'Version', 'Purpose'],
        ['flask',        '3.0.3',  'Web framework — routing, Jinja2 templates, session management'],
        ['cryptography', '42.0.8', 'AES-256-GCM (AESGCM), PBKDF2HMAC key derivation'],
        ['bcrypt',       '4.1.3',  'Adaptive password hashing for master password authentication'],
        ['flask-wtf',    '1.2.1',  'CSRF token generation and validation on all POST routes'],
    ]
    dt = Table(deps, colWidths=[2.8*cm, 2*cm, 9.7*cm])
    dt.setStyle(TableStyle([
        ('BACKGROUND',  (0,0),(-1,0), DARK),
        ('TEXTCOLOR',   (0,0),(-1,0), colors.white),
        ('FONTNAME',    (0,0),(-1,0), 'Helvetica-Bold'),
        ('FONTNAME',    (0,1),(-1,-1),'Helvetica'),
        ('FONTSIZE',    (0,0),(-1,-1), 8.5),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, CODE_BG]),
        ('GRID',        (0,0),(-1,-1), 0.3, BORDER),
        ('TOPPADDING',  (0,0),(-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ('LEFTPADDING', (0,0),(-1,-1), 7),
    ]))
    story.append(dt)

    # ── 6. SECURITY SUMMARY ───────────────────────────────────────────────────
    story.append(Paragraph('6.  Security Measures Summary', s['h1']))
    story.append(hr())

    summary = [
        ['Vulnerability / Threat',    'Control implemented',                  'Location in codebase'],
        ['Weak password storage',      'bcrypt, cost 12, per-user salt',       'crypto.py → hash_password()'],
        ['Vault data exposure',        'AES-256-GCM authenticated encryption', 'crypto.py → encrypt/decrypt()'],
        ['Brute-force key derivation', 'PBKDF2-SHA256, 600,000 iterations',    'crypto.py → derive_key()'],
        ['SQL injection',              'Parameterised queries throughout',      'database.py, routes/'],
        ['IDOR / broken access',       'user_id scope on all vault queries',    'routes/vault.py'],
        ['XSS',                        'Jinja2 auto-escape + CSP header',       'base.html'],
        ['CSRF',                       'Flask-WTF tokens on all POST forms',    'app/__init__.py'],
        ['Clickjacking',               'X-Frame-Options: DENY',                 'base.html'],
        ['Username enumeration',       'Constant-time login (dummy hash path)', 'routes/auth.py'],
        ['Session hijacking',          'HttpOnly + SameSite=Lax cookie',        'Flask session config'],
        ['Ciphertext tampering',       'AES-GCM 128-bit authentication tag',    'crypto.py → decrypt()'],
        ['Audit / incident response',  'Append-only audit_log table',           'routes/auth.py, routes/vault.py'],
    ]
    sumT = Table(summary, colWidths=[4.5*cm, 5.5*cm, 4.5*cm])
    sumT.setStyle(TableStyle([
        ('BACKGROUND',  (0,0),(-1,0), DARK),
        ('TEXTCOLOR',   (0,0),(-1,0), colors.white),
        ('FONTNAME',    (0,0),(-1,0), 'Helvetica-Bold'),
        ('FONTNAME',    (0,1),(-1,-1),'Helvetica'),
        ('FONTSIZE',    (0,0),(-1,-1), 8),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, CODE_BG]),
        ('GRID',        (0,0),(-1,-1), 0.3, BORDER),
        ('TOPPADDING',  (0,0),(-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ('LEFTPADDING', (0,0),(-1,-1), 7),
        ('VALIGN',      (0,0),(-1,-1), 'TOP'),
    ]))
    story.append(sumT)

    # ── 7. REFERENCES ─────────────────────────────────────────────────────────
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph('7.  References', s['h1']))
    story.append(hr())

    refs = [
        'McGrew, D. and Viega, J. (2004) <i>The Galois/Counter Mode of Operation (GCM)</i>. Submission to IEEE P1619 Working Group. Available at: https://csrc.nist.rip/groups/ST/toolkit/BCM/documents/proposedmodes/gcm/gcm-spec.pdf (Accessed: June 2025).',
        'NIST (2022) <i>SP 800-132: Recommendation for Password-Based Key Derivation — Part 1: Storage Applications</i>. National Institute of Standards and Technology. Available at: https://doi.org/10.6028/NIST.SP.800-132 (Accessed: June 2025).',
        'OWASP (2023) <i>Password Storage Cheat Sheet</i>. Available at: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html (Accessed: June 2025).',
        'OWASP (2023) <i>SQL Injection Prevention Cheat Sheet</i>. Available at: https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html (Accessed: June 2025).',
        'OWASP (2023) <i>Cross-Site Request Forgery Prevention Cheat Sheet</i>. Available at: https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html (Accessed: June 2025).',
        'OWASP (2023) <i>Cross Site Scripting Prevention Cheat Sheet</i>. Available at: https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html (Accessed: June 2025).',
        'Pallets Projects (2024) <i>Flask Documentation (3.0.x)</i>. Available at: https://flask.palletsprojects.com (Accessed: June 2025).',
        'Provos, N. and Mazières, D. (1999) \'A Future-Adaptable Password Scheme\', <i>Proceedings of the USENIX Annual Technical Conference</i>, Monterey, CA, pp. 32–32.',
        'Python Cryptographic Authority (2024) <i>cryptography library documentation</i>. Available at: https://cryptography.io/en/latest/ (Accessed: June 2025).',
    ]
    for i, ref in enumerate(refs, 1):
        story.append(Paragraph(f'{i}.&nbsp;&nbsp;{ref}', s['ref']))

    doc.build(story)
    print(f'Report written → {output}')

if __name__ == '__main__':
    build('/mnt/user-data/outputs/VaultKey_B207_Report.pdf')
