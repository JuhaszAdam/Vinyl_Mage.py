import os

import customtkinter as ctk
from customtkinter import ThemeManager


class LayoutView:
    available_themes = ['blue', 'dark-blue', 'green']
    current_theme_index = 0

    def __init__(self):
        try:
            themes_dir = self._determine_themes_dir()
            files = os.listdir(themes_dir)
            for file in files:
                self.available_themes.append(themes_dir + '/' + file)
        except FileNotFoundError:
            pass

        ctk.set_appearance_mode("system")
        self.current_theme_index = 0
        ctk.set_appearance_mode("system")

    def get_current_theme(self):
        return self.available_themes[self.current_theme_index]

    @staticmethod
    def _determine_themes_dir():
        return ('/'.join(os.path.abspath(__file__).split('\\')[:-2])) + "/themes"

    def reset_current_ui(self, root):
        self._recursive_reset_ui(root)

    def _recursive_reset_ui(self, widget):
        if bool(widget.children):
            for key, subwidget in widget.children.items():
                self._recursive_reset_ui(subwidget)

        try:
            dark_mode = 0 if ctk.get_appearance_mode() == "Light" else 1
            match type(widget).__name__:
                case "CTkMenuBar":
                    widget.configure(
                        background=ThemeManager.theme['CTk']['fg_color'][1],
                        foreground=ThemeManager.theme['CTkButton']['text_color'][dark_mode],
                        activebackground=ThemeManager.theme['CTkButton']['fg_color'][dark_mode],
                        activeforeground=ThemeManager.theme['CTkButton']['text_color'][dark_mode],
                    )

                case "CTk":
                    widget.configure(
                        fg_color=ThemeManager.theme['CTk']['fg_color'],
                    )
                case "CTkToplevel":
                    widget.configure(
                        fg_color=ThemeManager.theme['CTkToplevel']['fg_color'],
                    )
                case "CTkFrame":
                    widget.configure(
                        corner_radius=ThemeManager.theme['CTkFrame']['corner_radius'],
                        border_width=ThemeManager.theme['CTkFrame']['border_width'],
                        fg_color=ThemeManager.theme['CTk']['fg_color'],
                        top_fg_color=ThemeManager.theme['CTkFrame']['top_fg_color'],
                        border_color=ThemeManager.theme['CTkFrame']['border_color'],
                    )
                case "CTkButton":
                    if hasattr(widget, 'widgetName') and widget.widgetName == "menubar":
                        widget.configure(
                            fg_color="transparent" if dark_mode else ThemeManager.theme['CTkButton']['fg_color'],
                            border_color=ThemeManager.theme['CTkButton']['fg_color'] if dark_mode else
                            ThemeManager.theme['CTkButton']['border_color'],
                            border_width=1 if dark_mode else ThemeManager.theme['CTkButton']['border_width'],
                            text_color=ThemeManager.theme['CTkButton']['text_color'],
                            hover_color=ThemeManager.theme['CTkButton']['hover_color'],
                            corner_radius=ThemeManager.theme['CTkButton']['corner_radius'],
                            text_color_disabled=ThemeManager.theme['CTkButton']['text_color_disabled'],
                        )
                    else:
                        widget.configure(
                            fg_color=ThemeManager.theme['CTkButton']['fg_color'],
                            border_color=ThemeManager.theme['CTkButton']['border_color'],
                            border_width=ThemeManager.theme['CTkButton']['border_width'],
                            text_color=ThemeManager.theme['CTkButton']['text_color'],
                            hover_color=ThemeManager.theme['CTkButton']['hover_color'],
                            corner_radius=ThemeManager.theme['CTkButton']['corner_radius'],
                            text_color_disabled=ThemeManager.theme['CTkButton']['text_color_disabled'],
                        )
                case "CTkLabel":
                    if hasattr(widget, 'widgetName'):
                        if widget.widgetName == "user_chat":
                            widget.configure(
                                corner_radius=ThemeManager.theme['CTkButton']['corner_radius'],
                                fg_color=ThemeManager.theme["CTkFrame"]["fg_color"],
                                bg_color=ThemeManager.theme['CTkTextbox']['fg_color'][dark_mode],
                                text_color=ThemeManager.theme['CTkLabel']['text_color'],
                            )
                        elif widget.widgetName == "ai_chat":
                            widget.configure(
                                corner_radius=ThemeManager.theme['CTkButton']['corner_radius'],
                                fg_color=ThemeManager.theme["CTkButton"]["fg_color"],
                                bg_color=ThemeManager.theme['CTkTextbox']['fg_color'],
                                text_color=ThemeManager.theme['CTkLabel']['text_color'],
                            )
                        else:
                            widget.configure(
                                corner_radius=ThemeManager.theme['CTkButton']['corner_radius'],
                                fg_color=ThemeManager.theme['CTkLabel']['fg_color'],
                                bg_color=ThemeManager.theme['CTkTextbox']['fg_color'],
                                text_color=ThemeManager.theme['CTkLabel']['text_color'],
                            )
                case "CTkEntry":
                    widget.configure(
                        corner_radius=ThemeManager.theme['CTkEntry']['corner_radius'],
                        border_width=ThemeManager.theme['CTkEntry']['border_width'],
                        fg_color=ThemeManager.theme['CTkEntry']['fg_color'],
                        border_color=ThemeManager.theme['CTkEntry']['border_color'],
                        text_color=ThemeManager.theme['CTkEntry']['text_color'],
                    )
                case "CTkCheckBox":
                    widget.configure(
                        corner_radius=ThemeManager.theme['CTkCheckBox']['corner_radius'],
                        border_width=ThemeManager.theme['CTkCheckBox']['border_width'],
                        fg_color=ThemeManager.theme['CTkCheckBox']['fg_color'],
                        border_color=ThemeManager.theme['CTkCheckBox']['border_color'],
                        hover_color=ThemeManager.theme['CTkCheckBox']['hover_color'],
                        checkmark_color=ThemeManager.theme['CTkCheckBox']['checkmark_color'],
                        text_color=ThemeManager.theme['CTkCheckBox']['text_color'],
                        text_color_disabled=ThemeManager.theme['CTkCheckBox']['text_color_disabled'],
                    )
                case "CTkSwitch":
                    widget.configure(
                        corner_radius=ThemeManager.theme['CTkSwitch']['corner_radius'],
                        border_width=ThemeManager.theme['CTkSwitch']['border_width'],
                        button_length=ThemeManager.theme['CTkSwitch']['button_length'],
                        fg_color=ThemeManager.theme['CTkSwitch']['fg_color'],
                        progress_color=ThemeManager.theme['CTkSwitch']['progress_color'],
                        button_color=ThemeManager.theme['CTkSwitch']['button_color'],
                        button_hover_color=ThemeManager.theme['CTkSwitch']['button_hover_color'],
                        text_color=ThemeManager.theme['CTkSwitch']['text_color'],
                        text_color_disabled=ThemeManager.theme['CTkSwitch']['text_color_disabled'],
                    )
                case "CTkRadioButton":
                    widget.configure(
                        corner_radius=ThemeManager.theme['CTkRadioButton']['corner_radius'],
                        border_width_checked=ThemeManager.theme['CTkRadioButton']['border_width_checked'],
                        border_width_unchecked=ThemeManager.theme['CTkRadioButton']['border_width_unchecked'],
                        fg_color=ThemeManager.theme['CTkRadioButton']['fg_color'],
                        border_color=ThemeManager.theme['CTkRadioButton']['border_color'],
                        hover_color=ThemeManager.theme['CTkRadioButton']['hover_color'],
                        text_color=ThemeManager.theme['CTkRadioButton']['text_color'],
                        text_color_disabled=ThemeManager.theme['CTkRadioButton']['text_color_disabled'],
                    )
                case "CTkProgressBar":
                    widget.configure(
                        corner_radius=ThemeManager.theme['CTkProgressBar']['corner_radius'],
                        border_width=ThemeManager.theme['CTkProgressBar']['border_width'],
                        fg_color=ThemeManager.theme['CTkProgressBar']['fg_color'],
                        progress_color=ThemeManager.theme['CTkProgressBar']['progress_color'],
                        border_color=ThemeManager.theme['CTkProgressBar']['border_color'],
                    )
                case "CTkSlider":
                    widget.configure(
                        corner_radius=ThemeManager.theme['CTkSlider']['corner_radius'],
                        button_corner_radius=ThemeManager.theme['CTkSlider']['button_corner_radius'],
                        border_width=ThemeManager.theme['CTkSlider']['border_width'],
                        button_length=ThemeManager.theme['CTkSlider']['button_length'],
                        fg_color=ThemeManager.theme['CTkSlider']['fg_color'],
                        progress_color=ThemeManager.theme['CTkSlider']['progress_color'],
                        button_color=ThemeManager.theme['CTkSlider']['button_color'],
                        button_hover_color=ThemeManager.theme['CTkSlider']['button_hover_color'],
                    )
                case "CTkOptionMenu":
                    widget.configure(
                        corner_radius=ThemeManager.theme['CTkOptionMenu']['corner_radius'],
                        fg_color=ThemeManager.theme['CTkOptionMenu']['fg_color'],
                        button_color=ThemeManager.theme['CTkOptionMenu']['button_color'],
                        button_hover_color=ThemeManager.theme['CTkOptionMenu']['button_hover_color'],
                        text_color=ThemeManager.theme['CTkOptionMenu']['text_color'],
                        text_color_disabled=ThemeManager.theme['CTkOptionMenu']['text_color_disabled'],
                    )
                case "CTkComboBox":
                    widget.configure(
                        corner_radius=ThemeManager.theme['CTkComboBox']['corner_radius'],
                        border_width=ThemeManager.theme['CTkComboBox']['border_width'],
                        fg_color=ThemeManager.theme['CTkComboBox']['fg_color'],
                        border_color=ThemeManager.theme['CTkComboBox']['border_color'],
                        button_color=ThemeManager.theme['CTkComboBox']['button_color'],
                        button_hover_color=ThemeManager.theme['CTkComboBox']['button_hover_color'],
                        text_color=ThemeManager.theme['CTkComboBox']['text_color'],
                        text_color_disabled=ThemeManager.theme['CTkComboBox']['text_color_disabled'],
                    )

                case "CTkScrollbar":
                    widget.configure(
                        corner_radius=ThemeManager.theme['CTkScrollbar']['corner_radius'],
                        border_spacing=ThemeManager.theme['CTkScrollbar']['border_spacing'],
                        fg_color=ThemeManager.theme['CTkScrollbar']['fg_color'],
                        button_color=ThemeManager.theme['CTkScrollbar']['button_color'],
                        button_hover_color=ThemeManager.theme['CTkScrollbar']['button_hover_color'],
                    )
                case "CTkSegmentedButton":
                    widget.configure(
                        corner_radius=ThemeManager.theme['CTkSegmentedButton']['corner_radius'],
                        border_width=ThemeManager.theme['CTkSegmentedButton']['border_width'],
                        fg_color=ThemeManager.theme['CTkSegmentedButton']['fg_color'],
                        selected_color=ThemeManager.theme['CTkSegmentedButton']['selected_color'],
                        selected_hover_color=ThemeManager.theme['CTkSegmentedButton']['selected_hover_color'],
                        unselected_color=ThemeManager.theme['CTkSegmentedButton']['unselected_color'],
                        unselected_hover_color=ThemeManager.theme['CTkSegmentedButton']['unselected_hover_color'],
                        text_color=ThemeManager.theme['CTkSegmentedButton']['text_color'],
                        text_color_disabled=ThemeManager.theme['CTkSegmentedButton']['text_color_disabled'],
                    )
                case "CTkTextbox":
                    widget.configure(
                        corner_radius=ThemeManager.theme['CTkTextbox']['corner_radius'],
                        border_width=ThemeManager.theme['CTkTextbox']['border_width'],
                        fg_color=ThemeManager.theme['CTkTextbox']['fg_color'],
                        border_color=ThemeManager.theme['CTkTextbox']['border_color'],
                        text_color=ThemeManager.theme['CTkTextbox']['text_color'],
                        scrollbar_button_color=ThemeManager.theme['CTkTextbox']['scrollbar_button_color'],
                        scrollbar_button_hover_color=ThemeManager.theme['CTkTextbox']['scrollbar_button_hover_color'],
                    )
                case "Text":
                    widget.configure(
                        fg=ThemeManager.theme['CTkFrame']['fg_color'][dark_mode],
                        bg=ThemeManager.theme['CTkTextbox']['fg_color'][dark_mode],
                        bd=ThemeManager.theme['CTkTextbox']['border_width'],
                    )
                case "CTkScrollableFrame":
                    widget.configure(
                        corner_radius=ThemeManager.theme['CTkScrollableFrame']['corner_radius'],
                    )
                case "DropdownMenu":
                    widget.configure(
                        fg_color=ThemeManager.theme['DropdownMenu']['fg_color'],
                        hover_color=ThemeManager.theme['DropdownMenu']['hover_color'],
                        text_color=ThemeManager.theme['DropdownMenu']['text_color'],
                    )
                case _:
                    pass
        except ValueError as e:
            pass

    def toggle_theme(self, root):
        theme_name = self.available_themes[self.current_theme_index]
        ctk.set_default_color_theme(theme_name)
        self.current_theme_index = (self.current_theme_index + 1) % len(self.available_themes)
        self.reset_current_ui(root)
