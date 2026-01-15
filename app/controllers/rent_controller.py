from app.utils.ui import clear_root
from app.core.services.rental_service import RentalService

class RentController:
    def __init__(self, root, placa: str):
        self.root = root
        self.placa = placa
        self.view = None
        self.service = RentalService()

    def set_view(self, view):
        self.view = view

    def continue_to_payment(self):
        data_inicio, data_fim = self.view.get_dates()

        if not data_inicio or not data_fim:
            self.view.show_warning("Atenção", "Preencha data início e data fim.")
            return

        ok, msg, aluguel_id = self.service.create_pending_rent(self.placa, data_inicio, data_fim)
        if not ok:
            self.view.show_error("Erro", msg)
            return

        self.view.show_info("Ok", msg)
        self.open_payment(aluguel_id)

    def open_payment(self, aluguel_id: int):
        clear_root(self.root)
        from app.controllers.payment_controller import PaymentController
        from app.views.payment_view import PaymentView
        # Passando o ID para o controller e para a view conforme a lógica original
        PaymentView(self.root, PaymentController(self.root, aluguel_id), aluguel_id=aluguel_id)

    def back_to_car_details(self):
        clear_root(self.root)
        from app.controllers.car_details_controller import CarDetailsController
        from app.views.car_details_view import CarDetailsView
        CarDetailsView(self.root, CarDetailsController(self.root, self.placa))