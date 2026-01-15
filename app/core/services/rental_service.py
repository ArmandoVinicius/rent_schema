from datetime import datetime, date
from app.core import session
from app.models.rental_model import RentalModel

class RentalService:
    VALID_FORMS = {"dinheiro", "pix", "credito", "debito", "boleto"}

    def __init__(self):
        self.model = RentalModel()

    def _parse_date(self, s: str) -> date:
        return datetime.strptime(s, "%Y-%m-%d").date()

    def check_availability(self, placa: str, data_inicio: str, data_fim: str) -> tuple[bool, str]:
        try:
            di = self._parse_date(data_inicio)
            df = self._parse_date(data_fim)
        except ValueError:
            return False, "Datas inválidas. Use o formato YYYY-MM-DD."

        if df <= di:
            return False, "A data final deve ser maior que a data inicial."

        if self.model.has_date_conflict(placa, data_inicio, data_fim):
            return False, "Carro indisponível no período selecionado."

        return True, "Disponível!"

    def create_pending_rent(self, placa: str, data_inicio: str, data_fim: str):
        user = session.current_user
        if not user:
            return False, "Você precisa estar logado.", None

        try:
            car = self.model.get_car_for_rent(placa)
            if not car:
                return False, "Carro não encontrado.", None
            
            status = (car.get("Status") or "").lower()
            if status in ("inativo", "manutencao"):
                return False, f"Não é possível alugar, status do carro: '{status}'.", None
            
            # Tenta pegar o ID de várias formas possíveis dependendo do retorno do banco
            cliente_id = user.get("ID_Cliente") or user.get("id_cliente") or user.get("ID_cliente")
            if not cliente_id:
                return False, "Sessão inválida: ID do cliente não encontrado.", None

            ok, msg = self.check_availability(placa, data_inicio, data_fim)
            if not ok:
                return False, msg, None

            di = self._parse_date(data_inicio)
            df = self._parse_date(data_fim)
            dias = (df - di).days
            if dias < 1: dias = 1 # Mínimo 1 diária
            
            diaria = float(car["Valor_Diaria"])
            valor_total = dias * diaria

            aluguel_id = self.model.create_pending_rent(int(cliente_id), placa, data_inicio, data_fim, valor_total)
            return True, "Reserva criada! Agora confirme o pagamento.", aluguel_id

        except Exception as e:
            return False, f"Erro ao criar reserva: {e}", None

    def confirm_payment(self, aluguel_id: int, forma: str) -> tuple[bool, str]:
        if forma not in self.VALID_FORMS:
            return False, "Forma de pagamento inválida."

        try:
            rent = self.model.get_rent_by_id(aluguel_id)
            if not rent:
                return False, "Aluguel não encontrado."

            if rent.get("Status_Aluguel") == "pago":
                return False, "Este aluguel já está pago."

            valor = float(rent.get("Valor_Total") or 0.0)
            placa = rent.get("fk_Carro_Placa")
            today_str = date.today().strftime("%Y-%m-%d")

            self.model.insert_payment(aluguel_id, valor, today_str, forma)
            self.model.set_rent_paid(aluguel_id)
            self.model.set_car_status(placa, "alugado")

            return True, "Pagamento confirmado! Carro reservado como alugado."
        except Exception as e:
            return False, f"Erro ao processar pagamento: {e}"