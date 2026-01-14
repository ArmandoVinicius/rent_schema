from app.database.connection import DatabaseConnection

def create_tables():
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()

    try:
        stmts = [
            # ----------------
            # SCHEMA
            # ----------------
            """CREATE SCHEMA IF NOT EXISTS rent_schema;""",

            """USE rent_schema;""",

            # ----------------
            # DROP TABLES (ordem correta: filhas -> pais)
            # ----------------
            """DROP TABLE IF EXISTS Pagamento;""",
            """DROP TABLE IF EXISTS Aluguel;""",
            """DROP TABLE IF EXISTS Carro;""",
            """DROP TABLE IF EXISTS Modelo;""",
            """DROP TABLE IF EXISTS Funcionario;""",
            """DROP TABLE IF EXISTS Cliente;""",

            # ----------------
            # CLIENTE
            # ----------------
            """CREATE TABLE IF NOT EXISTS Cliente (
                ID_cliente INT NOT NULL AUTO_INCREMENT,
                CPF VARCHAR(14) NOT NULL,
                Nome VARCHAR(100) NOT NULL,
                CNH VARCHAR(20),
                Telefone VARCHAR(20),
                Endereco VARCHAR(150),
                senha_hash VARCHAR(255) NOT NULL,
                cargo ENUM('user', 'admin') NOT NULL DEFAULT 'user',

                PRIMARY KEY (ID_cliente),
                UNIQUE KEY uq_cliente_cpf (CPF)
            );""",

            # ----------------
            # FUNCIONARIO
            # ----------------
            """CREATE TABLE IF NOT EXISTS Funcionario (
                Matricula INT NOT NULL AUTO_INCREMENT,
                Nome VARCHAR(100) NOT NULL,
                Data_Admissao DATE NOT NULL,
                Cargo VARCHAR(50) NOT NULL,

                PRIMARY KEY (Matricula)
            );""",

            # ----------------
            # MODELO
            # ----------------
            """CREATE TABLE IF NOT EXISTS Modelo (
                ID_Modelo INT NOT NULL AUTO_INCREMENT,
                Marca VARCHAR(50) NOT NULL,
                Descricao VARCHAR(100) NOT NULL,
                Categoria VARCHAR(50) NOT NULL,
                Valor_Diaria DECIMAL(10,2) NOT NULL,

                PRIMARY KEY (ID_Modelo),
                UNIQUE KEY uq_modelo (Marca, Descricao, Categoria)
            );""",

            # ----------------
            # CARRO
            # ----------------
            """CREATE TABLE IF NOT EXISTS Carro (
                Placa CHAR(7) NOT NULL,
                Chassi VARCHAR(30) UNIQUE,
                Cor VARCHAR(20) NOT NULL,
                Ano SMALLINT NOT NULL,
                Quilometragem INT NOT NULL DEFAULT 0,
                Status ENUM('disponivel', 'alugado', 'manutencao', 'inativo') 
                    NOT NULL DEFAULT 'disponivel',
                fk_Modelo_ID_Modelo INT NOT NULL,

                PRIMARY KEY (Placa),

                CONSTRAINT fk_carro_modelo
                    FOREIGN KEY (fk_Modelo_ID_Modelo)
                    REFERENCES Modelo (ID_Modelo)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT
            );""",

            # ----------------
            # ALUGUEL
            # ----------------
            """CREATE TABLE IF NOT EXISTS Aluguel (
                ID_Aluguel INT NOT NULL AUTO_INCREMENT,
                Data_Inicio DATETIME NOT NULL,
                Data_Fim DATETIME,
                Data_devolucao_real DATETIME,
                Valor_Total DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                Status_Aluguel ENUM('pendente','pago','cancelado') NOT NULL DEFAULT 'pendente',

                fk_Cliente_ID_cliente INT NOT NULL,
                fk_Carro_Placa CHAR(7) NOT NULL,
                Matricula INT NULL,
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

                CONSTRAINT fk_aluguel_funcionario
                    FOREIGN KEY (Matricula)
                    REFERENCES Funcionario (Matricula)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT
            );""",

            # ----------------
            # PAGAMENTO
            # ----------------
            """CREATE TABLE IF NOT EXISTS Pagamento (
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
            );""",

            # ----------------
            # ADMIN PADRÃO
            # CPF: 00000000000
            # Senha: admin123
            # SHA-256: 240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9
            # ----------------
            """INSERT INTO Cliente (
                CPF, Nome, senha_hash, cargo
            ) VALUES (
                '00000000000',
                'Administrador do Sistema',
                '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9',
                'admin'
            )
            ON DUPLICATE KEY UPDATE
                cargo = 'admin';""",
            
            """INSERT INTO Modelo (Marca, Descricao, Categoria, Valor_Diaria)
                VALUES
                ('Toyota', 'Corolla', 'sedan', 120.00),
                ('Fiat', 'Argo', 'hatch', 100.00),
                ('Chevrolet', 'S10', 'picape', 150.00),
                ('Honda', 'Civic', 'sedan', 130.00),
                ('Volkswagen', 'Gol', 'hatch', 90.00),
                ('Chevrolet', 'Onix', 'hatch', 95.00),
                ('Jeep', 'Renegade', 'suv', 140.00),
                ('Hyundai', 'Creta', 'suv', 135.00)
            ON DUPLICATE KEY UPDATE Categoria = VALUES(Categoria);""",
            
            """INSERT INTO Carro (
                Placa,
                Chassi,
                Cor,
                Ano,
                Quilometragem,
                Status,
                fk_Modelo_ID_Modelo
            ) VALUES
            (
                'ABC1D23',
                'CHASSI12345678901',
                'Prata',
                2022,
                15000,
                'disponivel',
                (SELECT ID_Modelo FROM Modelo WHERE Marca='Toyota' AND Descricao='Corolla')
            ),
            (
                'DEF4G56',
                'CHASSI98765432109',
                'Branco',
                2021,
                32000,
                'disponivel',
                (SELECT ID_Modelo FROM Modelo WHERE Marca='Fiat' AND Descricao='Argo')
            ),
            (
                'HIJ7K89',
                'CHASSI11223344556',
                'Preto',
                2023,
                5000,
                'manutencao',
                (SELECT ID_Modelo FROM Modelo WHERE Marca='Chevrolet' AND Descricao='Onix')
            );
            """
        ]

        for sql in stmts:
            cursor.execute(sql)

        conn.commit()

    except Exception:
        try:
            conn.rollback()
        except Exception:
            pass
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_tables()