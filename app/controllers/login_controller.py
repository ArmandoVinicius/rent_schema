from app.views.register_view import RegisterView
from app.views.login_view import LoginView
from app.utils.ui import clear_root
from app.core.services.user_service import UserService
from app.core import session

class LoginController:
    def __init__(self, root):
        self.root = root
        self.view = None
        self.user_service = UserService()

    def set_view(self, view):
        self.view = view

    def go_to_register(self):
        clear_root(self.root)
        from app.controllers.register_controller import RegisterController
        rc = RegisterController(self.root)
        RegisterView(self.root, rc)

    def login(self):
        cpf = self.view.get_cpf()
        senha = self.view.get_senha()

        if not cpf or not senha:
            self.view.show_warning("Atenção", "Preencha CPF e senha.")
            return
        
        result, msg, user = self.user_service.login_user(cpf, senha)
        if result:
            self.view.show_info("Login bem sucedido!", msg)
            session.current_user = user
            self.go_to_dashboard()
        else:
            self.view.show_error("Erro", msg)

    def go_to_dashboard(self):
        clear_root(self.root)
        from app.controllers.dashboard_controller import DashboardController
        from app.views.dashboard_view import DashboardView
        dc = DashboardController(self.root)
        DashboardView(self.root, dc)