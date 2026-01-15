from app.core import session
from app.utils.ui import clear_root
from app.core.services.modelo_service import ModeloService

class ModelosController:
    def __init__(self, root):
        self.root = root
        self.view = None
        self.service = ModeloService()

    def set_view(self, view):
        self.view = view
        user = session.current_user
        if not user or user.get("cargo") != "admin":
            self.view.show_error("Acesso negado", "Apenas administradores podem gerenciar modelos.")
            self.back_to_dashboard()

    def load_modelos(self):
        try:
            modelos = self.service.list_modelos()
            self.view.set_modelos_list(modelos)
        except Exception as e:
            self.view.show_error("Erro", f"Falha ao carregar modelos: {e}")

    def open_new_form(self):
        self.view.open_modelo_form("Novo Modelo", None)

    def open_edit_form(self):
        mid = self.view.get_selected_modelo_id()
        if not mid:
            self.view.show_warning("Atenção", "Selecione um modelo para editar.")
            return

        modelo = self.service.get_modelo_by_id(mid)
        if not modelo:
            self.view.show_error("Erro", "Modelo não encontrado.")
            self.load_modelos()
            return

        self.view.open_modelo_form("Editar Modelo", modelo)

    def save_modelo_from_form(self, win, marca: str, descricao: str, categoria: str, diaria_str: str, initial: dict | None):
        if not marca or not descricao or not categoria or not diaria_str:
            self.view.show_warning("Atenção", "Preencha Marca, Descrição, Categoria e Valor da diária.")
            return

        try:
            diaria = float(diaria_str)
            if diaria <= 0:
                self.view.show_warning("Atenção", "Valor da diária deve ser maior que 0.")
                return
        except ValueError:
            self.view.show_warning("Atenção", "Valor da diária inválido (use formato 120.00).")
            return

        try:
            if initial is None:
                self.service.create_modelo(descricao=descricao, marca=marca, categoria=categoria, valor_diaria=diaria)
            else:
                mid = initial["ID_Modelo"]
                # Atualização campo a campo conforme estrutura do serviço
                self.service.update_modelo(mid, "Marca", marca)
                self.service.update_modelo(mid, "Descricao", descricao)
                self.service.update_modelo(mid, "Categoria", categoria)
                self.service.update_modelo(mid, "Valor_Diaria", diaria)

            win.destroy()
            self.load_modelos()
            self.view.show_info("Sucesso", "Modelo salvo com sucesso!")
        except Exception as e:
            self.view.show_error("Erro", f"Falha ao salvar modelo: {e}")

    def delete_selected(self):
        mid = self.view.get_selected_modelo_id()
        if not mid:
            self.view.show_warning("Atenção", "Selecione um modelo para excluir.")
            return

        if not self.view.ask_yes_no("Confirmar", "Deseja excluir este modelo?"):
            return

        try:
            ok, msg = self.service.delete_modelo(mid)
            if ok:
                self.view.show_info("Sucesso", msg)
                self.load_modelos()
            else:
                self.view.show_error("Erro", msg)
        except Exception as e:
            self.view.show_error("Erro", f"Falha ao excluir modelo: {e}")

    def back_to_dashboard(self):
        clear_root(self.root)
        from app.controllers.dashboard_controller import DashboardController
        from app.views.dashboard_view import DashboardView
        DashboardView(self.root, DashboardController(self.root))