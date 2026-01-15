from app.database.connection import DatabaseConnection

class RentalModel:
    def has_date_conflict(self, placa: str, data_inicio: str, data_fim: str) -> bool:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT 1 FROM Aluguel
                WHERE fk_Carro_Placa = %s
                  AND Status_Aluguel IN ('pendente','pago')
                  AND Data_Inicio < %s
                  AND %s < Data_Fim
                LIMIT 1
            """, (placa, data_fim, data_inicio))
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            conn.close()

    def create_pending_rent(self, cliente_id: int, placa: str, data_inicio: str, data_fim: str, valor_total: float) -> int:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Aluguel
                    (Data_Inicio, Data_Fim, Valor_Total, Data_devolucao_real,
                     fk_Cliente_ID_cliente, fk_Carro_Placa, Matricula, Status_Aluguel)
                VALUES
                    (%s, %s, %s, NULL, %s, %s, NULL, 'pendente')
            """, (data_inicio, data_fim, valor_total, cliente_id, placa))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    def get_car_for_rent(self, placa: str):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT c.Placa, c.Status, m.Valor_Diaria
                FROM Carro c
                JOIN Modelo m ON m.ID_Modelo = c.fk_Modelo_ID_Modelo
                WHERE c.Placa = %s
            """, (placa,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def get_rent_by_id(self, aluguel_id: int) -> dict | None:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT ID_Aluguel, Valor_Total, fk_Carro_Placa, Status_Aluguel
                FROM Aluguel
                WHERE ID_Aluguel = %s
            """, (aluguel_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def insert_payment(self, aluguel_id: int, valor: float, data_pagamento: str, forma: str) -> None:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Pagamento (ID_Aluguel, Valor, Data_Pagamento, Forma_Pagamento)
                VALUES (%s, %s, %s, %s)
            """, (aluguel_id, valor, data_pagamento, forma))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def set_rent_paid(self, aluguel_id: int) -> None:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE Aluguel SET Status_Aluguel = 'pago' WHERE ID_Aluguel = %s", (aluguel_id,))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def set_car_status(self, placa: str, status: str) -> None:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE Carro SET Status = %s WHERE Placa = %s", (status, placa))
            conn.commit()
        finally:
            cursor.close()
            conn.close()