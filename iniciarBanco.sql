-- Criar o banco de dados
CREATE DATABASE tarefas_db;

-- Conectar ao banco
\c tarefas_db;

-- Criar a tabela de tarefas
CREATE TABLE tarefas (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    status VARCHAR(50) DEFAULT 'pendente',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);