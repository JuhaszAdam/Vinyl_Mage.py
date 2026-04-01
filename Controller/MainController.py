import os
import subprocess
from tkinter import filedialog

import customtkinter as ctk
from customtkinter import ThemeManager, CTkButton, CTk, CTkProgressBar, CTkScrollableFrame, CTkLabel, \
    CTkFrame

from Controller.TransformerController import TransformerController
from View.LayoutView import LayoutView


class MainController:
    root: CTk
    content = None
    work_directory = "Resources"

    app = {}
    vinyl_list = {}
    layout_view = LayoutView

    def __init__(self, root: CTk):
        self.root = root
        self._init_window()
        self.root.bind('<Return>', lambda event: self.file_import())

    def _init_window(self):
        self.layout_view = LayoutView()

        self.root.title("Vinyl Mage")
        self.root.geometry("800x600")

        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=0)
        self.root.grid_columnconfigure(2, weight=1)

        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=1)

        # Módosítva: CTkTextbox helyett CTkScrollableFrame a böngészhetőség érdekében
        preview_tree = CTkScrollableFrame(
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

        theme_button = CTkButton(
            self.root,
            text='🎨',
            command=self._toggle_theme,
            width=30,
        )

        appearance_mode_button = ctk.CTkButton(
            self.root,
            text='☀' if ctk.get_appearance_mode() == "Dark" else '☾',
            command=self._toggle_appearance_mode,
            width=30,
        )

        progress_bar = CTkProgressBar(
            self.root,
            mode="indeterminate",
        )

        ### Apply to Grid ###
        preview_tree.grid(row=2, column=0, sticky='NSEW', pady=20, padx=20, columnspan=3)

        btn_import.grid(row=3, column=0, sticky='nw', pady=20, padx=20, ipady=20, ipadx=20)
        btn_export.grid(row=3, column=2, sticky='ne', pady=20, padx=20, ipady=20, ipadx=20)
        appearance_mode_button.grid(row=4, column=3, ipadx=2, padx=3)
        theme_button.grid(row=4, column=4, ipadx=2, padx=3)

        ### Save references ###
        self.app['preview_tree'] = preview_tree
        self.app['btn_import'] = btn_import
        self.app['btn_export'] = btn_export
        self.app['progress_bar'] = progress_bar
        self.app['theme_button'] = theme_button
        self.app['appearance_mode_button'] = appearance_mode_button

        ### Fullscreen ###
        self.root.state('zoomed')

    def file_import(self):
        self.app['progress_bar'].grid(row=3, column=1, sticky='ew', pady=20, padx=20)
        self.app['progress_bar'].start()
        filename = filedialog.askopenfilename(
            initialdir="Resources",
            title="Select a File",
            filetypes=(("Data files", "*.json* *.xml *.csv"), ("All files", "*.*")))

        if len(filename) != 0:
            self.app['btn_export'].configure(fg_color=ThemeManager.theme["CTkButton"]["fg_color"], state="normal")
            self.vinyl_list = TransformerController.transform(filename)

            # Előző elemek törlése a listából
            for widget in self.app['preview_tree'].winfo_children():
                widget.destroy()

            # Új elemek hozzáadása
            for vinyl in self.vinyl_list:
                self._add_vinyl_row(vinyl)

        self.app['progress_bar'].stop()
        self.app['progress_bar'].grid_forget()

    def _add_vinyl_row(self, vinyl):
        """Egy kiadvány sorának hozzáadása a görgethető listához."""
        row_frame = CTkFrame(self.app['preview_tree'])
        row_frame.pack(fill="x", padx=10, pady=5)

        # Adatok kinyerése (különböző adapterek eltérő kulcsokat használhatnak)
        artist = vinyl.attr.get('attr_values.eloado.hu', 'Ismeretlen előadó')
        title = vinyl.attr.get('product_description.name.hu', 'Ismeretlen cím')
        price = vinyl.attr.get('product.alapar', '0')
        sku = vinyl.attr.get('product.sku', 'N/A')

        # Ha az alapértelmezett kulcsok nem találhatók, próbáljunk meg valami mást
        if artist == 'Ismeretlen előadó' and title == 'Ismeretlen cím':
            # Ha van 'Artist' és 'Title' kulcs (pl. Bertus API-ból jön közvetlenül)
            artist = vinyl.attr.get('Artist', artist)
            title = vinyl.attr.get('Title', title)
            price = vinyl.attr.get('ListPrice', {}).get('Amount', price) if isinstance(vinyl.attr.get('ListPrice'),
                                                                                       dict) else vinyl.attr.get(
                'ListPrice', price)

        # Bal oldali információk (Előadó és Cím)
        info_label = CTkLabel(row_frame, text=f"{artist} - {title}", font=("Arial", 14, "bold"))
        info_label.pack(side="left", padx=15, pady=10)

        # SKU információ
        sku_label = CTkLabel(row_frame, text=f"SKU: {sku}", font=("Arial", 12))
        sku_label.pack(side="left", padx=15, pady=10)

        # Jobb oldali információ (Ár)
        price_label = CTkLabel(row_frame, text=f"{price} Ft", font=("Arial", 14, "italic"), text_color="#2FA572")
        price_label.pack(side="right", padx=15, pady=10)

    def file_export(self):
        self.app['progress_bar'].grid(row=3, column=1, sticky='ew', pady=20, padx=20)
        self.app['progress_bar'].start()

        location = 'Resources'
        filename = 'shoprenter_import.xml'
        path = os.path.join(os.getcwd(), location, filename)
        TransformerController.export(self.vinyl_list, location, filename)

        # Windows-specifikus explorer megnyitás (csak ha Windows-on fut)
        if os.name == 'nt':
            subprocess.Popen(f'explorer /select, {path}')
        else:
            print(f"Exportálva ide: {path}")

        self.app['progress_bar'].stop()
        self.app['progress_bar'].grid_forget()

    def refresh_preview(self):
        pass

    def _toggle_appearance_mode(self):
        ctk.set_appearance_mode("Light" if ctk.get_appearance_mode() == "Dark" else "Dark")
        self.app['appearance_mode_button'].configure(
            text='☀' if ctk.get_appearance_mode() == "Dark" else '☾',
        )
        self.layout_view.reset_current_ui(self.root)

    def _toggle_theme(self):
        self.layout_view.toggle_theme(self.root)
