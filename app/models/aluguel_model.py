# src/models/aluguel_model.py
from ..database.connection import DatabaseConnection

class AluguelModel:
  def __init__(self):
    pass
  
  def create_aluguel(self, data_inicio: str, data_fim: str, valor_total: float, data_devolucao_real: str | None, fk_cliente_id_cliente: int, fk_carro_placa: str, matricula: int):
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
      INSERT INTO Aluguel (Data_Inicio, Data_Fim, Valor_Total, Data_devolucao_real, fk_Cliente_ID_cliente, fk_Carro_Placa, Matricula)
      VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (data_inicio, data_fim, valor_total, data_devolucao_real, fk_cliente_id_cliente, fk_carro_placa, matricula))

    conn.commit()
    cursor.close()
    conn.close()

  def get_aluguel_by_id(self, id_aluguel: int) -> bool:
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ID_Aluguel FROM Aluguel WHERE ID_Aluguel = ?", (id_aluguel,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()
    return result is not None

  def update_aluguel(self, id_aluguel: int, field: str, value: str | int | float):
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE Aluguel SET {field} = ? WHERE ID_Aluguel = ?", (value, id_aluguel))
    conn.commit()
    cursor.close()
    conn.close()

  def delete_aluguel(self, id_aluguel: int):
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM Aluguel WHERE ID_Aluguel = ?", (id_aluguel,))
    conn.commit()
    cursor.close()
    conn.close()
