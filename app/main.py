import tkinter as tk
from app.views.register_view import RegisterView
from app.controllers.register_controller import RegisterController

def main():
    root = tk.Tk()
    controller = RegisterController(root)
    RegisterView(root, controller)
    root.mainloop()

if __name__ == "__main__":
    main()
