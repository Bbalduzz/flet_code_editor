"""Demo application for the Flet Code Editor."""

import sys
from pathlib import Path

import flet as ft

try:
    from . import CodeEditor, CodeEditorConfig, get_theme, list_themes
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from flet_code_editor import CodeEditor, CodeEditorConfig, get_theme, list_themes


def main(page: ft.Page):
    page.title = "Flet Code Editor"
    page.bgcolor = "#0D1117"
    page.padding = 0
    page.window_focused = True
    page.fonts = {
        "Consolas": "https://github.com/googlefonts/Inconsolata/raw/v3.000/fonts/ttf/Inconsolata-Regular.ttf",
        "Roboto Mono": "https://raw.githubusercontent.com/googlefonts/RobotoMono/main/fonts/ttf/RobotoMono-Regular.ttf",
        "Source Code Pro": "https://github.com/adobe-fonts/source-code-pro/raw/release/TTF/SourceCodePro-Regular.ttf",
        "Open Sans": "https://raw.githubusercontent.com/google/fonts/main/apache/opensans/OpenSans-Regular.ttf",
        "Lato": "https://raw.githubusercontent.com/google/fonts/main/ofl/lato/Lato-Regular.ttf",
        "Montserrat": "https://raw.githubusercontent.com/google/fonts/main/ofl/montserrat/Montserrat-Regular.ttf",
        "Playfair Display": "https://raw.githubusercontent.com/google/fonts/main/ofl/playfairdisplay/PlayfairDisplay-Regular.ttf",
        "Poppins": "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-Regular.ttf",
    }

    current_config = CodeEditorConfig(show_spaces=True)
    state = {"line_height_mult": 1.5}

    code = """# Python code example
import os
import json

def fibonacci(n):
    '''Calculate Fibonacci recursively'''
    if n <= 1: return n
    return fibonacci(n-1) + fibonacci(n-2)

class Calculator:
    @staticmethod
    def add(a, b):
        return a + b

    def __init__(self):
        self.result = 0
        self.data = {"status": True, "value": None}
"""
    editor = CodeEditor(code, current_config)

    def update_editor():
        current_config.line_height_px = int(
            current_config.font_size * state["line_height_mult"]
        )
        editor.update_config(current_config)

    def create_color_option(label: str, attr_name: str):
        obj = current_config.theme
        initial_color = getattr(obj, attr_name)

        color_preview = ft.Container(
            width=24,
            height=24,
            bgcolor=initial_color,
            border_radius=4,
            border=ft.border.all(1, "#30363d"),
        )

        def on_color_change(e):
            val = e.control.value
            if len(val) in [4, 7, 9] and val.startswith("#"):
                try:
                    setattr(current_config.theme, attr_name, val)
                    color_preview.bgcolor = val
                    color_preview.update()
                    update_editor()
                except:
                    pass

        return ft.Row(
            controls=[
                color_preview,
                ft.TextField(
                    value=initial_color,
                    label=label,
                    text_size=12,
                    height=35,
                    content_padding=10,
                    expand=True,
                    on_change=on_color_change,
                    border_color="#30363d",
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def on_font_size_change(e):
        current_config.font_size = int(e.control.value)
        update_editor()

    def on_line_height_change(e):
        state["line_height_mult"] = e.control.value
        update_editor()

    def on_font_family_change(e):
        current_config.font_family = e.control.value
        update_editor()

    def on_theme_change(e):
        theme = get_theme(e.control.value)
        current_config.theme = theme
        page.bgcolor = theme.editor_bg
        update_editor()
        page.update()

    theme_dd = ft.Dropdown(
        label="Theme",
        value="github_dark",
        options=[ft.dropdown.Option(name) for name in list_themes()],
        text_size=12,
        content_padding=10,
        on_change=on_theme_change,
    )

    font_family_dd = ft.Dropdown(
        label="Font Family",
        value="Consolas",
        options=[
            ft.dropdown.Option("Consolas"),
            ft.dropdown.Option("Roboto Mono"),
            ft.dropdown.Option("Source Code Pro"),
            ft.dropdown.Option("Courier New"),
            ft.dropdown.Option("Open Sans"),
            ft.dropdown.Option("Lato"),
            ft.dropdown.Option("Montserrat"),
            ft.dropdown.Option("Playfair Display"),
            ft.dropdown.Option("Poppins"),
        ],
        text_size=12,
        content_padding=10,
        on_change=on_font_family_change,
    )

    slider_font_size = ft.Slider(
        min=8,
        max=32,
        divisions=24,
        value=14,
        label="{value}px",
        on_change=on_font_size_change,
    )
    slider_line_height = ft.Slider(
        min=1.0,
        max=2.5,
        divisions=30,
        value=1.5,
        label="{value}x",
        on_change=on_line_height_change,
    )

    def on_toggle_change(e, attr):
        setattr(current_config, attr, e.control.value)
        update_editor()

    toggles = ft.Column(
        [
            ft.Switch(
                label="Line Numbers",
                value=True,
                on_change=lambda e: on_toggle_change(e, "show_line_numbers"),
            ),
            ft.Switch(
                label="Show Spaces",
                value=True,
                on_change=lambda e: on_toggle_change(e, "show_spaces"),
            ),
            ft.Switch(
                label="Show Tabs",
                value=False,
                on_change=lambda e: on_toggle_change(e, "show_tabs"),
            ),
        ]
    )

    ui_colors = ft.Column(
        [
            create_color_option("Background", "editor_bg"),
            create_color_option("Text Color", "editor_fg"),
            create_color_option("Selection", "selection_bg"),
            create_color_option("Cursor", "cursor_bg"),
            create_color_option("Line Num BG", "line_number_bg"),
            create_color_option("Line Num FG", "line_number_fg"),
        ],
        spacing=10,
    )

    syntax_colors = ft.Column(
        [
            create_color_option("Keyword", "keyword"),
            create_color_option("Function Def", "function"),
            create_color_option("Function Call", "function_call"),
            create_color_option("String", "string"),
            create_color_option("Comment", "comment"),
            create_color_option("Class Name", "class_name"),
            create_color_option("Number", "number"),
            create_color_option("Decorator", "decorator"),
            create_color_option("Instance (self)", "instance"),
            create_color_option("Built-ins", "builtin"),
        ],
        spacing=10,
    )

    settings_content = ft.Column(
        scroll=ft.ScrollMode.HIDDEN,
        expand=True,
        controls=[
            ft.Text("Theme", weight=ft.FontWeight.BOLD, color="white"),
            theme_dd,
            ft.Divider(color="#30363d"),
            ft.Text("Typography", weight=ft.FontWeight.BOLD, color="white"),
            font_family_dd,
            ft.Text("Font Size", size=12, color="grey"),
            slider_font_size,
            ft.Text("Line Height", size=12, color="grey"),
            slider_line_height,
            ft.Divider(color="#30363d"),
            ft.Text("Display", weight=ft.FontWeight.BOLD, color="white"),
            toggles,
            ft.Divider(color="#30363d"),
            ft.ExpansionTile(
                title=ft.Text("Interface Colors", size=14, weight=ft.FontWeight.W_500),
                controls=[ft.Container(content=ui_colors, padding=10)],
                collapsed_text_color="#c9d1d9",
                text_color="white",
                maintain_state=True,
                initially_expanded=False,
                bgcolor="#0D1117",
            ),
            ft.ExpansionTile(
                title=ft.Text(
                    "Syntax Highlighting", size=14, weight=ft.FontWeight.W_500
                ),
                controls=[ft.Container(content=syntax_colors, padding=10)],
                collapsed_text_color="#c9d1d9",
                text_color="white",
                maintain_state=True,
                initially_expanded=False,
                bgcolor="#0D1117",
            ),
        ],
    )

    settings_panel = ft.Container(
        width=320,
        bgcolor="#161b22",
        padding=15,
        border=ft.border.only(left=ft.border.BorderSide(1, "#30363d")),
        content=ft.Column(
            [
                ft.Text(
                    "Appearance",
                    size=20,
                    font_family="Consolas",
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Divider(color="#30363d"),
                ft.Container(content=settings_content, expand=True),
            ]
        ),
    )

    layout = ft.Row([editor, settings_panel], expand=True, spacing=0)

    page.on_keyboard_event = editor.handle_keyboard_event
    page.add(layout)


if __name__ == "__main__":
    ft.app(target=main)
