# src/controllers/user_controller.py
import hashlib
from database import queries

class UserController:
    @staticmethod
    def register(nome: str, email: str, senha: str, confirm: str):
        
        # Validações
        if not nome or not email or not senha:
            return False, "Preencha todos os campos."

        if senha != confirm:
            return False, "As senhas não coincidem."

        if queries.user_exists(email):
            return False, "Este email já está cadastrado."

        senha_hash = hashlib.sha256(senha.encode()).hexdigest()

        try:
            queries.create_user(nome, email, senha_hash)
            return True, "Usuário registrado com sucesso!"
        except Exception as e:
            return False, f"Erro ao registrar: {e}"
