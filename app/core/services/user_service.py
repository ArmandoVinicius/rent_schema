from models.user_model import UserModel
import hashlib

class UserService:
  def __init__(self):
    self.user_model = UserModel()
  
  def register_user(self, cpf: str, nome: str, cnh: str, telefone: str, senha: str, confirm: str):
    if not cpf or not nome or not cnh or not telefone or not senha or not confirm:
      return False, "Preencha todos os campos."
    if senha != confirm:
      return False, "As senhas não coincidem."
    if self.user_model.get_user_by_cpf(cpf=cpf):
      return False, "Este CPF já está cadastrado."
    
    # Olhar o bcrypt para adicionar o tempo na seed
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    try:
      self.user_model.create_user(cpf=cpf, nome=nome, cnh=cnh, telefone=telefone, senha_hash=senha_hash)
      return True, "Usuário registrado com sucesso!"
    except Exception as e:
      return False, f"Erro ao registrar: {e}"