from app.models.car_model import CarModel
from app.core import session

class CarService:
    VALID_STATUS = {"disponivel", "alugado", "manutencao", "inativo"}
    REQUIRED_FIELDS = ["placa", "chassi", "cor", "ano", "quilometragem", "status", "id_modelo"]
  
    def __init__(self):
        self.model = CarModel()

    def list_cars(self) -> list[dict]:
        try:
            return self.model.list_cars()
        except Exception:
            return []

    def get_car_by_placa(self, placa: str) -> dict | None:
        try:
            return self.model.get_car_by_placa(placa)
        except Exception:
            return None
  
    def create_car(self, **data):
        user = session.current_user
        if not user or user.get("cargo") != "admin":
            return False, "Apenas administradores podem adicionar carros."

        for field in self.REQUIRED_FIELDS:
            if field not in data or data[field] in [None, ""]:
                return False, f"O campo '{field}' é obrigatório."
        
        try:
            self.model.create_car(**data)
            return True, "Carro cadastrado com sucesso!"
        except Exception as e:
            return False, f"Erro ao criar carro: {e}"

    def get_car_details(self, placa: str) -> dict | None:
        try:
            return self.model.get_car_details(placa)
        except Exception:
            return None

    def update_car_fields(self, placa: str, data: dict):
        user = session.current_user
        if not user or user.get("cargo") != "admin":
            return False, "Apenas administradores podem alterar carros."

        if data.get("Status") not in self.VALID_STATUS:
            return False, "Status inválido."

        if not data.get("fk_Modelo_ID_Modelo"):
            return False, "Selecione um modelo válido."

        try:
            if int(data.get("Ano", 0)) < 1900:
                return False, "Ano inválido."
            if int(data.get("Quilometragem", -1)) < 0:
                return False, "Quilometragem inválida."

            self.model.update_car_fields(placa, data)
            return True, "Carro atualizado com sucesso."
        except Exception as e:
            return False, f"Erro ao atualizar: {e}"
  
    def delete_car(self, placa: str):
        user = session.current_user
        if not user or user.get("cargo") != "admin":
            return False, "Apenas administradores podem deletar carros."

        try:
            self.model.delete_car(placa)
            return True, "Carro deletado com sucesso."
        except Exception as e:
            return False, f"Erro ao deletar: {e}"