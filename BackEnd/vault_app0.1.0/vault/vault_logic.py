# vault/vault_logic.py

from db.database import conectar_bd, obter_user_id, obter_vault_items, remover_vault_item
from security.crypto import encrypt_binary, decrypt_binary, desencriptar, derivar_chave
from vault.storage import guardar_localmente, guardar_binario_local
import base64
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def encrypt_text(dado: str, password: str) -> str:
    salt = os.urandom(16)
    nonce = os.urandom(12)
    key = derivar_chave(password, salt)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, dado.encode(), None)
    combined = salt + nonce + ciphertext
    return base64.b64encode(combined).decode()

def decrypt_text(encrypted_b64: str, password: str) -> str:
    combined = base64.b64decode(encrypted_b64)
    return desencriptar(combined, password)

def adicionar_item_texto(username: str, tipo: str, conteudo: str, password: str):
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user:
        print("❌ Utilizador não encontrado.")
        return

    user_id = user[0]
    dado_encriptado = encrypt_text(conteudo, password)

    try:
        cursor.execute("INSERT INTO vault_items (user_id, type, data_encrypted) VALUES (%s, %s, %s)",
                       (user_id, tipo, dado_encriptado))
        conn.commit()
        guardar_localmente(user_id, tipo, dado_encriptado)
        print("✅ Item guardado com sucesso.")
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        cursor.close()
        conn.close()

def adicionar_item_ficheiro(user_id: int, tipo: str, caminho_ficheiro: str, password: str):
    with open(caminho_ficheiro, "rb") as f:
        dados = f.read()

    salt = os.urandom(16)
    nonce = os.urandom(12)
    key = derivar_chave(password, salt)
    aesgcm = AESGCM(key)
    encrypted = aesgcm.encrypt(nonce, dados, None)
    combined = salt + nonce + encrypted
    combined_b64 = base64.b64encode(combined).decode()

    conn = conectar_bd()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO vault_items (user_id, type, data_encrypted) VALUES (%s, %s, %s)",
                       (user_id, tipo, combined_b64))
        conn.commit()
        guardar_binario_local(user_id, tipo, salt + nonce + encrypted)
        print("✅ Ficheiro encriptado e guardado.")
    except Exception as e:
        print(f"❌ Erro ao guardar: {e}")
    finally:
        cursor.close()
        conn.close()

def listar_itens_utilizador(username: str, password: str):
    user_id = obter_user_id(username)
    if not user_id:
        print("❌ Utilizador não encontrado.")
        return

    itens = obter_vault_items(user_id)
    if not itens:
        print("ℹ️ Sem itens.")
        return

    print("\n📂 Itens armazenados:")
    for item in itens:
        try:
            dados_b64 = item['data_encrypted']
            conteudo = decrypt_text(dados_b64, password)
            print(f"🔐 ID: {item['id']} | Tipo: {item['type']} | Conteúdo: {conteudo[:30]}...")
        except Exception as e:
            print(f"⚠️ Erro ao desencriptar item {item['id']}: {e}")

def remover_item_por_id(username: str, item_id: int):
    user_id = obter_user_id(username)
    if not user_id:
        print("❌ Utilizador não encontrado.")
        return

    sucesso = remover_vault_item(item_id, user_id)
    if sucesso:
        print(f"✅ Item {item_id} removido.")
    else:
        print("❌ Item não encontrado ou não pertence ao utilizador.")

def adicionar_item_texto_grupo(username: str, grupos: str, tipo: str, conteudo: str, password: str):
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if not user:
        print("❌ Utilizador não encontrado.")
        return
    user_id = user[0]

    cursor.execute("SELECT id FROM grupos WHERE name = %s", (grupos,))
    grupo_res = cursor.fetchone()
    if not grupo_res:
        print("❌ Grupo não encontrado.")
        return
    grupo_id = grupo_res[0]

    salt = os.urandom(16)
    nonce = os.urandom(12)
    key = derivar_chave(password, salt)
    aesgcm = AESGCM(key)
    encrypted = aesgcm.encrypt(nonce, conteudo.encode(), None)
    combinado = salt + nonce + encrypted
    dado_b64 = base64.b64encode(combinado).decode()

    try:
        cursor.execute("""
            INSERT INTO vault_items (user_id, group_id, type, data_encrypted)
            VALUES (%s, %s, %s, %s)
        """, (user_id, grupo_id, tipo, dado_b64))
        conn.commit()
        print("✅ Item guardado para o grupo.")
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        cursor.close()
        conn.close()

def listar_itens_grupo(username: str, grupo: str, password: str):
    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if not user:
        print("❌ Utilizador não encontrado.")
        return
    user_id = user['id']

    cursor.execute("SELECT id FROM grupos WHERE name = %s", (grupo,))
    g = cursor.fetchone()
    if not g:
        print("❌ Grupo não encontrado.")
        return
    grupo_id = g['id']

    # Verificar se o user pertence ao grupo
    cursor.execute("SELECT * FROM group_users WHERE user_id = %s AND group_id = %s", (user_id, grupo_id))
    assoc = cursor.fetchone()
    if not assoc:
        print("❌ Utilizador não pertence ao grupo.")
        return

    cursor.execute("""
        SELECT id, type, data_encrypted FROM vault_items
        WHERE group_id = %s
    """, (grupo_id,))
    items = cursor.fetchall()
    if not items:
        print("📁 Sem itens no grupo.")
        return

    print(f"\n📂 Itens do grupo '{grupo}':")
    for item in items:
        try:
            dados = base64.b64decode(item['data_encrypted'])
            conteudo = desencriptar(dados, password)
            print(f"🔐 ID: {item['id']} | Tipo: {item['type']} | Conteúdo: {conteudo[:30]}...")
        except Exception as e:
            print(f"⚠️ Erro ao desencriptar item {item['id']}: {e}")

