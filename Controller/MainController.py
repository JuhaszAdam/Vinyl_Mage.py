from customtkinter import *

from Controller.TransformerController import TransformerController


class MainController:
    root: CTk
    content = None

    app = {}

    def __init__(self, root: CTk):
        self.transformerController: TransformerController = TransformerController()
        self.root = root
        self._init_window()

    def _init_window(self):
        self.root.title("Vinyl Mage")
        self.root.geometry("800x600")

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=0)

        label_import_file = CTkLabel(
            self.root,
            text="Importálás",
        )

        label_preview_data = CTkLabel(
            self.root,
            text="Előnézet",
        )

        input_file_name = CTkEntry(
            self.root,
        )

        preview_tree = CTkTextbox(
            self.root,
        )

        btn_import = CTkButton(
            self.root,
            text="Importálás",
            command=self.file_import,
        )

        btn_export = CTkButton(
            self.root,
            text="Exportálás",
            command=self.file_export,
        )

        ### Apply to Grid ###
        label_import_file.grid(row=0, column=0, sticky='nw', pady=20, padx=20)
        label_preview_data.grid(row=0, column=1, sticky='ne', pady=20, padx=20)

        input_file_name.grid(row=1, column=0, sticky='nw', pady=20, padx=20)
        preview_tree.grid(row=1, column=1, sticky='ne', pady=20, padx=20)

        btn_import.grid(row=2, column=0, sticky='nw', pady=20, padx=20)
        btn_export.grid(row=2, column=1, sticky='ne', pady=20, padx=20)

        ### Save references ###
        self.app['label_import_file'] = label_import_file
        self.app['label_preview_data'] = label_preview_data
        self.app['input_file_name'] = input_file_name
        self.app['preview_tree'] = preview_tree
        self.app['btn_import'] = btn_import
        self.app['btn_export'] = btn_export

        ### Fullscreen ###
        self.root.state('zoomed')

    def file_import(self):
        filename = self.app['input_file_name'].get()
        if len(filename) != 0:
            result = self.transformerController.transform(filename)
            print(result)
            # self.refresh_preview()

    def file_export(self):
        print("export")

    def refresh_preview(self):
        preview_tree = self.root.nametowidget('preview_tree')
        preview_tree.delete(*preview_tree.get_children())
        preview_tree.insert("", 'end', text=self.content)
