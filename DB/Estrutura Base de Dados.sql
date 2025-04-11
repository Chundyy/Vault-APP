Tabela users (Credenciais de Users)

CREATE TABLE users (
	id INT AUTO_INCREMENT PRIMARY KEY,
	username VARCHAR(50) UNIQUE NOT NULL,
	password_hash VARCHAR(255) NOT NULL,
	email VARCHAR(100) UNIQUE NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


Tabela vault_items (Dados Criptografados)

Armazena senhas, documentos e fotos de forma segura.

CREATE TABLE vault_items (
	id INT AUTO_INCREMENT PRIMARY KEY,
	user_id INT NOT NULL,
	type ENUM('password', 'document', 'photo') NOT NULL,
	data_encrypted TEXT NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


Tabela grupos (Grupos de Credenciais e Permissões)
Define diferentes grupos de acesso.
CREATE TABLE grupos (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(50) UNIQUE NOT NULL
);


Tabela group_users (Associação Usuário → Grupo)
Relaciona os usuários aos grupos.
CREATE TABLE group_users (
	user_id INT NOT NULL,
	group_id INT NOT NULL,
	PRIMARY KEY (user_id, group_id),
	FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
	FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE
);

Tabela permissions (Permissões por Grupo)
Define permissões de leitura, escrita e exclusão.

CREATE TABLE permissions (
	id INT AUTO_INCREMENT PRIMARY KEY,
	group_id INT NOT NULL,
	permission ENUM('read', 'write', 'delete') NOT NULL,
	FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE
);

Tabela audit_logs (Logs de Auditoria)
Registra acessos ao Vault.

CREATE TABLE audit_logs (
	id INT AUTO_INCREMENT PRIMARY KEY,
	user_id INT NOT NULL,
	action ENUM('ACCESS_VAULT', 'MODIFY_VAULT', 'DELETE_VAULT') NOT NULL,
	item_id INT NULL,
	timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	ip_address VARCHAR(45),
	FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
	FOREIGN KEY (item_id) REFERENCES vault_items(id) ON DELETE SET NULL
);




