from app.utils.ui import clear_root
from app.views.dashboard_view import DashboardView
from app.core.services.car_service import CarService
from app.core.services.modelo_service import ModeloService

class AddCarController:
    def __init__(self, root):
        self.root = root
        self.view = None
        self.car_service = CarService()
        self.modelo_service = ModeloService()

    def set_view(self, view):
        self.view = view
        modelos = self.modelo_service.list_modelos()
        self.view.set_modelos(modelos)

    def save_car(self):
        try:
            data = self.view.get_form_data()
            ok, msg = self.car_service.create_car(**data)

            if ok:
                self.view.show_info("Sucesso", msg)
                self.back_to_dashboard()
            else:
                self.view.show_error("Erro", msg)
        except ValueError as e:
            self.view.show_error("Atenção", str(e))

    def back_to_dashboard(self):
        from app.controllers.dashboard_controller import DashboardController
        clear_root(self.root)
        DashboardView(self.root, DashboardController(self.root))