# app/views/car_details_view.py
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from app.utils.ui import center_window

class CarDetailsView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        root.title("Detalhes do Carro")
        root.resizable(False, False)
        center_window(root, 520, 600)

        self.model_map = {}  # texto -> id_modelo

        self.build_ui()
        self.controller.set_view(self)
        self.controller.load_details()

    def build_ui(self):
        container = ttk.Frame(self.root, padding=16)
        container.pack(fill=BOTH, expand=True)

        header = ttk.Frame(container)
        header.pack(fill=X)

        ttk.Label(header, text="Detalhes do Carro", font=("Arial", 16, "bold")).pack(side=LEFT)
        ttk.Button(header, text="Voltar", bootstyle=SECONDARY, command=self.on_back_click).pack(side=RIGHT)

        form = ttk.Frame(container)
        form.pack(fill=BOTH, expand=True, pady=(14, 0))

        ttk.Label(form, text="Placa:").pack(anchor=W)
        self.var_placa = tk.StringVar(value="")
        self.ent_placa = ttk.Entry(form, textvariable=self.var_placa, width=40, state="readonly")
        self.ent_placa.pack(fill=X)

        ttk.Label(form, text="Modelo:").pack(anchor=W, pady=(10, 0))
        self.cmb_modelo = ttk.Combobox(form, state="readonly", width=38)
        self.cmb_modelo.pack(fill=X)

        ttk.Label(form, text="Valor da diária (R$):").pack(anchor=W, pady=(10, 0))
        self.var_diaria = tk.StringVar(value="")
        ttk.Entry(form, textvariable=self.var_diaria, state="readonly", width=40).pack(fill=X)

        ttk.Label(form, text="Chassi:").pack(anchor=W, pady=(10, 0))
        self.var_chassi = tk.StringVar(value="")
        self.ent_chassi = ttk.Entry(form, textvariable=self.var_chassi, width=40)
        self.ent_chassi.pack(fill=X)

        ttk.Label(form, text="Cor:").pack(anchor=W, pady=(10, 0))
        self.var_cor = tk.StringVar(value="")
        self.ent_cor = ttk.Entry(form, textvariable=self.var_cor, width=40)
        self.ent_cor.pack(fill=X)

        ttk.Label(form, text="Ano:").pack(anchor=W, pady=(10, 0))
        self.var_ano = tk.StringVar(value="")
        self.ent_ano = ttk.Entry(form, textvariable=self.var_ano, width=40)
        self.ent_ano.pack(fill=X)

        ttk.Label(form, text="Quilometragem:").pack(anchor=W, pady=(10, 0))
        self.var_km = tk.StringVar(value="")
        self.ent_km = ttk.Entry(form, textvariable=self.var_km, width=40)
        self.ent_km.pack(fill=X)

        ttk.Label(form, text="Status:").pack(anchor=W, pady=(10, 0))
        self.status_var = tk.StringVar()
        self.cmb_status = ttk.Combobox(
            form,
            state="readonly",
            width=38,
            textvariable=self.status_var,
            values=["disponivel", "alugado", "manutencao", "inativo"]
        )
        self.cmb_status.pack(fill=X)

        actions = ttk.Frame(container)
        actions.pack(fill=X, pady=(16, 0))

        self.btn_rent = ttk.Button(actions, text="Alugar", bootstyle=PRIMARY, command=self.on_rent_click)
        self.btn_save = ttk.Button(actions, text="Salvar alterações", bootstyle=SUCCESS, command=self.on_save_click)

        # por padrão: escondidos; controller decide
        self.btn_rent.pack_forget()
        self.btn_save.pack_forget()

    # --------- Controller -> View ----------
    def set_mode(self, is_admin: bool):
        if is_admin:
            # edição liberada
            self.ent_chassi.config(state="normal")
            self.ent_cor.config(state="normal")
            self.ent_ano.config(state="normal")
            self.ent_km.config(state="normal")
            self.cmb_status.config(state="readonly")
            self.cmb_modelo.config(state="readonly")

            self.btn_rent.pack_forget()
            self.btn_save.pack(side=RIGHT)
        else:
            # somente leitura
            self.ent_chassi.config(state="readonly")
            self.ent_cor.config(state="readonly")
            self.ent_ano.config(state="readonly")
            self.ent_km.config(state="readonly")
            self.cmb_status.config(state="disabled")
            self.cmb_modelo.config(state="disabled")

            self.btn_save.pack_forget()
            self.btn_rent.pack(side=LEFT)

    def set_modelos(self, modelos: list[dict]):
        options = []
        self.model_map = {}

        for m in modelos:
            texto = f"{m['Marca']} {m['Descricao']} — {m['Categoria']}"
            options.append(texto)
            self.model_map[texto] = m["ID_Modelo"]

        self.cmb_modelo["values"] = options

    def set_car_data(self, car: dict):
        self.var_placa.set(car.get("Placa", ""))
        self.var_chassi.set(car.get("Chassi", "") or "")
        self.var_diaria.set(f"{car.get('Valor_Diaria', 0):.2f}")
        self.var_cor.set(car.get("Cor", "") or "")
        self.var_ano.set(str(car.get("Ano", "") or ""))
        self.var_km.set(str(car.get("Quilometragem", "") or ""))

        self.status_var.set(car.get("Status") or "disponivel")

        modelo_texto = car.get("ModeloTexto")
        if modelo_texto:
            vals = list(self.cmb_modelo["values"])
            if modelo_texto in vals:
                self.cmb_modelo.set(modelo_texto)
            elif vals:
                self.cmb_modelo.current(0)

    def get_update_data(self) -> dict:
        # valida campos numéricos sem explodir
        ano_str = self.var_ano.get().strip()
        km_str = self.var_km.get().strip()
        if not ano_str.isdigit() or not km_str.isdigit():
            raise ValueError("Ano/Quilometragem inválidos.")

        modelo_texto = self.cmb_modelo.get().strip()
        id_modelo = self.model_map.get(modelo_texto)
        if not id_modelo:
            raise ValueError("Selecione um modelo válido.")

        return {
            "Chassi": self.var_chassi.get().strip() or None,
            "Cor": self.var_cor.get().strip(),
            "Ano": int(ano_str),
            "Quilometragem": int(km_str),
            "Status": self.cmb_status.get().strip(),
            "fk_Modelo_ID_Modelo": id_modelo,
        }

    # --------- Eventos ----------
    def on_back_click(self):
        self.controller.back_to_dashboard()

    def on_save_click(self):
        self.controller.save_updates()

    def on_rent_click(self):
        self.controller.open_rent()

    # --------- Mensagens ----------
    def show_info(self, title: str, msg: str):
        messagebox.showinfo(title, msg)

    def show_error(self, title: str, msg: str):
        messagebox.showerror(title, msg)

    def show_warning(self, title: str, msg: str):
        messagebox.showwarning(title, msg)
