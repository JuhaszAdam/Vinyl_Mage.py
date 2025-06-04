import pprint
import subprocess

from customtkinter import *

from Controller.TransformerController import TransformerController


class MainController:
    root: CTk
    content = None
    work_directory = "Resources"

    app = {}
    vinyl_list = {}

    def __init__(self, root: CTk):
        self.root = root
        self._init_window()
        self.root.bind('<Return>', self.file_import)

    def _init_window(self):
        self.root.title("Vinyl Mage")
        self.root.geometry("800x600")

        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)

        preview_tree = CTkTextbox(
            self.root,
            border_color=ThemeManager.theme["CTkButton"]["fg_color"],
            border_width=1
        )

        btn_import = CTkButton(
            self.root,
            text="Import",
            command=self.file_import,
            border_width=1,
            border_color=ThemeManager.theme["CTkButton"]["fg_color"],
        )

        btn_export = CTkButton(
            self.root,
            text="Export",
            command=self.file_export,
            state="disabled",
            fg_color="transparent",
            border_color=ThemeManager.theme["CTkButton"]["fg_color"],
            border_width=1
        )

        progress_bar = CTkProgressBar(
            self.root,
            mode="indeterminate",
        )

        ### Apply to Grid ###
        preview_tree.grid(row=1, column=0, sticky='NSEW', pady=20, padx=20, columnspan=3)

        btn_import.grid(row=2, column=0, sticky='nw', pady=20, padx=20, ipady=20, ipadx=20)
        btn_export.grid(row=2, column=2, sticky='ne', pady=20, padx=20, ipady=20, ipadx=20)

        ### Save references ###
        self.app['preview_tree'] = preview_tree
        self.app['btn_import'] = btn_import
        self.app['btn_export'] = btn_export
        self.app['progress_bar'] = progress_bar


        ### Fullscreen ###
        self.root.state('zoomed')

    def file_import(self, event=None):
        self.app['progress_bar'].grid(row=2, column=1, sticky='ew', pady=20, padx=20)
        self.app['progress_bar'].start()
        filename = filedialog.askopenfilename(
            initialdir="Resources",
            title="Select a File",
            filetypes=(("Data files", "*.json* *.xml *.csv"), ("All files", "*.*")))

        if len(filename) != 0:
            self.app['btn_export'].configure(fg_color=ThemeManager.theme["CTkButton"]["fg_color"], state="normal")
            self.vinyl_list = TransformerController.transform(filename)
            self.app['preview_tree'].delete('0.0', 'end')
            self.app['preview_tree'].insert('end', f'\nImportált termékek száma: {len(self.vinyl_list)}\n')
            for vinyl in self.vinyl_list:
                self.app['preview_tree'].insert('end', f'\n*********** Item ***********\n')
                self.app['preview_tree'].insert('end', pprint.pformat(vinyl.attr))  ## todo: ULTRA HACK BLACK MAGIC

        self.app['progress_bar'].stop()
        self.app['progress_bar'].grid_forget()

    def file_export(self):
        self.app['progress_bar'].grid(row=2, column=1, sticky='ew', pady=20, padx=20)
        self.app['progress_bar'].start()

        location = 'Resources'
        filename = 'shoprenter_import.xml'
        path = os.path.join(os.getcwd(), location, filename)
        TransformerController.export(self.vinyl_list, location, filename)
        subprocess.Popen(f'explorer /select, {path}')

        self.app['progress_bar'].stop()
        self.app['progress_bar'].grid_forget()

    def refresh_preview(self):
        preview_tree = self.app['preview_tree']
