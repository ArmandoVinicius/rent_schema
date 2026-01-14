from app.database.connection import DatabaseConnection

class AluguelModel:
    def create_aluguel(self, data_inicio: str, data_fim: str, valor_total: float, data_devolucao_real: str | None, fk_cliente_id_cliente: int, fk_carro_placa: str, matricula: int):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Aluguel (Data_Inicio, Data_Fim, Valor_Total, Data_devolucao_real, fk_Cliente_ID_cliente, fk_Carro_Placa, Matricula)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (data_inicio, data_fim, valor_total, data_devolucao_real, fk_cliente_id_cliente, fk_carro_placa, matricula))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def get_aluguel_by_id(self, id_aluguel: int) -> bool:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT ID_Aluguel FROM Aluguel WHERE ID_Aluguel = %s", (id_aluguel,))
            result = cursor.fetchone()
            return result is not None
        finally:
            cursor.close()
            conn.close()

    def update_aluguel(self, id_aluguel: int, field: str, value: str | int | float):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(f"UPDATE Aluguel SET {field} = %s WHERE ID_Aluguel = %s", (value, id_aluguel))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def delete_aluguel(self, id_aluguel: int):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Aluguel WHERE ID_Aluguel = %s", (id_aluguel,))
            conn.commit()
        finally:
            cursor.close()
            conn.close()