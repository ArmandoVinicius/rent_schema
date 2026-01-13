import tkinter as tk
import ttkbootstrap as ttk
from app.views.register_view import RegisterView
from app.controllers.register_controller import RegisterController

def main():
    root = ttk.Window()
    controller = RegisterController(root)
    RegisterView(root, controller)
    root.mainloop()

if __name__ == "__main__":
    main()
