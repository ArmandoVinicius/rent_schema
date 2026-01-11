# src/models/modelo_model.py
from ..database.connection import DatabaseConnection

class ModeloModel:
  def __init__(self):
    pass
  
  def create_modelo(self, descricao: str, marca: str, categoria: str):
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
      INSERT INTO Modelo (Descricao, Marca, Categoria)
      VALUES (?, ?, ?)
    """, (descricao, marca, categoria))

    conn.commit()
    cursor.close()
    conn.close()

  def get_modelo_by_id(self, id_modelo: int) -> bool:
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ID_Modelo FROM Modelo WHERE ID_Modelo = ?", (id_modelo,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()
    return result is not None

  def update_modelo(self, id_modelo: int, field: str, value: str | int | float):
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE Modelo SET {field} = ? WHERE ID_Modelo = ?", (value, id_modelo))
    conn.commit()
    cursor.close()
    conn.close()

  def delete_modelo(self, id_modelo: int):
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM Modelo WHERE ID_Modelo = ?", (id_modelo,))
    conn.commit()
    cursor.close()
    conn.close()
