from core.services.user_service import UserService

class RegisterController:
  def __init__(self):
    self.user_service = UserService()
  
  def set_view(self, view):
    self.view = view
  
  def register(self):
    cpf = self.view.get_cpf()
    nome = self.view.get_nome()
    cnh = self.view.get_cnh()
    telefone = self.view.get_telefone()
    senha = self.view.get_senha()
    confirm = self.view.get_confirm()
    
    result, msg = self.user_service.register_user(cpf, nome, cnh, telefone, senha, confirm)
    
    if result:
      self.view.show_info("Sucesso!", msg)
      self.go_to_login()
    else:
      self.view.show_error("Erro!", msg)

  def go_to_login(self):
    pass
  #   self.view.show_frame("LoginView")
    
  #   login_controller = LoginController()
  #   LoginView(root, login_controller)