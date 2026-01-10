from database.connection import DatabaseConnection

# Roda separado!

def create_tables():
  conn = DatabaseConnection.get_connection()
  cursor = conn.cursor()
  
  try:
    cursor.execute("""CREATE SCHEMA IF NOT EXISTS rent_schema;

USE rent_schema;

CREATE TABLE Cliente (
    CPF VARCHAR(14) UNIQUE,
    Nome VARCHAR(100),
    CNH VARCHAR(20),
    Telefone VARCHAR(20),
    ID_cliente INTEGER PRIMARY KEY,
    Endereco VARCHAR(150)
);

CREATE TABLE Funcionario (
    Matricula INTEGER PRIMARY KEY,
    Nome VARCHAR(100),
    Data_Admissao DATE,
    Cargo VARCHAR(50)
);

CREATE TABLE Carro (
    Placa CHAR(7) PRIMARY KEY,
    Chassi VARCHAR(30),
    Cor VARCHAR(20),
    Ano INTEGER,
    Quilometragem INTEGER,
    Status VARCHAR(20),
    ano_fabricacao INTEGER,
    fk_Modelo_ID_Modelo INTEGER
);

CREATE TABLE Modelo (
    ID_Modelo INTEGER PRIMARY KEY,
    Descricao VARCHAR(100),
    Marca VARCHAR(50),
    Categoria VARCHAR(50)
);

CREATE TABLE Aluguel (
    ID_Aluguel INTEGER PRIMARY KEY,
    Data_Inicio DATETIME,
    Data_Fim DATETIME,
    Valor_Total DECIMAL(10,2),
    Data_devolucao_real DATETIME,
    fk_Cliente_ID_cliente INTEGER,
    fk_Carro_Placa CHAR(7),
    Matricula INTEGER
);

CREATE TABLE Pagamento (
    ID_Pagamento INTEGER PRIMARY KEY,
    Valor DECIMAL(10,2),
    Data_Pagamento DATE,
    Forma_Pagamento VARCHAR(50),
    ID_Aluguel INTEGER
);

ALTER TABLE Carro ADD CONSTRAINT FK_Carro_2
    FOREIGN KEY (fk_Modelo_ID_Modelo)
    REFERENCES Modelo (ID_Modelo);

ALTER TABLE Aluguel ADD CONSTRAINT FK_Aluguel_2
    FOREIGN KEY (fk_Cliente_ID_cliente)
    REFERENCES Cliente (ID_cliente)
    ON DELETE CASCADE;

ALTER TABLE Aluguel ADD CONSTRAINT FK_Aluguel_3
    FOREIGN KEY (fk_Carro_Placa)
    REFERENCES Carro (Placa)
    ON DELETE CASCADE;

ALTER TABLE Aluguel ADD CONSTRAINT FK_Aluguel_4
    FOREIGN KEY (Matricula)
    REFERENCES Funcionario (Matricula);

ALTER TABLE Pagamento ADD CONSTRAINT FK_Pagamento_2
    FOREIGN KEY (ID_Aluguel)
    REFERENCES Aluguel (ID_Aluguel);""")

    conn.commit()
  except Exception as e:
    conn.rollback()
    print(e)

create_tables()