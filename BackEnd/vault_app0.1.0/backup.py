# main.py
from security.auth import criar_utilizador, autenticar_utilizador
from vault.vault_logic import adicionar_item_texto, listar_itens_utilizador, remover_item_por_id
from db.database import criar_grupo, adicionar_utilizador_ao_grupo
from session import Sessao

sessao = Sessao()

def menu():
    while True:
        print("\n🔐 MENU 🔐")
        print("1. Criar utilizador")
        print("2. Login")
        print("3. Adicionar item texto")
        print("4. Criar grupo")
        print("5. Adicionar utilizador a grupo")
        print("6. Listar itens de utilizador")
        print("7. Remover item por ID")
        print("8. Logout")
        print("0. Sair")

        op = input("Opção: ")

        if op == "1":
            u = input("Username: ")
            p = input("Password: ")
            e = input("Email: ")
            criar_utilizador(u, p, e)

        elif op == "2":
            u = input("Username: ")
            p = input("Password: ")
            if autenticar_utilizador(u, p):
                sessao.login(u, p)
                print("✅ Login OK")
            else:
                print("❌ Login falhou.")

        elif op == "3":
            if not sessao.esta_autenticado():
                print("⚠️ Por favor faz login primeiro.")
                continue
            t = input("Tipo: ")
            c = input("Conteúdo: ")
            adicionar_item_texto(sessao.utilizador, t, c, sessao.password)

        elif op == "4":
            nome = input("Nome do grupo: ")
            criar_grupo(nome)

        elif op == "5":
            user = input("Nome do utilizador: ")
            grupo = input("Nome do grupo: ")
            adicionar_utilizador_ao_grupo(user, grupo)

        elif op == "6":
            if not sessao.esta_autenticado():
                print("⚠️ Por favor faz login primeiro.")
                continue
            listar_itens_utilizador(sessao.utilizador, sessao.password)

        elif op == "7":
            if not sessao.esta_autenticado():
                print("⚠️ Por favor faz login primeiro.")
                continue
            item_id = input("ID do item: ")
            remover_item_por_id(sessao.utilizador, item_id)

        elif op == "8":
            sessao.logout()
            print("🚪 Logout efetuado.")

        elif op == "0":
            break

        else:
            print("Opção inválida.")

menu()