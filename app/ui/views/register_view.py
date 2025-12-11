# src/views/register_view.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ui.controllers.user_controller import UserController

class RegisterView:
    def __init__(self, root, go_to_login):
        self.root = root
        self.go_to_login = go_to_login

        root.title("Registro - Aluguel de Carros")
        root.geometry("400x380")
        root.resizable(False, False)

        self.build_ui()

    def build_ui(self):
        style = ttk.Style()
        style.configure('Green.TButton',  background="#4CAF50", foreground="white")

        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Cadastro de Usuário", font=("Arial", 16, "bold")).pack(pady=10)

        ttk.Label(frame, text="Nome completo:").pack(anchor="w")
        self.entry_nome = ttk.Entry(frame, width=40)
        self.entry_nome.pack()

        ttk.Label(frame, text="Email:").pack(anchor="w")
        self.entry_email = ttk.Entry(frame, width=40)
        self.entry_email.pack()

        ttk.Label(frame, text="Senha:").pack(anchor="w")
        self.entry_senha = ttk.Entry(frame, width=40, show="*")
        self.entry_senha.pack()

        ttk.Label(frame, text="Confirmar senha:").pack(anchor="w")
        self.entry_confirm = ttk.Entry(frame, width=40, show="*")
        self.entry_confirm.pack()

        ttk.Button(
            frame, text="Registrar", style='Green.TButton',
            width=20, command=self.on_register_click
        ).pack(pady=15)

        ttk.Button(
            frame, text="Já tenho conta → Login",
            command=self.go_to_login
        ).pack()

    def on_register_click(self):
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        senha = self.entry_senha.get()
        confirm = self.entry_confirm.get()

        success, msg = UserController.register(nome, email, senha, confirm)

        if success:
            messagebox.showinfo("Sucesso", msg)
            self.go_to_login()
        else:
            messagebox.showerror("Erro", msg)
