# crypto.py
from argon2 import PasswordHasher
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64
import hashlib

# Inicialização do Argon2id
ph = PasswordHasher()

# ⚠️ Em produção, esta chave deve ser segura (ex: variáveis de ambiente ou cofre seguro)
CHAVE_AES = AESGCM.generate_key(bit_length=256)

def hash_password(pwd: str) -> str:
    return ph.hash(pwd)

def verify_password(hash_guardado: str, pwd_fornecido: str) -> bool:
    try:
        return ph.verify(hash_guardado, pwd_fornecido)
    except Exception:
        return False

def encrypt_text(dado: str) -> str:
    aesgcm = AESGCM(CHAVE_AES)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, dado.encode(), None)
    return base64.b64encode(nonce + ciphertext).decode()

def decrypt_text(encrypted_b64: str) -> str:
    aesgcm = AESGCM(CHAVE_AES)
    dados = base64.b64decode(encrypted_b64)
    nonce = dados[:12]
    ciphertext = dados[12:]
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode()

def encrypt_binary(data: bytes) -> bytes:
    aesgcm = AESGCM(CHAVE_AES)
    nonce = os.urandom(12)
    return nonce + aesgcm.encrypt(nonce, data, None)

def decrypt_binary(data: bytes) -> bytes:
    aesgcm = AESGCM(CHAVE_AES)
    nonce = data[:12]
    ciphertext = data[12:]
    return aesgcm.decrypt(nonce, ciphertext, None)

def derivar_chave(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000, dklen=32)

def desencriptar(combined_data: bytes, password: str) -> str:
    salt = combined_data[:16]
    nonce = combined_data[16:28]
    ciphertext = combined_data[28:]
    key = derivar_chave(password, salt)
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode()

