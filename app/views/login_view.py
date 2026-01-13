# src/views/login_view.py
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from app.utils.ui import center_window

class LoginView:
  def __init__(self, root, controller):
    self.root = root
    self.controller = controller
    self.controller.set_view(self)

    root.title("Login - Aluguel de Carros")
    root.resizable(False, False)
    
    center_window(root, 400, 420)

    self.build_ui()

  def build_ui(self):
    frame = tk.Frame(self.root, padx=20, pady=20)
    frame.pack(expand=True)

    ttk.Label(frame, text="Login", font=("Arial", 16, "bold")).pack(pady=10)

    ttk.Label(frame, text="CPF (Apenas números):").pack(anchor="w")
    self.entry_cpf = ttk.Entry(frame, width=40)
    self.entry_cpf.pack()

    ttk.Label(frame, text="Senha:").pack(anchor="w")
    self.entry_senha = ttk.Entry(frame, width=40, show="*")
    self.entry_senha.pack()

    ttk.Button(
      frame, text="Entrar", bootstyle='success',
      width=20, command=self.on_login_click
    ).pack(pady=15)

    ttk.Button(
      frame, text="Criar conta → Registro",
      command=self.on_register_click
    ).pack()

  def get_cpf(self):
    return self.entry_cpf.get().strip()

  def get_senha(self):
    return self.entry_senha.get()

  def on_login_click(self):
    self.controller.login()

  def on_register_click(self):
    self.controller.go_to_register()

  def show_info(self, msg_title: str, message: str):
    messagebox.showinfo(msg_title, message)

  def show_error(self, msg_title: str, message: str):
    messagebox.showerror(msg_title, message)

  def show_warning(self, msg_title: str, message: str):
    messagebox.showwarning(msg_title, message)