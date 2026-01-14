from app.models.user_model import UserModel
import hashlib

class UserService:
    def __init__(self):
        self.user_model = UserModel()
  
    def register_user(self, cpf: str, nome: str, cnh: str, telefone: str, senha: str, confirm: str):
        if not cpf or not nome or not cnh or not telefone or not senha or not confirm:
            return False, "Preencha todos os campos."
        if senha != confirm:
            return False, "As senhas não coincidem."
        if len(cpf) != 11 or not cpf.isdigit():
            return False, "CPF deve conter 11 números."
        if len(telefone) != 11 or not telefone.isdigit():
            return False, "Telefone deve conter 11 números."
        
        try:
            if self.user_model.get_user_by_cpf(cpf=cpf):
                return False, "Este CPF já está cadastrado."
            
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()
            self.user_model.create_user(cpf=cpf, nome=nome, cnh=cnh, telefone=telefone, senha_hash=senha_hash)
            return True, "Usuário registrado com sucesso!"
        except Exception as e:
            return False, f"Erro ao registrar: {e}"
    
    def login_user(self, cpf: str, senha: str):
        try:
            user = self.user_model.get_user_by_cpf(cpf=cpf)
            if not user:
                return False, "Usuário ou senha incorretos.", None
            
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()
            # Verifica a chave correta retornada pelo banco (geralmente lowercase no dict)
            stored_hash = user.get('senha_hash') or user.get('Senha_Hash')
            
            if stored_hash != senha_hash:
                return False, "Usuário ou senha incorretos.", None
            
            return True, "Login bem-sucedido.", user
        except Exception as e:
            return False, f"Erro no login: {e}", None