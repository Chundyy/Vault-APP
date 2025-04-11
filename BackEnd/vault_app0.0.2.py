import mysql.connector
from argon2 import PasswordHasher
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64

# === Inicializações ===

# Inicializa o Argon2id
ph = PasswordHasher()

# Chave AES (256 bits). Em produção, esta chave deve ser guardada de forma segura!
CHAVE_AES = AESGCM.generate_key(bit_length=256)

# === Funções de encriptação ===

def encriptar_documento(chave, dados):
    aesgcm = AESGCM(chave)
    nonce = os.urandom(12)  # 12 bytes recomendados para GCM
    dados_bytes = dados.encode()
    ciphertext = aesgcm.encrypt(nonce, dados_bytes, None)
    return base64.b64encode(nonce + ciphertext).decode()

def desencriptar_documento(chave, dados_encriptados):
    aesgcm = AESGCM(chave)
    dados = base64.b64decode(dados_encriptados)
    nonce = dados[:12]
    ciphertext = dados[12:]
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode()

# === Base de Dados ===

def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="P@ssw0rd",
        database="vault_app"
    )

# === Utilizadores ===

def criar_utilizador():
    username = input("Nome de utilizador: ")
    senha = input("Palavra-passe: ")
    email = input("E-mail: ")

    senha_hash = ph.hash(senha)
    email_hash = ph.hash(email)

    conn = conectar_bd()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)",
            (username, senha_hash, email)
        )
        conn.commit()
        print(f"✅ Utilizador '{username}' criado com sucesso!")
    except mysql.connector.Error as err:
        print(f"❌ Erro ao criar utilizador: {err}")

    cursor.close()
    conn.close()

def autenticar():
    username = input("Nome de utilizador: ")
    senha_digitada = input("Palavra-passe: ")

    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado:
        senha_hash_armazenada = resultado[0]
        try:
            if ph.verify(senha_hash_armazenada, senha_digitada):
                print("✅ Palavra-passe correta! Acesso permitido.")
                return True
        except Exception:
            pass

    print("❌ Palavra-passe incorreta! Acesso negado.")
    return False

# === Grupos ===

def criar_grupo():
    group_name = input("Nome do grupo: ")

    conn = conectar_bd()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO grupos (name) VALUES (%s)", (group_name,))
        conn.commit()
        print(f"✅ Grupo '{group_name}' criado com sucesso!")
    except mysql.connector.Error as err:
        print(f"❌ Erro ao criar grupo: {err}")

    cursor.close()
    conn.close()

def adicionar_utilizador_ao_grupo():
    username = input("Nome do utilizador: ")
    group_name = input("Nome do grupo: ")

    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    cursor.execute("SELECT id FROM grupos WHERE name = %s", (group_name,))
    group = cursor.fetchone()

    if user and group:
        try:
            cursor.execute("INSERT INTO group_users (user_id, group_id) VALUES (%s, %s)", (user[0], group[0]))
            conn.commit()
            print(f"✅ Utilizador '{username}' adicionado ao grupo '{group_name}'!")
        except mysql.connector.Error as err:
            print(f"❌ Erro ao adicionar ao grupo: {err}")
    else:
        print("❌ Utilizador ou grupo não encontrado!")

    cursor.close()
    conn.close()

# === Vault ===

def adicionar_item_vault():
    username = input("Nome do utilizador: ")
    tipo = input("Tipo (palavra-passe/documento/foto): ")
    dado = input("Conteúdo a guardar: ")

    dado_encriptado = encriptar_documento(CHAVE_AES, dado)

    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user:
        try:
            cursor.execute("""
                INSERT INTO vault_items (user_id, type, data_encrypted) 
                VALUES (%s, %s, %s)
            """, (user[0], tipo, dado_encriptado))
            conn.commit()
            cursor.execute("""
                INSERT INTO vault_items (user_id, type, data_encrypted) 
                VALUES (%s, %s, %s)
            """, (user[0], tipo, dado_encriptado))
            conn.commit()

            # Novo: salvar no disco
            guardar_localmente(user[0], tipo, dado_encriptado)
            print(f"✅ Item '{tipo}' adicionado com sucesso ao Vault!")
        except mysql.connector.Error as err:
            print(f"❌ Erro ao adicionar item: {err}")
    else:
        print("❌ Utilizador não encontrado!")

    cursor.close()
    conn.close()

def remover_item_vault():
    username = input("Nome do utilizador: ")

    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user:
        print("❌ Utilizador não encontrado!")
        cursor.close()
        conn.close()
        return

    user_id = user[0]

    cursor.execute("SELECT id, type, data_encrypted FROM vault_items WHERE user_id = %s", (user_id,))
    itens = cursor.fetchall()

    if not itens:
        print("ℹ️ Nenhum item encontrado para este utilizador!")
        cursor.close()
        conn.close()
        return

    print("\nItens disponíveis para remoção:")
    for item in itens:
        print(f"🔹 ID: {item[0]} | Tipo: {item[1]} | Conteúdo (encriptado): {item[2][:30]}...")

    item_id = input("Digite o ID do item que deseja remover: ")

    try:
        cursor.execute("DELETE FROM vault_items WHERE id = %s AND user_id = %s", (item_id, user_id))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"✅ Item com ID {item_id} removido com sucesso!")
        else:
            print("❌ Erro: Item não encontrado ou pertence a outro utilizador.")
    except mysql.connector.Error as err:
        print(f"❌ Erro ao remover item: {err}")

    cursor.close()
    conn.close()


# === Guardar ficheiros localmente ===

def guardar_localmente(user_id, tipo, dados_encriptados):
    pasta = "vault_storage"
    os.makedirs(pasta, exist_ok=True)

    filename = f"{pasta}/user_{user_id}_{tipo}_{os.urandom(4).hex()}.vault"
    with open(filename, "w") as f:
        f.write(dados_encriptados)

    print(f"💾 Backup local guardado em: {filename}")



# === Menu Principal ===

def menu():
    while True:
        print("\n🔐 MENU PRINCIPAL 🔐")
        print("1️⃣ Criar utilizador")
        print("2️⃣ Criar grupo")
        print("3️⃣ Adicionar utilizador a um grupo")
        print("4️⃣ Adicionar item ao Vault")
        print("5️⃣ Autenticar utilizador")
        print("6️⃣ Remover item do Vault")
        print("0️⃣ Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            criar_utilizador()
        elif escolha == "2":
            criar_grupo()
        elif escolha == "3":
            adicionar_utilizador_ao_grupo()
        elif escolha == "4":
            adicionar_item_vault()
        elif escolha == "5":
            autenticar()
        elif escolha == "6":
            remover_item_vault()
        elif escolha == "0":
            print("👋 A sair... Até breve!")
            break
        else:
            print("⚠️ Opção inválida! Escolha um número entre 0 e 6.")

# === Iniciar ===
menu()
