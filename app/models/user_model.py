# src/models/user_model.py
from database.connection import DatabaseConnection

class UserModel:
  def __init__(self):
    pass
  
  def create_user(self, cpf: str, nome: str, cnh: str, telefone: str, senha_hash: str):
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
      INSERT INTO Cliente (CPF, Nome, CNH, Telefone, senha)
      VALUES (?, ?, ?, ?, ?)
    """, (cpf, nome, cnh, telefone, senha_hash))

    conn.commit()
    cursor.close()
    conn.close()

  def get_user_by_cpf(self, cpf: str) -> bool:
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ID_cliente FROM Cliente WHERE cpf = ?", (cpf,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()
    return result is not None
