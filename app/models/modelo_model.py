# app/models/modelo_model.py
from app.database.connection import DatabaseConnection

class ModeloModel:
    ALLOWED_FIELDS = {"Descricao", "Marca", "Categoria", "Valor_Diaria"}

    def create_modelo(self, descricao: str, marca: str, categoria: str, valor_diaria: float):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Modelo (Descricao, Marca, Categoria, Valor_Diaria)
                VALUES (%s, %s, %s, %s)
            """, (descricao, marca, categoria, valor_diaria))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def list_modelos(self) -> list[dict]:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT ID_Modelo, Marca, Descricao, Categoria, Valor_Diaria
                FROM Modelo
                ORDER BY Marca, Descricao
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_modelo_by_id(self, id_modelo: int) -> dict | None:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT ID_Modelo, Marca, Descricao, Categoria, Valor_Diaria
                FROM Modelo
                WHERE ID_Modelo = %s
            """, (id_modelo,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def update_modelo(self, id_modelo: int, field: str, value):
        if field not in self.ALLOWED_FIELDS:
            raise ValueError(f"Campo inválido: {field}")

        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(f"""
                UPDATE Modelo
                SET {field} = %s
                WHERE ID_Modelo = %s
            """, (value, id_modelo))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def delete_modelo(self, id_modelo: int):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Modelo WHERE ID_Modelo = %s", (id_modelo,))
            conn.commit()
        finally:
            cursor.close()
            conn.close()
