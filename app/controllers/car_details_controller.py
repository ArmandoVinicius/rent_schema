from app.core import session
from app.utils.ui import clear_root
from app.core.services.car_service import CarService
from app.core.services.modelo_service import ModeloService

class CarDetailsController:
    def __init__(self, root, placa: str):
        self.root = root
        self.placa = placa
        self.view = None
        self.car_service = CarService()
        self.modelo_service = ModeloService()

    def set_view(self, view):
        self.view = view
        user = session.current_user
        is_admin = bool(user) and user.get("cargo") == "admin"
        self.view.set_mode(is_admin)

        modelos = self.modelo_service.list_modelos()
        self.view.set_modelos(modelos)

    def load_details(self):
        car = self.car_service.get_car_details(self.placa)
        if not car:
            self.view.show_error("Erro", "Carro não encontrado.")
            self.back_to_dashboard()
            return
        self.view.set_car_data(car)

    def open_rent(self):
        user = session.current_user
        if not user:
            self.view.show_error("Erro", "Você precisa estar logado.")
            return

        clear_root(self.root)
        from app.controllers.rent_controller import RentController
        from app.views.rent_view import RentView
        RentView(self.root, RentController(self.root, self.placa), self.placa)

    def save_updates(self):
        user = session.current_user
        if not user or user.get("cargo") != "admin":
            self.view.show_error("Acesso negado", "Apenas administradores podem alterar dados.")
            return

        try:
            data = self.view.get_update_data()
            ok, msg = self.car_service.update_car_fields(self.placa, data)
            if ok:
                self.view.show_info("Sucesso", msg)
                self.load_details()
            else:
                self.view.show_error("Erro", msg)
        except ValueError as e:
            self.view.show_warning("Atenção", str(e))
        except Exception as e:
            self.view.show_error("Erro", f"Falha ao salvar: {e}")

    def back_to_dashboard(self):
        clear_root(self.root)
        from app.controllers.dashboard_controller import DashboardController
        from app.views.dashboard_view import DashboardView
        DashboardView(self.root, DashboardController(self.root))