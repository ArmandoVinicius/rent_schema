# app/views/rent_view.py
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from app.utils.ui import center_window

class RentView:
    def __init__(self, root, controller, placa: str):
        self.root = root
        self.controller = controller
        self.placa = placa

        root.title("Alugar Carro")
        root.resizable(False, False)
        center_window(root, 420, 340)

        self.build_ui()
        self.controller.set_view(self)

    def build_ui(self):
        container = ttk.Frame(self.root, padding=16)
        container.pack(fill=BOTH, expand=True)

        ttk.Label(container, text="Alugar Carro", font=("Arial", 16, "bold")).pack(anchor=W)
        ttk.Label(container, text=f"Placa: {self.placa}", font=("Arial", 11)).pack(anchor=W, pady=(6, 14))

        ttk.Label(container, text="Data início (YYYY-MM-DD):").pack(anchor=W)
        self.entry_inicio = ttk.Entry(container, width=40)
        self.entry_inicio.pack(fill=X)

        ttk.Label(container, text="Data fim (YYYY-MM-DD):").pack(anchor=W, pady=(10, 0))
        self.entry_fim = ttk.Entry(container, width=40)
        self.entry_fim.pack(fill=X)

        actions = ttk.Frame(container)
        actions.pack(fill=X, pady=(16, 0))

        ttk.Button(actions, text="Cancelar", bootstyle=DANGER, command=self.on_cancel).pack(side=LEFT)
        ttk.Button(actions, text="Continuar", bootstyle=SUCCESS, command=self.on_continue).pack(side=RIGHT)

    def get_dates(self) -> tuple[str, str]:
        return self.entry_inicio.get().strip(), self.entry_fim.get().strip()

    def on_continue(self):
        self.controller.continue_to_payment()

    def on_cancel(self):
        self.controller.back_to_car_details()

    def show_info(self, title: str, msg: str):
        messagebox.showinfo(title, msg)

    def show_warning(self, title: str, msg: str):
        messagebox.showwarning(title, msg)

    def show_error(self, title: str, msg: str):
        messagebox.showerror(title, msg)
