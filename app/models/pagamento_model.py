# src/models/pagamento_model.py
from ..database.connection import DatabaseConnection

class PagamentoModel:
  def __init__(self):
    pass
  
  def create_pagamento(self, valor: float, data_pagamento: str, forma_pagamento: str, id_aluguel: int):
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
      INSERT INTO Pagamento (Valor, Data_Pagamento, Forma_Pagamento, ID_Aluguel)
      VALUES (?, ?, ?, ?)
    """, (valor, data_pagamento, forma_pagamento, id_aluguel))

    conn.commit()
    cursor.close()
    conn.close()

  def get_pagamento_by_id(self, id_pagamento: int) -> bool:
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ID_Pagamento FROM Pagamento WHERE ID_Pagamento = ?", (id_pagamento,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()
    return result is not None

  def update_pagamento(self, id_pagamento: int, field: str, value: str | int | float):
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE Pagamento SET {field} = ? WHERE ID_Pagamento = ?", (value, id_pagamento))
    conn.commit()
    cursor.close()
    conn.close()

  def delete_pagamento(self, id_pagamento: int):
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM Pagamento WHERE ID_Pagamento = ?", (id_pagamento,))
    conn.commit()
    cursor.close()
    conn.close()
