# src/models/car_model.py
from ..database.connection import DatabaseConnection

class CarModel:
  def __init__(self):
    pass
  
  def create_car(self, placa: str, chassi: str, cor: str, ano: int, quilometragem: int, status: str, ano_fabricacao: int, id_modelo: int):
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
      INSERT INTO Carro (Placa, Chassi, Cor, Ano, Quilometragem, Status, ano_fabricacao, fk_Modelo_ID_Modelo)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (placa, chassi, cor, ano, quilometragem, status, ano_fabricacao, id_modelo))

    conn.commit()
    cursor.close()
    conn.close()

  def get_car_by_placa(self, placa: str) -> bool:
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Placa FROM Carro WHERE Placa = ?", (placa,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()
    return result is not None

  def update_car(self, placa: str, field: str, value: str | int | float):
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE Carro SET {field} = ? WHERE Placa = ?", (value, placa))
    conn.commit()
    cursor.close()
    conn.close()

  def delete_car(self, placa: str):
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM Carro WHERE Placa = ?", (placa,))
    conn.commit()
    cursor.close()
    conn.close()