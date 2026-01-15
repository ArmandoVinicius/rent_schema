-- CRIAÇÃO DO ESQUEMA

CREATE SCHEMA IF NOT EXISTS rent_schema;
USE rent_schema;

-- RESET DAS TABELAS

DROP TABLE IF EXISTS Pagamento;
DROP TABLE IF EXISTS Aluguel;
DROP TABLE IF EXISTS Carro;
DROP TABLE IF EXISTS Modelo;
DROP TABLE IF EXISTS Cliente;

-- CRIAÇÃO DAS TABELAS

CREATE TABLE Cliente (
    ID_cliente INT NOT NULL AUTO_INCREMENT,
    CPF VARCHAR(14) NOT NULL,
    Nome VARCHAR(100) NOT NULL,
    CNH VARCHAR(20),
    Telefone VARCHAR(20),
    senha_hash VARCHAR(255) NOT NULL,
    cargo ENUM('user', 'admin') NOT NULL DEFAULT 'user',
    PRIMARY KEY (ID_cliente),
    UNIQUE KEY uq_cliente_cpf (CPF)
);

CREATE TABLE Modelo (
    ID_Modelo INT NOT NULL AUTO_INCREMENT,
    Marca VARCHAR(50) NOT NULL,
    Descricao VARCHAR(100) NOT NULL,
    Categoria VARCHAR(50) NOT NULL,
    Valor_Diaria DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (ID_Modelo),
    UNIQUE KEY uq_modelo (Marca, Descricao, Categoria)
);

CREATE TABLE Carro (
    Placa CHAR(7) NOT NULL,
    Chassi VARCHAR(30) UNIQUE,
    Cor VARCHAR(20) NOT NULL,
    Ano SMALLINT NOT NULL,
    Quilometragem INT NOT NULL DEFAULT 0,
    Status ENUM('disponivel', 'alugado', 'manutencao', 'inativo') NOT NULL DEFAULT 'disponivel',
    fk_Modelo_ID_Modelo INT NOT NULL,
    PRIMARY KEY (Placa),
    CONSTRAINT fk_carro_modelo
        FOREIGN KEY (fk_Modelo_ID_Modelo)
        REFERENCES Modelo (ID_Modelo)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE Aluguel (
    ID_Aluguel INT NOT NULL AUTO_INCREMENT,
    Data_Inicio DATETIME NOT NULL,
    Data_Fim DATETIME,
    Data_devolucao_real DATETIME,
    Valor_Total DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    Status_Aluguel ENUM('pendente','pago','cancelado') NOT NULL DEFAULT 'pendente',
    fk_Cliente_ID_cliente INT NOT NULL,
    fk_Carro_Placa CHAR(7) NOT NULL,
    PRIMARY KEY (ID_Aluguel),
    CONSTRAINT fk_aluguel_cliente
        FOREIGN KEY (fk_Cliente_ID_cliente)
        REFERENCES Cliente (ID_cliente)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_aluguel_carro
        FOREIGN KEY (fk_Carro_Placa)
        REFERENCES Carro (Placa)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
);

CREATE TABLE Pagamento (
    ID_Pagamento INT NOT NULL AUTO_INCREMENT,
    ID_Aluguel INT NOT NULL,
    Valor DECIMAL(10,2) NOT NULL,
    Data_Pagamento DATE NOT NULL,
    Forma_Pagamento ENUM('dinheiro','pix','credito','debito','boleto') NOT NULL,
    PRIMARY KEY (ID_Pagamento),
    CONSTRAINT fk_pagamento_aluguel
        FOREIGN KEY (ID_Aluguel)
        REFERENCES Aluguel (ID_Aluguel)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- INSERÇÃO DE DADOS INICIAIS

INSERT INTO Cliente (CPF, Nome, Endereco, senha_hash, cargo) VALUES (
    '00000000000',
    'Administrador do Sistema',
    'Sistema',
    '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9',
    'admin'
);

INSERT INTO Modelo (Marca, Descricao, Categoria, Valor_Diaria) VALUES
('Toyota', 'Corolla', 'sedan', 120.00),
('Fiat', 'Argo', 'hatch', 100.00),
('Chevrolet', 'S10', 'picape', 150.00),
('Honda', 'Civic', 'sedan', 130.00),
('Volkswagen', 'Gol', 'hatch', 90.00),
('Chevrolet', 'Onix', 'hatch', 95.00),
('Jeep', 'Renegade', 'suv', 140.00),
('Hyundai', 'Creta', 'suv', 135.00)
ON DUPLICATE KEY UPDATE Categoria = VALUES(Categoria);

INSERT IGNORE INTO Carro (Placa, Chassi, Cor, Ano, Quilometragem, Status, fk_Modelo_ID_Modelo) VALUES
('ABC1D23', 'CHASSI12345678901', 'Prata', 2022, 15000, 'disponivel', (SELECT ID_Modelo FROM Modelo WHERE Marca='Toyota' AND Descricao='Corolla')),
('DEF4G56', 'CHASSI98765432109', 'Branco', 2021, 32000, 'disponivel', (SELECT ID_Modelo FROM Modelo WHERE Marca='Fiat' AND Descricao='Argo')),
('HIJ7K89', 'CHASSI11223344556', 'Preto', 2023, 5000, 'manutencao', (SELECT ID_Modelo FROM Modelo WHERE Marca='Chevrolet' AND Descricao='Onix'));


-- COMANDOS DE RELATÓRIO

-- 1. Top 10 carros mais alugados
SELECT
  c.Placa,
  m.Marca,
  m.Descricao AS Modelo,
  COUNT(a.ID_Aluguel) AS Total_Alugueis
FROM Carro c
JOIN Modelo m ON m.ID_Modelo = c.fk_Modelo_ID_Modelo
JOIN Aluguel a ON a.fk_Carro_Placa = c.Placa
WHERE a.Status_Aluguel = 'pago'
GROUP BY c.Placa, m.Marca, m.Descricao
ORDER BY Total_Alugueis DESC
LIMIT 10;

-- 2. Resumo de pagamentos por forma de pagamento
SELECT
  p.Forma_Pagamento,
  COUNT(*) AS Qtde_Pagamentos,
  SUM(p.Valor) AS Total_Recebido,
  AVG(p.Valor) AS Ticket_Medio
FROM Pagamento p
GROUP BY p.Forma_Pagamento
ORDER BY Total_Recebido DESC;

-- 3. Menor e maior valor de diária entre carros disponíveis
SELECT
  MIN(m.Valor_Diaria) AS Menor_Diaria,
  MAX(m.Valor_Diaria) AS Maior_Diaria
FROM Carro c
JOIN Modelo m ON m.ID_Modelo = c.fk_Modelo_ID_Modelo
WHERE c.Status = 'disponivel';

-- 4. Carros disponíveis com diária entre R$80 e R$150
SELECT
  c.Placa,
  m.Marca,
  m.Descricao AS Modelo,
  m.Categoria,
  m.Valor_Diaria
FROM Carro c
JOIN Modelo m ON m.ID_Modelo = c.fk_Modelo_ID_Modelo
WHERE c.Status = 'disponivel'
  AND m.Valor_Diaria BETWEEN 80 AND 150
ORDER BY m.Valor_Diaria ASC;

-- 5. Modelos com 'a' na descrição
SELECT
  m.ID_Modelo,
  m.Marca,
  m.Descricao,
  m.Categoria,
  m.Valor_Diaria
FROM Modelo m
WHERE m.Descricao LIKE '%a%'
ORDER BY m.Marca, m.Descricao;