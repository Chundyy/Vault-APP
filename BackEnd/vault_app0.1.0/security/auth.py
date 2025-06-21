# auth.py
from db.database import conectar_bd
from security.crypto import hash_password, verify_password

def criar_utilizador(username: str, senha: str, email: str):
    senha_hash = hash_password(senha)
    email_hash = hash_password(email)

    conn = conectar_bd()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)",
            (username, senha_hash, email_hash)
        )
        conn.commit()
        print(f"✅ Utilizador '{username}' criado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar utilizador: {e}")
    finally:
        cursor.close()
        conn.close()

def autenticar_utilizador(username: str, senha: str) -> bool:
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado:
        return verify_password(resultado[0], senha)

    return False


def autenticar_utilizador(username: str, password: str) -> bool:
    print(f"DEBUG - Username recebido: '{username}'")  # Novo
    print(f"DEBUG - Password recebido: '{password}'")  # Novo

    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
    resultado = cursor.fetchone()

    print(f"DEBUG - Resultado DB: {resultado}")  # Novo

    cursor.close()
    conn.close()

    if resultado:
        return verify_password(resultado[0], password)

    return False
