# app/views/dashboard_view.py
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from app.utils.ui import center_window

class DashboardView:
  def __init__(self, root, controller):
    self.root = root
    self.controller = controller
    self.build_ui()
    self.controller.set_view(self)

    root.title("Dashboard - Aluguel de Carros")
    root.resizable(False, False)

    center_window(root, 900, 520)


    # carrega os carros do banco ao abrir
    self.controller.load_cars()

  def build_ui(self):
    container = tk.Frame(self.root, padx=16, pady=16)
    container.pack(fill="both", expand=True)

    header = tk.Frame(container)
    header.pack(fill="x")

    ttk.Label(header, text="Dashboard", font=("Arial", 16, "bold")).pack(side="left")

    ttk.Button(
      header, text="Sair", bootstyle="danger",
      command=self.on_logout_click
    ).pack(side="right")

    # Listagem
    ttk.Label(container, text="Carros cadastrados:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(16, 6))

    table_frame = tk.Frame(container)
    table_frame.pack(fill="both", expand=True)

    cols = ("placa", "marca", "modelo", "categoria", "ano", "status", "cor", "km")
    self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=14)

    self.tree.heading("placa", text="Placa")
    self.tree.heading("marca", text="Marca")
    self.tree.heading("modelo", text="Modelo")
    self.tree.heading("categoria", text="Categoria")
    self.tree.heading("ano", text="Ano")
    self.tree.heading("status", text="Status")
    self.tree.heading("cor", text="Cor")
    self.tree.heading("km", text="Km")

    self.tree.column("placa", width=90)
    self.tree.column("marca", width=120)
    self.tree.column("modelo", width=180)
    self.tree.column("categoria", width=110)
    self.tree.column("ano", width=60)
    self.tree.column("status", width=110)
    self.tree.column("cor", width=110)
    self.tree.column("km", width=120)

    vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
    self.tree.configure(yscrollcommand=vsb.set)

    self.tree.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")

    # Clique duplo abre detalhes
    self.tree.bind("<Double-1>", self.on_open_details_double_click)

    actions = tk.Frame(container)
    actions.pack(fill="x", pady=(10, 0))

    ttk.Button(
      actions, text="Atualizar lista",
      command=self.on_refresh_click
    ).pack(side="left", padx=6)

    ttk.Button(
      actions, text="Ver detalhes",
      command=self.on_open_details_click
    ).pack(side="right")

    self.btn_add = ttk.Button(
        actions, text="Adicionar carro",
        bootstyle="success",
        command=self.on_add_click
    )

    self.btn_delete = ttk.Button(
        actions, text="Excluir carro",
        bootstyle="danger",
        command=self.on_delete_click
    )
    
    self.btn_modelos = ttk.Button(
      actions,
      text="Gerenciar Modelos",
      command=self.on_modelos_click
    )

  # --------- Métodos chamados pelo Controller ---------
  def set_car_list(self, cars: list[dict]):
    # limpa
    for item in self.tree.get_children():
      self.tree.delete(item)

    # insere
    for car in cars:
      placa = car.get("Placa")
      self.tree.insert(
        "", "end",
        iid=placa,
        values=(
          placa,
          car.get("Marca"),
          car.get("Descricao"),
          car.get("Categoria"),
          car.get("Ano"),
          car.get("Status"),
          car.get("Cor"),
          car.get("Quilometragem")
      )
      )

  def get_selected_car_placa(self) -> str | None:
    sel = self.tree.selection()
    if not sel:
      return None
    # como iid = placa, selection()[0] já é a placa
    return sel[0]

  # --------- Eventos da View ---------
  def on_refresh_click(self):
    self.controller.load_cars()

  def on_open_details_click(self):
    self.controller.open_car_details()

  def on_open_details_double_click(self, event):
    self.controller.open_car_details()

  def on_logout_click(self):
    self.controller.logout()

  def on_add_click(self):
    self.controller.open_add_car()
  
  def on_delete_click(self):
    self.controller.delete_selected_car()

  def on_modelos_click(self):
    self.controller.open_modelos()

  def set_admin_mode(self, is_admin: bool):
    if is_admin:
      self.btn_add.pack(side="left", padx=6)
      self.btn_delete.pack(side="left", padx=6)
      self.btn_modelos.pack(side="left", padx=6)
    else:
      self.btn_add.pack_forget()
      self.btn_delete.pack_forget()
      self.btn_modelos.pack_forget()

  # --------- Mensagens padrão ---------
  def show_info(self, msg_title: str, message: str):
    messagebox.showinfo(msg_title, message)

  def show_error(self, msg_title: str, message: str):
    messagebox.showerror(msg_title, message)

  def show_warning(self, msg_title: str, message: str):
    messagebox.showwarning(msg_title, message)
