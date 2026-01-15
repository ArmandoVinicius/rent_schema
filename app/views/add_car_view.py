# app/views/add_car_view.py
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from app.utils.ui import center_window

class AddCarView:
  def __init__(self, root, controller):
    self.root = root
    self.controller = controller
    self.model_map = {}

    root.title("Adicionar Carro")
    root.resizable(False, False)
    center_window(root, 420, 520)

    self.build_ui()
    self.controller.set_view(self)

  def build_ui(self):
    frame = tk.Frame(self.root, padx=20, pady=20)
    frame.pack(expand=True)

    self.entries = {}

    for label in ["Placa", "Chassi", "Cor", "Ano", "Quilometragem"]:
      ttk.Label(frame, text=label).pack(anchor="w")
      if label == "Ano" or label == "Quilometragem":
        e = ttk.Spinbox(frame, from_=1900, to=2100, width=37) if label == "Ano" else ttk.Spinbox(frame, from_=0, to=1_000_000, increment=100, width=37)
      else:
        e = ttk.Entry(frame, width=40)
      e.pack()
      self.entries[label] = e

    ttk.Label(frame, text="Status:").pack(anchor="w")
    self.cmb_status = ttk.Combobox(
        frame,
        state="readonly",
        width=37,
        values=[
            "disponivel",
            "alugado",
            "manutencao",
            "inativo"
        ]
    )
    self.cmb_status.pack()
    self.cmb_status.current(0)
    
    ttk.Label(frame, text="Modelo:").pack(anchor="w")
    self.cmb_modelo = ttk.Combobox(frame, state="readonly", width=37)
    self.cmb_modelo.pack()

    ttk.Button(frame, text="Salvar", bootstyle="success", command=self.on_save).pack(pady=10)
    ttk.Button(frame, text="Cancelar", bootstyle="danger", command=self.on_cancel).pack()

  def get_form_data(self):
    placa = self.entries["Placa"].get().strip()
    chassi = self.entries["Chassi"].get().strip()
    cor = self.entries["Cor"].get().strip()
    ano_str = self.entries["Ano"].get().strip()
    km_str = self.entries["Quilometragem"].get().strip()
    status = self.cmb_status.get()
    modelo_texto = self.cmb_modelo.get()

    if not placa or not cor or not ano_str or not km_str:
      raise ValueError("Placa, Cor, Ano e Quilometragem são obrigatórios.")

    if not ano_str.isdigit() or not km_str.isdigit():
      raise ValueError("Ano e Quilometragem devem ser números.")

    if ano_str and (int(ano_str) < 1900 or int(ano_str) > 2100):
      raise ValueError("Ano deve estar entre 1900 e 2100.")
    
    if km_str and int(km_str) < 0:
      raise ValueError("Quilometragem não pode ser negativa.")

    if len(placa) != 7:
      raise ValueError("Placa deve ter exatamente 7 caracteres.")

    id_modelo = self.model_map.get(modelo_texto)
    if not id_modelo:
      raise ValueError("Selecione um modelo válido.")

    return {
        "placa": placa,
        "chassi": chassi or None,
        "cor": cor,
        "ano": int(ano_str),
        "quilometragem": int(km_str),
        "status": status,
        "id_modelo": id_modelo,
    }

  def set_modelos(self, modelos: list[dict]):
    options = []
    self.model_map = {}

    for m in modelos:
        texto = f"{m['Marca']} {m['Descricao']} - {m['Categoria']}"
        options.append(texto)
        self.model_map[texto] = m["ID_Modelo"]

    self.cmb_modelo["values"] = options
    if options:
        self.cmb_modelo.current(0)


  def on_save(self):
    self.controller.save_car()

  def on_cancel(self):
    self.controller.back_to_dashboard()

  def show_info(self, title, msg):
    messagebox.showinfo(title, msg)

  def show_error(self, title, msg):
    messagebox.showerror(title, msg)
