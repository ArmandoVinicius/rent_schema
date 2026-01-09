from models.user_model import UserModel
import hashlib

class UserService:
  def __init__(self):
    self.user_model = UserModel()
  
  def register_user(self, nome: str, email: str, senha: str, confirm: str):
    if not nome or not email or not senha:
      return False, "Preencha todos os campos."
    if senha != confirm:
      return False, "As senhas não coincidem."
    if self.user_model.get_user_by_email(email=email):
      return False, "Este email já está cadastrado."
    
    # Olhar o bcrypt para adicionar o tempo na seed
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    try:
      self.user_model.create_user(nome=nome, email=email, senha_hash=senha_hash)
      return True, "Usuário registrado com sucesso!"
    except Exception as e:
      return False, f"Erro ao registrar: {e}"