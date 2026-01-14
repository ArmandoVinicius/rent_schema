from app.database.connection import DatabaseConnection

class UserModel:
    def create_user(self, cpf: str, nome: str, cnh: str, telefone: str, senha_hash: str):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Cliente (CPF, Nome, CNH, Telefone, senha_hash)
                VALUES (%s, %s, %s, %s, %s)
            """, (cpf, nome, cnh, telefone, senha_hash))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def get_user_by_cpf(self, cpf: str) -> dict | None:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM Cliente WHERE CPF = %s", (cpf,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def update_user(self, cpf: str, field: str, value: str | int | float):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(f"UPDATE Cliente SET {field} = %s WHERE CPF = %s", (value, cpf))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def delete_user(self, cpf: str):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Cliente WHERE CPF = %s", (cpf,))
            conn.commit()
        finally:
            cursor.close()
            conn.close()