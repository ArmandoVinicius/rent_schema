# src/views/register_view.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class RegisterView:
  def __init__(self, root, controller):
    self.root = root
    self.controller = controller
    self.controller.set_view(self)

    root.title("Registro - Aluguel de Carros")
    root.geometry("400x580")
    root.resizable(False, False)

    self.build_ui()

  def build_ui(self):
    style = ttk.Style()
    style.configure('Green.TButton',  background="#4CAF50", foreground="white")

    frame = tk.Frame(self.root, padx=20, pady=20)
    frame.pack(expand=True)

    ttk.Label(frame, text="Cadastro de Usuário", font=("Arial", 16, "bold")).pack(pady=10)

    ttk.Label(frame, text="CPF (Apenas números):").pack(anchor="w")
    self.entry_cpf = ttk.Entry(frame, width=40)
    self.entry_cpf.pack()

    ttk.Label(frame, text="Nome completo:").pack(anchor="w")
    self.entry_nome = ttk.Entry(frame, width=40)
    self.entry_nome.pack()

    ttk.Label(frame, text="CNH:").pack(anchor="w")
    self.entry_cnh = ttk.Entry(frame, width=40)
    self.entry_cnh.pack()

    ttk.Label(frame, text="Telefone:").pack(anchor="w")
    self.entry_telefone = ttk.Entry(frame, width=40)
    self.entry_telefone.pack()

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
      command=self.on_login_click
    ).pack()

  def get_cpf(self):
    return self.entry_cpf.get().strip()
  
  def get_nome(self):
    return self.entry_nome.get().strip()
  
  def get_cnh(self):
    return self.entry_cnh.get().strip()
  
  def get_telefone(self):
    return self.entry_telefone.get().strip()
    
  def get_senha(self):
    return self.entry_senha.get()
    
  def get_confirm(self):
    return self.entry_confirm.get()

  def on_login_click(self):
    self.controller.go_to_login()

  def on_register_click(self):
    self.controller.register()

  # def destroy_window(self):
  #   self.window.destroy()

  def show_info(self, msg_title: str, message: str):
    messagebox.showinfo(msg_title, message)
  
  def show_error(self, msg_title: str, message: str):
    messagebox.showerror(msg_title, message)
    
  def show_warning(self, msg_title: str, message: str):
    messagebox.showwarning(msg_title, message)