from ipaddress import ip_address

from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
import secrets

# Configurações (em produção, use variáveis de ambiente)
SECRET_KEY = os.getenv("SECRET_KEY", "segredo_temporario")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def generate_session_token(user_id: int) -> str:
    """Gera um token de sessão seguro"""
    token = secrets.token_urlsafe(32)
    # Aqui você deveria armazenar o token no banco de dados
    # com user_id e data de expiração
    return f"{user_id}:{token}"

def verify_session_token(token: str) -> bool:
    """Verifica se um token de sessão é válido"""
    if not token:
        return False
    # Implemente a verificação no banco de dados
    return True  # Temporário - implemente a lógica real
