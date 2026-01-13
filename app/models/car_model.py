# src/models/car_model.py
from app.database.connection import DatabaseConnection

class CarModel:
  ALLOWED_UPDATE_FIELDS = {"Placa", "Cor", "Ano", "Quilometragem", "Status"}
  def __init__(self):
    pass
  
  def create_car(self, placa: str, chassi: str, cor: str, ano: int, quilometragem: int, status: str, id_modelo: int):
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
      INSERT INTO Carro (Placa, Chassi, Cor, Ano, Quilometragem, Status, fk_Modelo_ID_Modelo)
      VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (placa, chassi, cor, ano, quilometragem, status, id_modelo))

    conn.commit()
    cursor.close()
    conn.close()

  def get_car_by_placa(self, placa: str) -> bool:
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Placa FROM Carro WHERE Placa = %s", (placa,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()
    return result is not None

  def delete_car(self, placa: str):
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM Carro WHERE Placa = %s", (placa,))
    conn.commit()
    cursor.close()
    conn.close()
    
  def list_cars(self) -> list[dict]:
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            c.Placa,
            c.Ano,
            c.Status,
            c.Cor,
            c.Quilometragem,
            m.Marca,
            m.Descricao,
            m.Categoria
        FROM Carro c
        JOIN Modelo m ON m.ID_Modelo = c.fk_Modelo_ID_Modelo
        ORDER BY c.Placa
    """)

    car_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return car_list
  
  def get_car_details(self, placa: str) -> dict | None:
      conn = DatabaseConnection.get_connection()
      cursor = conn.cursor(dictionary=True)
      try:
          cursor.execute("""
              SELECT
                  c.Placa, c.Chassi, c.Cor, c.Ano, c.Quilometragem, c.Status, c.fk_Modelo_ID_Modelo,
                  m.Marca, m.Descricao, m.Categoria
              FROM Carro c
              JOIN Modelo m ON m.ID_Modelo = c.fk_Modelo_ID_Modelo
              WHERE c.Placa = %s
          """, (placa,))
          row = cursor.fetchone()
          if not row:
              return None

          # texto amigável para o combobox
          row["ModeloTexto"] = f"{row['Marca']} {row['Descricao']} — {row['Categoria']}"
          return row
      finally:
          cursor.close()
          conn.close()

  def update_car_fields(self, placa: str, data: dict) -> None:
      # monta UPDATE seguro (com whitelist)
      fields = []
      values = []

      for k, v in data.items():
          if k in self.ALLOWED_UPDATE_FIELDS:
              fields.append(f"{k} = %s")
              values.append(v)

      if not fields:
          return

      values.append(placa)

      sql = f"UPDATE Carro SET {', '.join(fields)} WHERE Placa = %s"

      conn = DatabaseConnection.get_connection()
      cursor = conn.cursor()
      try:
          cursor.execute(sql, tuple(values))
          conn.commit()
      finally:
          cursor.close()
          conn.close()
