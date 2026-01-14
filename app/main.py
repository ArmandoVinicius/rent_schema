import os
import sys
import ttkbootstrap as ttk
from app.controllers.login_controller import LoginController
from app.views.login_view import LoginView

def main():
    # Verifica se o arquivo de configuração existe
    # Caminho: rent_schema/app/config/database.ini
    config_path = os.path.join(os.path.dirname(__file__), "config", "database.ini")
    
    if not os.path.exists(config_path):
        print("---------------------------------------------------------")
        print(f"ERRO CRÍTICO: Arquivo de configuração não encontrado.")
        print(f"Esperado em: {config_path}")
        print("Crie o arquivo 'database.ini' dentro de 'app/config/'")
        print("com as credenciais [mysql] (host, user, password...).")
        print("---------------------------------------------------------")
        return

    # Inicia a janela com o tema padrão
    root = ttk.Window(themename="flatly")
    root.title("Sistema de Aluguel de Carros")
    
    # Inicia o fluxo pelo Login
    controller = LoginController(root)
    LoginView(root, controller)

    root.mainloop()

if __name__ == "__main__":
    main()