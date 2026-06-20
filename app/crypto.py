"""
crypto.py — Encryption utilities for VaultKey

All sensitive fields (passwords, notes) are encrypted at rest using AES-256-GCM.
A unique IV is generated per encryption call so no two ciphertexts share an IV.
The master encryption key is derived from the user's login password using PBKDF2-HMAC-SHA256,
meaning Anthropic (or any server operator) cannot decrypt vault data without the user's password.

Key derivation:  PBKDF2-HMAC-SHA256  (600,000 iterations, 32-byte output)
Encryption:      AES-256-GCM          (128-bit authentication tag, 12-byte random IV)
Password hashing for auth:  bcrypt    (cost factor 12)
"""

import os
import base64
import bcrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


# ---------- Password hashing (for authentication) ----------

def hash_password(plain: str) -> tuple[str, str]:
    """Return (bcrypt_hash, hex_salt). Salt is embedded in hash but we
    also store it separately for the KDF step."""
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(plain.encode(), salt)
    return hashed.decode(), salt.decode()


def verify_password(plain: str, stored_hash: str) -> bool:
    """Constant-time bcrypt comparison."""
    return bcrypt.checkpw(plain.encode(), stored_hash.encode())


# ---------- Key derivation (for vault encryption) ----------

def derive_key(password: str, salt_str: str) -> bytes:
    """
    Derive a 256-bit AES key from the user's password + stored salt string.
    Uses PBKDF2-HMAC-SHA256 with 600,000 iterations (OWASP 2023 recommendation).
    The salt is encoded to bytes directly from the string.
    """
    salt = salt_str.encode('utf-8')
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600_000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())


# ---------- AES-256-GCM encryption / decryption ----------

def encrypt(plaintext: str, key: bytes) -> tuple[bytes, bytes]:
    """
    Encrypt a UTF-8 string with AES-256-GCM.
    Returns (ciphertext_with_tag, iv).  iv must be stored alongside ciphertext.
    """
    iv = os.urandom(12)          # 96-bit random IV — never reuse with the same key
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(iv, plaintext.encode('utf-8'), None)
    return ciphertext, iv


def decrypt(ciphertext: bytes, iv: bytes, key: bytes) -> str:
    """
    Decrypt AES-256-GCM ciphertext.  Raises InvalidTag if tampered.
    """
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(iv, ciphertext, None)
    return plaintext.decode('utf-8')


# ---------- Password generator ----------

import secrets
import string

def generate_password(length: int = 20, use_symbols: bool = True) -> str:
    """
    Cryptographically secure password generator using secrets.choice.
    Character set: uppercase + lowercase + digits + optional symbols.
    """
    chars = string.ascii_letters + string.digits
    if use_symbols:
        chars += "!@#$%^&*()-_=+[]{}|;:,.<>?"
    # Guarantee at least one of each required class
    pwd = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
    ]
    if use_symbols:
        pwd.append(secrets.choice("!@#$%^&*()-_=+[]{}|;:,.<>?"))
    pwd += [secrets.choice(chars) for _ in range(length - len(pwd))]
    secrets.SystemRandom().shuffle(pwd)
    return ''.join(pwd)
