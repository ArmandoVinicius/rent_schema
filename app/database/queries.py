from database.connection import DatabaseConnection

def get_connection():
  db = DatabaseConnection()
  conn = db.connect()
  return conn, conn.cursor()

def get_users():
  conn, cursor = get_connection()
  cursor.execute("SELECT * FROM usuarios")
  result = cursor.fetchall()
  cursor.close()
  conn.close()
  return result

def create_user(nome: str, email: str, senha_hash: str):
  conn, cursor = get_connection()
  cursor.execute("INSERT INTO clientes (nome, email, senha)VALUES (?, ?, ?)", (nome, email, senha_hash))
  conn.commit()
  cursor.close()
  conn.close()

def user_exists(email: str) -> bool:
  conn, cursor = get_connection()
  cursor.execute("SELECT id FROM clientes WHERE email = ?", (email,))
  result = cursor.fetchone()
  cursor.close()
  conn.close()
  return result is not None