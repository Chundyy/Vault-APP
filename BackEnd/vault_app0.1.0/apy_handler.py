#!C:\Python39\python.exe  # Aponte para seu Python
import sys
import json
from vault.vault_logic import *


def main():
    try:
        # Windows precisa desta configuração de encoding
        sys.stdin.reconfigure(encoding='utf-8')
        sys.stdout.reconfigure(encoding='utf-8')

        input_data = json.load(sys.stdin)
        action = input_data.get('action')

        # Suas funções originais
        if action == 'add_text':
            result = adicionar_item_texto(
                input_data['user_id'],
                input_data['type'],
                input_data['content'],
                input_data['password']
            )
        elif action == 'list_items':
            result = listar_itens_utilizador(
                input_data['user_id'],
                input_data['password']
            )
        # ... adicione outras ações

        print(json.dumps({'status': 'success', 'data': result}))

    except Exception as e:
        print(json.dumps({'status': 'error', 'message': str(e)}))


if __name__ == '__main__':
    main()