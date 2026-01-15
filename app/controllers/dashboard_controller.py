from app.views.login_view import LoginView
from app.controllers.login_controller import LoginController
from app.controllers.add_car_controller import AddCarController
from app.views.add_car_view import AddCarView
from app.core.services.car_service import CarService
from app.core import session
from app.utils.ui import clear_root

class DashboardController:
    def __init__(self, root):
        self.root = root
        self.view = None
        self.car_service = CarService()

    def set_view(self, view):
        self.view = view
        is_admin = session.current_user.get("cargo") == "admin"
        self.view.set_admin_mode(is_admin)

    def load_cars(self):
        try:
            cars = self.car_service.list_cars()
            self.view.set_car_list(cars)
        except Exception as e:
            self.view.show_error("Erro", f"Falha ao carregar carros: {e}")

    def open_car_details(self):
        from app.views.car_details_view import CarDetailsView
        from app.controllers.car_details_controller import CarDetailsController
        
        placa = self.view.get_selected_car_placa()
        if not placa:
            self.view.show_warning("Atenção", "Selecione um carro para ver os detalhes.")
            return

        clear_root(self.root)
        CarDetailsView(self.root, CarDetailsController(self.root, placa))

    def open_add_car(self):
        user = session.current_user
        if not user or user.get("cargo") != "admin":
            self.view.show_error("Acesso negado", "Apenas administradores podem adicionar carros.")
            return

        clear_root(self.root)
        controller = AddCarController(self.root)
        AddCarView(self.root, controller)

    def delete_selected_car(self):
        placa = self.view.get_selected_car_placa()
        if not placa:
            self.view.show_warning("Atenção", "Selecione um carro para excluir.")
            return

        try:
            self.car_service.delete_car(placa)
            self.view.show_info("Sucesso", f"Carro com placa {placa} excluído.")
            self.load_cars()
        except Exception as e:
            self.view.show_error("Erro", f"Falha ao excluir carro: {e}")

    def open_modelos(self):
        user = session.current_user
        if not user or user.get("cargo") != "admin":
            self.view.show_error("Acesso negado", "Apenas administradores.")
            return

        clear_root(self.root)
        from app.controllers.modelos_controller import ModelosController
        from app.views.modelos_view import ModelosView
        ModelosView(self.root, ModelosController(self.root))

    def logout(self):
        clear_root(self.root)
        lc = LoginController(self.root)
        LoginView(self.root, lc)