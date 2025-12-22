from database.connection import DatabaseConnection

# Roda separado!

def create_tables():
  conn = DatabaseConnection.get_connection()
  cursor = conn.cursor()
  
  try:
    cursor.execute("""CREATE TABLE IF NOT EXISTS carros (
      id INTEGER AUTO_INCREMENT,
      modelo TEXT NOT NULL,
      marca TEXT NOT NULL,
      ano INTEGER NOT NULL,
      placa TEXT UNIQUE NOT NULL,
      categoria TEXT,
      km_atual INTEGER,
      status TEXT DEFAULT 'disponivel',
      primary key(id)
    );""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS clientes (
      id INTEGER PRIMARY KEY AUTO_INCREMENT,
      nome TEXT NOT NULL,
      cpf TEXT UNIQUE,
      telefone TEXT,
      email TEXT,
      senha TEXT
  );""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS alugueis (
      id INTEGER PRIMARY KEY AUTO_INCREMENT,
      id_cliente INTEGER NOT NULL,
      id_carro INTEGER NOT NULL,
      data_inicio DATE NOT NULL,
      data_fim DATE,
      valor_diaria REAL NOT NULL,
      status TEXT DEFAULT 'ativo',  -- ativo, finalizado, cancelado
      FOREIGN KEY(id_cliente) REFERENCES clientes(id),
      FOREIGN KEY(id_carro) REFERENCES carros(id)
  );""")
    conn.commit()
  except Exception as e:
    conn.rollback()