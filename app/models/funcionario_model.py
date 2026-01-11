# src/models/funcionario_model.py
from ..database.connection import DatabaseConnection

class FuncionarioModel:
  def __init__(self):
    pass
  
  def create_funcionario(self, nome: str, data_admissao: str, cargo: str):
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
      INSERT INTO Funcionario (Nome, Data_Admissao, Cargo)
      VALUES (?, ?, ?)
    """, (nome, data_admissao, cargo))

    conn.commit()
    cursor.close()
    conn.close()

  def get_funcionario_by_matricula(self, matricula: int) -> bool:
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Matricula FROM Funcionario WHERE Matricula = ?", (matricula,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()
    return result is not None

  def update_funcionario(self, matricula: int, field: str, value: str | int | float):
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE Funcionario SET {field} = ? WHERE Matricula = ?", (value, matricula))
    conn.commit()
    cursor.close()
    conn.close()

  def delete_funcionario(self, matricula: int):
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM Funcionario WHERE Matricula = ?", (matricula,))
    conn.commit()
    cursor.close()
    conn.close()
