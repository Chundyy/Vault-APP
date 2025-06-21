# storage.py
import os

def guardar_localmente(user_id, tipo, dados_encriptados: str):
    pasta = "vault_storage"
    os.makedirs(pasta, exist_ok=True)
    filename = f"{pasta}/user_{user_id}_{tipo}_{os.urandom(4).hex()}.vault"
    with open(filename, "w") as f:
        f.write(dados_encriptados)
    print(f"💾 Backup local guardado: {filename}")

def guardar_binario_local(user_id, tipo, dados_encriptados: bytes):
    pasta = "vault_storage"
    os.makedirs(pasta, exist_ok=True)
    filename = f"{pasta}/user_{user_id}_{tipo}_{os.urandom(4).hex()}.vault"
    with open(filename, "wb") as f:
        f.write(dados_encriptados)
    print(f"💾 Backup binário guardado: {filename}")
