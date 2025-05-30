import customtkinter as tk
from Controller.MainController import MainController


def run():
    root = tk.CTk()
    MainController(root)

    root.mainloop()


if __name__ == "__main__":
    run()
