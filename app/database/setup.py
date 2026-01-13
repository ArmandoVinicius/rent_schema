from app.database.connection import DatabaseConnection

def create_tables():
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()

    try:
        stmts = [
            """CREATE SCHEMA IF NOT EXISTS rent_schema;""",

            """USE rent_schema;""",

            """CREATE TABLE IF NOT EXISTS Cliente (
                CPF VARCHAR(14) UNIQUE,
                Nome VARCHAR(100),
                CNH VARCHAR(20),
                Telefone VARCHAR(20),
                ID_cliente INTEGER PRIMARY KEY AUTO_INCREMENT,
                senha_hash VARCHAR(255) NOT NULL,
                Endereco VARCHAR(150)
            );""",

            """CREATE TABLE IF NOT EXISTS Funcionario (
                Matricula INTEGER PRIMARY KEY,
                Nome VARCHAR(100),
                Data_Admissao DATE,
                Cargo VARCHAR(50)
            );""",

            """CREATE TABLE IF NOT EXISTS Modelo (
                ID_Modelo INTEGER PRIMARY KEY,
                Descricao VARCHAR(100),
                Marca VARCHAR(50),
                Categoria VARCHAR(50)
            );""",

            """CREATE TABLE IF NOT EXISTS Carro (
                Placa CHAR(7) PRIMARY KEY,
                Chassi VARCHAR(30),
                Cor VARCHAR(20),
                Ano INTEGER,
                Quilometragem INTEGER,
                Status VARCHAR(20),
                ano_fabricacao INTEGER,
                fk_Modelo_ID_Modelo INTEGER,
                
                CONSTRAINT FK_Carro_2
                FOREIGN KEY (fk_Modelo_ID_Modelo)
                REFERENCES Modelo (ID_Modelo)
            );""",

            """CREATE TABLE IF NOT EXISTS Aluguel (
                ID_Aluguel INTEGER PRIMARY KEY,
                Data_Inicio DATETIME,
                Data_Fim DATETIME,
                Valor_Total DECIMAL(10,2),
                Data_devolucao_real DATETIME,
                fk_Cliente_ID_cliente INTEGER,
                fk_Carro_Placa CHAR(7),
                Matricula INTEGER,
                
                CONSTRAINT FK_Aluguel_2
                FOREIGN KEY (fk_Cliente_ID_cliente)
                REFERENCES Cliente (ID_cliente)
                ON DELETE CASCADE,
                
                CONSTRAINT FK_Aluguel_3
                FOREIGN KEY (fk_Carro_Placa)
                REFERENCES Carro (Placa)
                ON DELETE CASCADE,
                
                CONSTRAINT FK_Aluguel_4
                FOREIGN KEY (Matricula)
                REFERENCES Funcionario (Matricula)
            );""",

            """CREATE TABLE IF NOT EXISTS Pagamento (
                ID_Pagamento INTEGER PRIMARY KEY,
                Valor DECIMAL(10,2),
                Data_Pagamento DATE,
                Forma_Pagamento VARCHAR(50),
                ID_Aluguel INTEGER,
                
                CONSTRAINT FK_Pagamento_2
                FOREIGN KEY (ID_Aluguel)
                REFERENCES Aluguel (ID_Aluguel)
            );""",
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