from app.utils.ui import clear_root
from app.core.services.rental_service import RentalService

class PaymentController:
    def __init__(self, root, aluguel_id: int):
        self.root = root
        self.aluguel_id = aluguel_id
        self.view = None
        self.service = RentalService()

    def set_view(self, view):
        self.view = view

    def load_summary(self):
        self.view.set_summary_text(f"Aluguel #{self.aluguel_id}\nSelecione a forma e confirme.")

    def confirm_payment(self):
        forma = self.view.get_forma()
        ok, msg = self.service.confirm_payment(self.aluguel_id, forma)
        if ok:
            self.view.show_info("Sucesso", msg)
            self.back_to_dashboard()
        else:
            self.view.show_error("Erro", msg)

    def back_to_dashboard(self):
        clear_root(self.root)
        from app.controllers.dashboard_controller import DashboardController
        from app.views.dashboard_view import DashboardView
        DashboardView(self.root, DashboardController(self.root))