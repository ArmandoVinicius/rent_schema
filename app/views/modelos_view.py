# app/views/modelos_view.py
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from app.utils.ui import center_window


class ModelosView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        root.title("Gerenciar Modelos")
        root.resizable(False, False)
        center_window(root, 900, 540)

        self.build_ui()
        self.controller.set_view(self)
        self.controller.load_modelos()

    def build_ui(self):
        container = ttk.Frame(self.root, padding=16)
        container.pack(fill=BOTH, expand=True)

        header = ttk.Frame(container)
        header.pack(fill=X)

        ttk.Label(header, text="Modelos", font=("Arial", 16, "bold")).pack(side=LEFT)
        ttk.Button(header, text="Voltar", bootstyle=SECONDARY, command=self.on_back_click).pack(side=RIGHT)

        ttk.Label(container, text="Lista de modelos:", font=("Arial", 11, "bold")).pack(anchor=W, pady=(16, 6))

        table_frame = ttk.Frame(container)
        table_frame.pack(fill=BOTH, expand=True)

        cols = ("id", "marca", "descricao", "categoria", "diaria")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=14)

        self.tree.heading("id", text="ID")
        self.tree.heading("marca", text="Marca")
        self.tree.heading("descricao", text="Descrição")
        self.tree.heading("categoria", text="Categoria")
        self.tree.heading("diaria", text="Diária (R$)")

        self.tree.column("id", width=70, anchor=W)
        self.tree.column("marca", width=160, anchor=W)
        self.tree.column("descricao", width=320, anchor=W)
        self.tree.column("categoria", width=140, anchor=W)
        self.tree.column("diaria", width=120, anchor=E)

        vsb = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview, bootstyle=SECONDARY)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        vsb.pack(side=RIGHT, fill=Y)

        self.tree.bind("<Double-1>", self.on_edit_double_click)

        actions = ttk.Frame(container)
        actions.pack(fill=X, pady=(12, 0))

        ttk.Button(actions, text="Atualizar", bootstyle=INFO, command=self.on_refresh_click).pack(side=LEFT)

        ttk.Button(actions, text="Excluir", bootstyle=DANGER, command=self.on_delete_click).pack(side=RIGHT, padx=(8, 0))
        ttk.Button(actions, text="Editar", bootstyle=WARNING, command=self.on_edit_click).pack(side=RIGHT, padx=(8, 0))
        ttk.Button(actions, text="Novo", bootstyle=SUCCESS, command=self.on_new_click).pack(side=RIGHT, padx=(8, 0))

    # ---------- dados ----------
    def set_modelos_list(self, modelos: list[dict]):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for m in modelos:
            mid = m.get("ID_Modelo")
            diaria = m.get("Valor_Diaria")
            diaria_txt = f"{float(diaria):.2f}" if diaria is not None else ""

            self.tree.insert(
                "",
                "end",
                iid=str(mid),
                values=(
                    mid,
                    m.get("Marca"),
                    m.get("Descricao"),
                    m.get("Categoria"),
                    diaria_txt
                )
            )

    def get_selected_modelo_id(self) -> int | None:
        sel = self.tree.selection()
        if not sel:
            return None
        return int(sel[0])

    # ---------- formulário ----------
    def open_modelo_form(self, title: str, initial: dict | None = None):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.resizable(False, False)
        center_window(win, 460, 390)

        frame = ttk.Frame(win, padding=16)
        frame.pack(fill=BOTH, expand=True)

        ttk.Label(frame, text=title, font=("Arial", 13, "bold")).pack(anchor=W, pady=(0, 10))

        ttk.Label(frame, text="Marca:").pack(anchor=W)
        entry_marca = ttk.Entry(frame, width=44)
        entry_marca.pack(fill=X)

        ttk.Label(frame, text="Descrição:").pack(anchor=W, pady=(10, 0))
        entry_desc = ttk.Entry(frame, width=44)
        entry_desc.pack(fill=X)

        ttk.Label(frame, text="Categoria:").pack(anchor=W, pady=(10, 0))
        entry_cat = ttk.Entry(frame, width=44)
        entry_cat.pack(fill=X)

        ttk.Label(frame, text="Valor diária (R$):").pack(anchor=W, pady=(10, 0))
        entry_diaria = ttk.Entry(frame, width=44)
        entry_diaria.pack(fill=X)

        if initial:
            entry_marca.insert(0, initial.get("Marca", ""))
            entry_desc.insert(0, initial.get("Descricao", ""))
            entry_cat.insert(0, initial.get("Categoria", ""))
            vd = initial.get("Valor_Diaria")
            entry_diaria.insert(0, f"{float(vd):.2f}" if vd is not None else "")

        btns = ttk.Frame(frame)
        btns.pack(fill=X, pady=(16, 0))

        ttk.Button(btns, text="Cancelar", bootstyle=SECONDARY, command=win.destroy).pack(side=LEFT)

        def on_save():
            marca = entry_marca.get().strip()
            desc = entry_desc.get().strip()
            cat = entry_cat.get().strip()
            diaria_str = entry_diaria.get().strip().replace(",", ".")
            self.controller.save_modelo_from_form(win, marca, desc, cat, diaria_str, initial)

        ttk.Button(btns, text="Salvar", bootstyle=SUCCESS, command=on_save).pack(side=RIGHT)

        win.bind("<Return>", lambda e: on_save())

    # ---------- eventos ----------
    def on_refresh_click(self):
        self.controller.load_modelos()

    def on_new_click(self):
        self.controller.open_new_form()

    def on_edit_click(self):
        self.controller.open_edit_form()

    def on_edit_double_click(self, event):
        self.controller.open_edit_form()

    def on_delete_click(self):
        self.controller.delete_selected()

    def on_back_click(self):
        self.controller.back_to_dashboard()

    # ---------- mensagens ----------
    def ask_yes_no(self, title: str, msg: str) -> bool:
        return messagebox.askyesno(title, msg)

    def show_info(self, title: str, msg: str):
        messagebox.showinfo(title, msg)

    def show_error(self, title: str, msg: str):
        messagebox.showerror(title, msg)

    def show_warning(self, title: str, msg: str):
        messagebox.showwarning(title, msg)
