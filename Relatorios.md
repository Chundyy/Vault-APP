# Vault 0.0.1
- Pequeno Menu para testar as funcionalidades do codigo
- Encriptação de palavras passes em Argon2
- Encriptação de dados pessoais
- Encriptação de documentos em base64 (so teste, nao guarda ainda o documento em si)
- Criação de Utilizadores e Grupos
- Base de dados ligada a sistema web via xampp


# Vaut 0.0.2
- Guarda ficheiro localmente (cria um documento encriptado em base64, exemplo: user_2_document_a5f228f7.vault)


# Vault 0.1.0

## 1. Segurança Aprimorada
Sessões na Base de Dados (vs armazenamento em memória)

Cookies HTTP-Only e Secure (proteção contra XSS)

Rotação Automática de Chaves (para sessões e criptografia)

Validação de Inputs Rigorosa (prevenção contra SQL injection)

Logs de Auditoria Detalhados (rastreabilidade completa)

2. Arquitetura Moderna
Separação MVC Claro (Models, Views, Controllers)

Injeção de Dependências (melhor testabilidade)

Middlewares Especializados (tratamento centralizado)

Design Orientado a Serviços (AuthService, CryptoService)

3. Funcionalidades Avançadas
Renovação Automática de Sessão

Cleanup de Sessões Expiradas (cron job)

Proteção CSRF Integrada (via tokens)

Autenticação em Duas Etapas Pronta (base para implementar 2FA)

4. Tecnologias Adicionadas
FastAPI (vs script linear)

Jinja2 Templates (frontend organizado)

HTMX (interatividade sem JS complexo)

APScheduler (tarefas agendadas)

Pydantic (validação de dados)
