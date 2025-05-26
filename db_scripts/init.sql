-- Criação do banco de dados (opcional, pois já definimos MYSQL_DATABASE no compose)
CREATE DATABASE IF NOT EXISTS gestao_bens_escolares CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE gestao_bens_escolares;

-- Tabela de ambientes (portas com RFID ativo)
CREATE TABLE IF NOT EXISTS ambientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    rfid_tag VARCHAR(50) UNIQUE NOT NULL,
    localizacao VARCHAR(100),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_rfid_tag (rfid_tag)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabela de bens
CREATE TABLE IF NOT EXISTS bens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    rfid_tag VARCHAR(50) UNIQUE NOT NULL,
    categoria VARCHAR(50),
    data_aquisicao DATE,
    valor DECIMAL(10,2),
    status ENUM('disponivel', 'em_uso', 'manutencao', 'descartado') DEFAULT 'disponivel',
    INDEX idx_rfid_tag (rfid_tag),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    rfid_tag VARCHAR(50) UNIQUE,
    cargo VARCHAR(50),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_rfid_tag (rfid_tag)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabela de permissões
CREATE TABLE IF NOT EXISTS permissoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    nivel ENUM('leitura', 'operador', 'administrador') NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    UNIQUE KEY uniq_usuario (usuario_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabela de movimentações
CREATE TABLE IF NOT EXISTS movimentacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bem_id INT NOT NULL,
    origem_id INT,
    destino_id INT NOT NULL,
    usuario_id INT NOT NULL,
    data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    observacao TEXT,
    FOREIGN KEY (bem_id) REFERENCES bens(id) ON DELETE CASCADE,
    FOREIGN KEY (origem_id) REFERENCES ambientes(id) ON DELETE SET NULL,
    FOREIGN KEY (destino_id) REFERENCES ambientes(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    INDEX idx_bem (bem_id),
    INDEX idx_data (data_movimentacao)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dados iniciais para demonstração
INSERT IGNORE INTO ambientes (nome, descricao, rfid_tag, localizacao) VALUES
    ('Sala de Aula 101', 'Sala de aula do 1º andar', 'A1B2C3D4E5', 'Bloco A - 1º Andar'),
    ('Laboratório de Informática', 'Laboratório com 20 computadores', 'F6G7H8I9J0', 'Bloco B - Térreo'),
    ('Secretaria', 'Setor administrativo', 'K1L2M3N4O5', 'Bloco Central');

INSERT IGNORE INTO bens (nome, descricao, rfid_tag, categoria, data_aquisicao, valor, status) VALUES
    ('Notebook Dell', 'Notebook i5 8GB RAM', 'P6Q7R8S9T0', 'Informática', '2023-01-15', 3500.00, 'disponivel'),
    ('Projetor Epson', 'Projetor Full HD', 'U1V2W3X4Y5', 'Audiovisual', '2023-02-20', 2800.00, 'em_uso'),
    ('Ar Condicionado Split', '30.000 BTUs', 'Z6A7B8C9D0', 'Climatização', '2022-11-10', 4200.00, 'disponivel');

INSERT IGNORE INTO usuarios (nome, email, rfid_tag, cargo) VALUES
    ('João Silva', 'joao@escola.com', 'E1F2G3H4I5', 'Professor'),
    ('Maria Oliveira', 'maria@escola.com', 'J6K7L8M9N0', 'Coordenadora'),
    ('Admin', 'admin@escola.com', 'O1P2Q3R4S5', 'Administrador');

INSERT IGNORE INTO permissoes (usuario_id, nivel) VALUES
    (1, 'operador'),
    (2, 'operador'),
    (3, 'administrador');

-- Movimentação de exemplo
INSERT IGNORE INTO movimentacoes (bem_id, origem_id, destino_id, usuario_id, observacao) VALUES
    (2, NULL, 1, 1, 'Alocação inicial para aula de informática');
