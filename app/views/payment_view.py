# app/views/payment_view.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from app.utils.ui import center_window

class PaymentView:
    def __init__(self, root, controller, aluguel_id: int):
        self.root = root
        self.controller = controller
        self.aluguel_id = aluguel_id

        root.title("Pagamento")
        root.resizable(False, False)
        center_window(root, 420, 320)

        self.build_ui()
        self.controller.set_view(self)
        self.controller.load_summary()

    def build_ui(self):
        container = ttk.Frame(self.root, padding=16)
        container.pack(fill=BOTH, expand=True)

        ttk.Label(container, text="Pagamento", font=("Arial", 16, "bold")).pack(anchor=W)
        self.lbl_info = ttk.Label(container, text="", font=("Arial", 11))
        self.lbl_info.pack(anchor=W, pady=(8, 14))

        ttk.Label(container, text="Forma de pagamento:").pack(anchor=W)
        self.cmb_forma = ttk.Combobox(
            container,
            state="readonly",
            width=38,
            values=["pix", "credito", "debito", "dinheiro", "boleto"]
        )
        self.cmb_forma.pack(fill=X)
        self.cmb_forma.current(0)

        actions = ttk.Frame(container)
        actions.pack(fill=X, pady=(16, 0))

        ttk.Button(actions, text="Cancelar", bootstyle=DANGER, command=self.on_cancel).pack(side=LEFT)
        ttk.Button(actions, text="Confirmar (pago)", bootstyle=SUCCESS, command=self.on_confirm).pack(side=RIGHT)

    def set_summary_text(self, text: str):
        self.lbl_info.config(text=text)

    def get_forma(self) -> str:
        return self.cmb_forma.get().strip()

    def on_confirm(self):
        self.controller.confirm_payment()

    def on_cancel(self):
        self.controller.back_to_dashboard()

    def show_info(self, title: str, msg: str):
        messagebox.showinfo(title, msg)

    def show_warning(self, title: str, msg: str):
        messagebox.showwarning(title, msg)

    def show_error(self, title: str, msg: str):
        messagebox.showerror(title, msg)
