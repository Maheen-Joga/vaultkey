# VaultKey — Secure Password Manager

B207 Cyber Security | GISMA University of Applied Sciences

## Setup & Run

```bash
bash setup.sh
```

Then open http://127.0.0.1:5000

Demo login: username `demo` / password `Demo@12345`

## Security Features

- AES-256-GCM encryption for all stored credentials
- bcrypt password hashing (cost factor 12)
- PBKDF2-HMAC-SHA256 key derivation (600,000 iterations)
- SQL injection prevention (parameterised queries)
- CSRF protection (Flask-WTF)
- XSS prevention (Jinja2 auto-escape + CSP)
- IDOR prevention (user_id scoped queries)
- Audit logging for all security events
