import tkinter as tk
#from models.database import create_tables
from views.register_view import RegisterView

def open_register():
    for widget in root.winfo_children():
        widget.destroy()
    RegisterView(root, open_login)

def open_login():
    for widget in root.winfo_children():
        widget.destroy()
    # aqui você criará LoginView depois
    tk.Label(root, text="Tela de login futura").pack()

root = tk.Tk()
#create_tables()
open_register()
root.mainloop()
