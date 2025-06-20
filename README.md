### **Vault App - Cofre Digital de Credenciais**

O Vault é uma aplicação segura para o armazenamento e gestão de dados confidenciais, como passwords, documentos, projectos e fotografia. O foco principal é a proteção, criptografia e confidencialidade das informações, garantindo que apenas os utilizadores autorizados possam aceder aos seu dados.

### **Funcionalidades Principais**

- Aarmazenamento Seguro -> Proteção de passwords, docs, e fotos.
- Criptografia Avançada -> Utilização de AES-256 para proteger os dados.
- Senhas Mestras e Hasing seguro -> Hash das credenciais com bcryp / Argon2.
- Autenticação Multifator (2FA) -> Opções de segurança extra via SMS, email ou biometria
- Grupos de Credenciais -> Organização das informações por categorias: Pessoal, Trabalho e Outros (Customizavel)
- Controle de Acessos Empresarial -> Diferentes niveis de acesso para funcionarios, chefes e CO's
- Backups Automaticos -> Garantia de recuperação segura dos dados

### **Tecnologias Utilizadas**

- FrontEnd: PHP + HTMX (para interatividade moderna sem JavaScript complexo)
- BackEnd: Python + FastAPI (substituindo soluções mais antigas por maior performance e segurança)
- Base de Dados: MySQL com encryption at-rest (proteção adicional para dados em repouso)
- Criptografia:
    - Argon2id (para hashing de senhas)
    - AES-256-GCM (para dados sensíveis)
    - PBKDF2 (para derivação de chaves)

### **Estrutura da Equipa**

- UI/UX (Interface Grafica): JoaoMreis08 & DidasO
- Base de Dados: Bill3501 & Nootzzzzz
- Criptografia: Chundy & andrecar099
- Segurança: Chundy & NunoR0drigues
 
**Product Owner: Chundy**

### **Diagrama de Arquitetura**
![VAULT](https://github.com/Chundyy/Vault-APP/blob/main/Arquitetura.png?raw=true)

![VAULT](https://github.com/Chundyy/Vault-APP/blob/main/Vault.png?raw=true)

