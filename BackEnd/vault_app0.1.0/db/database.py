# database.py
import mysql.connector

def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="vault_app"
    )

def obter_user_id(username):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user[0] if user else None

def inserir_vault_item(user_id, tipo, conteudo_encriptado):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO vault_items (user_id, type, data_encrypted) VALUES (%s, %s, %s)",
        (user_id, tipo, conteudo_encriptado)
    )
    conn.commit()
    cursor.close()
    conn.close()

def obter_vault_item(user_id, tipo):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT data_encrypted FROM vault_items WHERE user_id = %s AND type = %s",
        (user_id, tipo)
    )
    item = cursor.fetchone()
    cursor.close()
    conn.close()
    return item[0] if item else None

def criar_grupo(nome):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO grupos (name) VALUES (%s)", (nome,))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Erro ao criar grupo: {err}")
    finally:
        cursor.close()
        conn.close()

def adicionar_utilizador_ao_grupo(username, group_name):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.execute("SELECT id FROM grupos WHERE name = %s", (group_name,))
        group = cursor.fetchone()
        if user and group:
            cursor.execute("INSERT INTO group_users (user_id, group_id) VALUES (%s, %s)", (user[0], group[0]))
            conn.commit()
        else:
            print("Utilizador ou grupo não encontrado.")
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
    finally:
        cursor.close()
        conn.close()

def obter_vault_items(user_id):
    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, type, data_encrypted FROM vault_items WHERE user_id = %s", (user_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def remover_vault_item(item_id, user_id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vault_items WHERE id = %s AND user_id = %s", (item_id, user_id))
    conn.commit()
    sucesso = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return sucesso
