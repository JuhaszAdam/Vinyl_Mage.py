from Controller.MainController import MainController

import customtkinter as ctk
from CTkMenuBar import CTkMenuBar


def run():
    root = ctk.CTk()
    menubar = CTkMenuBar(root)
    menubar.grid(row=0, column=0, sticky="ew")
    menubar.grid_forget() # TODO: not needed yet
    MainController(root)

    root.mainloop()


if __name__ == "__main__":
    run()
