from app.models.modelo_model import ModeloModel

class ModeloService:
    def __init__(self):
        self.model = ModeloModel()

    def list_modelos(self):
        try:
            return self.model.list_modelos()
        except Exception:
            return []

    def get_modelo_by_id(self, id_modelo: int):
        return self.model.get_modelo_by_id(id_modelo)

    def create_modelo(self, descricao: str, marca: str, categoria: str, valor_diaria: float):
        try:
            self.model.create_modelo(descricao, marca, categoria, valor_diaria)
            return True
        except Exception:
            raise

    def update_modelo(self, id_modelo: int, field: str, value):
        self.model.update_modelo(id_modelo, field, value)

    def delete_modelo(self, id_modelo: int):
        try:
            self.model.delete_modelo(id_modelo)
            return True, "Modelo excluído com sucesso."
        except Exception as e:
            msg = str(e).lower()
            if "1451" in msg or "foreign key constraint fails" in msg:
                return False, "Não é possível excluir: existe carro usando este modelo."
            return False, f"Erro ao excluir: {e}"