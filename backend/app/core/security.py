import base64, os
from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# JWT
ALGORITHM = "HS256"


def create_access_token(subject: dict, expires_minutes: int | None = None) -> str:
expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes or settings.JWT_EXPIRE_MIN)
to_encode = {**subject, "exp": expire}
return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
return jwt.decode(token, settings.JWT_SECRET, algorithms=[ALGORITHM])


# Passwords


def hash_password(password: str) -> str:
return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
return pwd_context.verify(password, hashed)


# AES-256-GCM for API keys


def _derive_key(master_key: str, salt: bytes) -> bytes:
kdf = PBKDF2HMAC(
algorithm=hashes.SHA256(), length=32, salt=salt, iterations=390_000
)
return kdf.derive(master_key.encode())


def encrypt_secret(plaintext: str) -> str:
if plaintext is None:
return None
salt = os.urandom(16)
key = _derive_key(settings.MASTER_KEY, salt)
aes = AESGCM(key)
nonce = os.urandom(12)
ct = aes.encrypt(nonce, plaintext.encode(), None)
return base64.urlsafe_b64encode(salt + nonce + ct).decode()


def decrypt_secret(token: str) -> str:
if token is None:
return None
raw = base64.urlsafe_b64decode(token.encode())
salt, nonce, ct = raw[:16], raw[16:28], raw[28:]
key = _derive_key(settings.MASTER_KEY, salt)
aes = AESGCM(key)
return aes.decrypt(nonce, ct, None).decode()