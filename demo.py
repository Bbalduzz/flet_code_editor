"""Demo application for the Flet Code Editor."""

import sys
from pathlib import Path

import flet as ft

try:
    from . import CodeEditor, CodeEditorConfig, Python, Rust, get_theme, list_themes
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from flet_code_editor import (
        CodeEditor,
        CodeEditorConfig,
        Python,
        Rust,
        get_theme,
        list_themes,
    )


# Vercel-style color palette
COLORS = {
    "bg": "#000000",
    "bg_elevated": "#0a0a0a",
    "bg_card": "#111111",
    "border": "#1a1a1a",
    "border_hover": "#333333",
    "text_primary": "#ededed",
    "text_secondary": "#888888",
    "text_tertiary": "#666666",
    "accent": "#0070f3",
}


def main(page: ft.Page):
    page.title = "Code Editor"
    page.bgcolor = COLORS["bg"]
    page.padding = 0
    page.fonts = {
        # UI Font
        "Inter": "https://fonts.gstatic.com/s/inter/v13/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuLyfAZ9hiJ-Ek-_EeA.woff2",
        # Monospace / Code Fonts
        "Consolas": "https://github.com/googlefonts/Inconsolata/raw/v3.000/fonts/ttf/Inconsolata-Regular.ttf",
        "JetBrains Mono": "https://fonts.gstatic.com/s/jetbrainsmono/v18/tDbY2o-flEEny0FZhsfKu5WU4zr3E_BX0PnT8RD8yKxjPVmUsaaDhw.woff2",
        "Fira Code": "https://fonts.gstatic.com/s/firacode/v22/uU9NCBsR6Z2vfE9aq3bh0NSDqFGedCMX.woff2",
        "Source Code Pro": "https://raw.githubusercontent.com/adobe-fonts/source-code-pro/release/TTF/SourceCodePro-Regular.ttf",
        "IBM Plex Mono": "https://fonts.gstatic.com/s/ibmplexmono/v19/-F63fjptAgt5VM-kVkqdyU8n3twJ.woff2",
        "Roboto Mono": "https://raw.githubusercontent.com/googlefonts/RobotoMono/main/fonts/ttf/RobotoMono-Regular.ttf",
        # Sans-serif Fonts
        "Open Sans": "https://raw.githubusercontent.com/google/fonts/main/apache/opensans/OpenSans-Regular.ttf",
        "Lato": "https://raw.githubusercontent.com/google/fonts/main/ofl/lato/Lato-Regular.ttf",
        "Montserrat": "https://raw.githubusercontent.com/google/fonts/main/ofl/montserrat/Montserrat-Regular.ttf",
        "Poppins": "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-Regular.ttf",
        # Serif Font
        "Playfair Display": "https://raw.githubusercontent.com/google/fonts/main/ofl/playfairdisplay/PlayfairDisplay-Regular.ttf",
    }

    current_config = CodeEditorConfig(
        show_spaces=False, language=Python, font_family="Consolas"
    )
    state = {
        "line_height_mult": 1.5,
        "current_lang": "python",
        "current_theme": "github_dark",
        "search_regex": False,
        "search_case": False,
        "search_word": False,
        "editor_keyboard_enabled": True,
    }

    SAMPLE_CODE = {
        "python": '''
# Python Example - Fibonacci & Calculator
import os
import json
from typing import Dict, Any

def fibonacci(n: int) -> int:
    """Calculate Fibonacci number recursively."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

class Calculator:
    """A simple calculator with history."""

    @staticmethod
    def add(a: float, b: float) -> float:
        return a + b

    @staticmethod
    def multiply(a: float, b: float) -> float:
        return a * b

    def __init__(self):
        self.result = 0
        self.history: Dict[str, Any] = {"operations": [], "count": 0}

    def compute(self, operation: str, *args) -> float:
        """Execute an operation and store in history."""
        ops = {"add": self.add, "multiply": self.multiply}
        self.result = ops[operation](*args)
        self.history["operations"].append(operation)
        self.history["count"] += 1
        return self.result

# Main execution
if __name__ == "__main__":
    calc = Calculator()
    print(f"Fibonacci(10) = {fibonacci(10)}")
    print(f"5 + 3 = {calc.compute('add', 5, 3)}")
''',
        "rust": """
#[stable(feature = "rust1", since = "1.0.0")]
impl<'a, T, P> Iterator for Split<'a, T, P>
where
    P: FnMut(&T) -> bool,
{
    type Item = &'a [T];

    #[inline]
    fn next(&mut self) -> Option<&'a [T]> {
        if self.finished {
            return None;
        }

        match self.v.iter().position(|x| (self.pred)(x)) {
            None => self.finish(),
            Some(idx) => {
                let ret = Some(&self.v[..idx]);
                self.v = &self.v[idx + 1..];
                ret
            }
        }
    }

    #[inline]
    fn size_hint(&self) -> (usize, Option<usize>) {
        if self.finished { (0, Some(0)) } else { (1, Some(self.v.len() + 1)) }
    }
}
""",
    }

    LANGUAGES = {"python": Python, "rust": Rust}
    FONTS = [
        "Consolas",
        "JetBrains Mono",
        "Fira Code",
        "Source Code Pro",
        "IBM Plex Mono",
        "Roboto Mono",
        "Open Sans",
        "Lato",
        "Montserrat",
        "Poppins",
        "Playfair Display",
    ]
    THEMES = list_themes()

    editor = CodeEditor(SAMPLE_CODE["python"], current_config)

    def update_editor():
        current_config.line_height_px = int(
            current_config.font_size * state["line_height_mult"]
        )
        editor.update_config(current_config)

    # --- Search Bar ---

    def on_input_focus(e):
        state["editor_keyboard_enabled"] = False

    def on_input_blur(e):
        state["editor_keyboard_enabled"] = True

    search_input = ft.TextField(
        hint_text="Search...",
        height=32,
        text_size=12,
        content_padding=ft.padding.symmetric(horizontal=10, vertical=4),
        border_color=COLORS["border"],
        focused_border_color=COLORS["accent"],
        bgcolor=COLORS["bg_elevated"],
        border_radius=6,
        expand=True,
        text_style=ft.TextStyle(font_family="Inter", color=COLORS["text_primary"]),
        hint_style=ft.TextStyle(color=COLORS["text_tertiary"]),
        on_submit=lambda e: do_search(),
        on_focus=on_input_focus,
        on_blur=on_input_blur,
    )

    replace_input = ft.TextField(
        hint_text="Replace...",
        height=32,
        text_size=12,
        content_padding=ft.padding.symmetric(horizontal=10, vertical=4),
        border_color=COLORS["border"],
        focused_border_color=COLORS["accent"],
        bgcolor=COLORS["bg_elevated"],
        border_radius=6,
        width=150,
        text_style=ft.TextStyle(font_family="Inter", color=COLORS["text_primary"]),
        hint_style=ft.TextStyle(color=COLORS["text_tertiary"]),
        on_focus=on_input_focus,
        on_blur=on_input_blur,
    )

    match_count_text = ft.Text(
        "0 results",
        size=11,
        color=COLORS["text_tertiary"],
        font_family="Inter",
        width=70,
    )

    def update_match_count():
        count = editor.search_match_count
        idx = editor.current_search_index
        if count > 0:
            match_count_text.value = f"{idx + 1}/{count}"
        else:
            match_count_text.value = "0 results"
        match_count_text.update()

    def do_search():
        query = search_input.value or ""
        editor.find(
            query,
            regex=state["search_regex"],
            case_sensitive=state["search_case"],
            whole_word=state["search_word"],
        )
        update_match_count()

    def on_search_change(e):
        do_search()

    search_input.on_change = on_search_change

    def on_find_next(e):
        editor.find_next()
        update_match_count()

    def on_find_prev(e):
        editor.find_previous()
        update_match_count()

    def on_replace(e):
        editor.replace_current(replace_input.value or "")
        update_match_count()

    def on_replace_all(e):
        editor.replace_all(replace_input.value or "")
        update_match_count()

    def on_close_search(e):
        editor.clear_search()
        search_input.value = ""
        search_input.update()
        update_match_count()

    def make_toggle_button(label: str, key: str):
        def on_click(e):
            state[key] = not state[key]
            e.control.style.bgcolor = (
                COLORS["accent"] if state[key] else COLORS["bg_card"]
            )
            e.control.update()
            do_search()

        return ft.TextButton(
            label,
            style=ft.ButtonStyle(
                color=COLORS["text_primary"],
                bgcolor=COLORS["accent"] if state[key] else COLORS["bg_card"],
                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                shape=ft.RoundedRectangleBorder(radius=4),
                text_style=ft.TextStyle(size=11, font_family="Inter"),
            ),
            height=26,
            on_click=on_click,
        )

    def icon_button(icon: str, tooltip: str, on_click):
        return ft.IconButton(
            icon=icon,
            icon_size=16,
            icon_color=COLORS["text_secondary"],
            tooltip=tooltip,
            style=ft.ButtonStyle(
                padding=4,
                shape=ft.RoundedRectangleBorder(radius=4),
            ),
            on_click=on_click,
        )

    search_bar = ft.Container(
        content=ft.Row(
            [
                search_input,
                make_toggle_button(".*", "search_regex"),
                make_toggle_button("Aa", "search_case"),
                make_toggle_button("W", "search_word"),
                match_count_text,
                icon_button(ft.Icons.KEYBOARD_ARROW_UP, "Previous", on_find_prev),
                icon_button(ft.Icons.KEYBOARD_ARROW_DOWN, "Next", on_find_next),
                ft.Container(width=1, height=20, bgcolor=COLORS["border"]),
                replace_input,
                ft.TextButton(
                    "Replace",
                    style=ft.ButtonStyle(
                        color=COLORS["text_primary"],
                        bgcolor=COLORS["bg_card"],
                        padding=ft.padding.symmetric(horizontal=10, vertical=4),
                        shape=ft.RoundedRectangleBorder(radius=4),
                        text_style=ft.TextStyle(size=11, font_family="Inter"),
                    ),
                    height=26,
                    on_click=on_replace,
                ),
                ft.TextButton(
                    "All",
                    style=ft.ButtonStyle(
                        color=COLORS["text_primary"],
                        bgcolor=COLORS["bg_card"],
                        padding=ft.padding.symmetric(horizontal=10, vertical=4),
                        shape=ft.RoundedRectangleBorder(radius=4),
                        text_style=ft.TextStyle(size=11, font_family="Inter"),
                    ),
                    height=26,
                    on_click=on_replace_all,
                ),
                icon_button(ft.Icons.CLOSE, "Close", on_close_search),
            ],
            spacing=6,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=COLORS["bg_elevated"],
        padding=ft.padding.symmetric(horizontal=12, vertical=8),
        border=ft.border.only(bottom=ft.BorderSide(1, COLORS["border"])),
    )

    editor_with_search = ft.Column(
        [search_bar, editor],
        spacing=0,
        expand=True,
    )

    # --- Vercel-style UI Components ---

    def section_header(text: str):
        return ft.Container(
            content=ft.Text(
                text,
                size=11,
                weight=ft.FontWeight.W_500,
                color=COLORS["text_tertiary"],
                font_family="Inter",
            ),
            padding=ft.padding.only(bottom=12),
        )

    def setting_card(children: list):
        return ft.Container(
            content=ft.Column(children, spacing=0),
            bgcolor=COLORS["bg_card"],
            border=ft.border.all(1, COLORS["border"]),
            border_radius=10,
            padding=0,
        )

    def setting_row(
        label: str, control: ft.Control, subtitle: str = None, show_border: bool = True
    ):
        content = ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(
                            label,
                            size=13,
                            color=COLORS["text_primary"],
                            font_family="Inter",
                        ),
                    ]
                    + (
                        [
                            ft.Text(
                                subtitle,
                                size=11,
                                color=COLORS["text_tertiary"],
                                font_family="Inter",
                            )
                        ]
                        if subtitle
                        else []
                    ),
                    spacing=2,
                    expand=True,
                ),
                control,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        return ft.Container(
            content=content,
            padding=ft.padding.symmetric(vertical=12, horizontal=14),
            border=ft.border.only(bottom=ft.BorderSide(1, COLORS["border"]))
            if show_border
            else None,
        )

    def toggle_switch(value: bool, on_change):
        return ft.Switch(
            value=value,
            active_color=COLORS["accent"],
            active_track_color=COLORS["accent"],
            inactive_thumb_color=COLORS["text_tertiary"],
            inactive_track_color=COLORS["border"],
            on_change=on_change,
            scale=0.8,
        )

    def dropdown_select(options: list, value: str, on_change, width: int = 130):
        return ft.Dropdown(
            value=value,
            options=[ft.dropdown.Option(o) for o in options],
            text_size=12,
            content_padding=ft.padding.symmetric(horizontal=10, vertical=6),
            border_color=COLORS["border"],
            focused_border_color=COLORS["accent"],
            bgcolor=COLORS["bg_elevated"],
            border_radius=6,
            on_change=on_change,
            width=width,
            text_style=ft.TextStyle(font_family="Inter", color=COLORS["text_primary"]),
        )

    def slider_with_value(
        min_val: float,
        max_val: float,
        value: float,
        on_change,
        label_ref: ft.Ref,
        divisions: int = None,
        format_fn=None,
    ):
        if format_fn is None:
            format_fn = lambda v: str(int(v))

        label = ft.Text(
            format_fn(value),
            size=12,
            color=COLORS["text_primary"],
            font_family="Inter",
            width=35,
            text_align=ft.TextAlign.RIGHT,
            ref=label_ref,
        )

        slider = ft.Slider(
            min=min_val,
            max=max_val,
            value=value,
            divisions=divisions,
            active_color=COLORS["accent"],
            inactive_color=COLORS["border"],
            thumb_color=COLORS["text_primary"],
            on_change=on_change,
            width=100,
        )

        return ft.Row([slider, label], spacing=8)

    def color_input(attr_name: str):
        initial_color = getattr(current_config.theme, attr_name)

        preview = ft.Container(
            width=24,
            height=24,
            bgcolor=initial_color,
            border_radius=4,
            border=ft.border.all(1, COLORS["border"]),
        )

        def on_change(e):
            val = e.control.value
            if len(val) in [4, 7, 9] and val.startswith("#"):
                setattr(current_config.theme, attr_name, val)
                preview.bgcolor = val
                preview.update()
                update_editor()

        return ft.Row(
            [
                preview,
                ft.TextField(
                    value=initial_color,
                    width=90,
                    height=32,
                    text_size=11,
                    content_padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    border_color=COLORS["border"],
                    focused_border_color=COLORS["accent"],
                    bgcolor=COLORS["bg_elevated"],
                    border_radius=4,
                    on_change=on_change,
                    text_style=ft.TextStyle(
                        font_family="JetBrains Mono", color=COLORS["text_primary"]
                    ),
                ),
            ],
            spacing=8,
        )

    # --- Event Handlers ---

    def on_language_change(e):
        lang = e.control.value
        state["current_lang"] = lang
        current_config.language = LANGUAGES[lang]
        editor.set_text(SAMPLE_CODE[lang])
        update_editor()

    def on_theme_change(e):
        theme_name = e.control.value
        state["current_theme"] = theme_name
        current_config.theme = get_theme(theme_name)
        update_editor()
        rebuild_colors()

    def on_font_change(e):
        current_config.font_family = e.control.value
        update_editor()

    font_size_label_ref = ft.Ref[ft.Text]()
    line_height_label_ref = ft.Ref[ft.Text]()

    def on_font_size_change(e):
        current_config.font_size = int(e.control.value)
        if font_size_label_ref.current:
            font_size_label_ref.current.value = str(int(e.control.value))
            font_size_label_ref.current.update()
        update_editor()

    def on_line_height_change(e):
        state["line_height_mult"] = round(e.control.value, 1)
        if line_height_label_ref.current:
            line_height_label_ref.current.value = f"{state['line_height_mult']:.1f}"
            line_height_label_ref.current.update()
        update_editor()

    def on_toggle(attr):
        def handler(e):
            setattr(current_config, attr, e.control.value)
            update_editor()

        return handler

    # --- Color Sections (rebuilt on theme change) ---

    ui_colors_column = ft.Column(spacing=8)
    syntax_colors_column = ft.Column(spacing=8)

    def rebuild_colors():
        ui_colors_column.controls = [
            ft.Row(
                [
                    ft.Text(
                        "Background",
                        size=11,
                        color=COLORS["text_secondary"],
                        width=80,
                        font_family="Inter",
                    ),
                    color_input("editor_bg"),
                ]
            ),
            ft.Row(
                [
                    ft.Text(
                        "Foreground",
                        size=11,
                        color=COLORS["text_secondary"],
                        width=80,
                        font_family="Inter",
                    ),
                    color_input("editor_fg"),
                ]
            ),
            ft.Row(
                [
                    ft.Text(
                        "Selection",
                        size=11,
                        color=COLORS["text_secondary"],
                        width=80,
                        font_family="Inter",
                    ),
                    color_input("selection_bg"),
                ]
            ),
            ft.Row(
                [
                    ft.Text(
                        "Cursor",
                        size=11,
                        color=COLORS["text_secondary"],
                        width=80,
                        font_family="Inter",
                    ),
                    color_input("cursor_bg"),
                ]
            ),
            ft.Row(
                [
                    ft.Text(
                        "Line Num",
                        size=11,
                        color=COLORS["text_secondary"],
                        width=80,
                        font_family="Inter",
                    ),
                    color_input("line_number_fg"),
                ]
            ),
        ]
        syntax_colors_column.controls = [
            ft.Row(
                [
                    ft.Text(
                        "Keyword",
                        size=11,
                        color=COLORS["text_secondary"],
                        width=80,
                        font_family="Inter",
                    ),
                    color_input("keyword"),
                ]
            ),
            ft.Row(
                [
                    ft.Text(
                        "Function",
                        size=11,
                        color=COLORS["text_secondary"],
                        width=80,
                        font_family="Inter",
                    ),
                    color_input("function"),
                ]
            ),
            ft.Row(
                [
                    ft.Text(
                        "String",
                        size=11,
                        color=COLORS["text_secondary"],
                        width=80,
                        font_family="Inter",
                    ),
                    color_input("string"),
                ]
            ),
            ft.Row(
                [
                    ft.Text(
                        "Comment",
                        size=11,
                        color=COLORS["text_secondary"],
                        width=80,
                        font_family="Inter",
                    ),
                    color_input("comment"),
                ]
            ),
            ft.Row(
                [
                    ft.Text(
                        "Number",
                        size=11,
                        color=COLORS["text_secondary"],
                        width=80,
                        font_family="Inter",
                    ),
                    color_input("number"),
                ]
            ),
            ft.Row(
                [
                    ft.Text(
                        "Class",
                        size=11,
                        color=COLORS["text_secondary"],
                        width=80,
                        font_family="Inter",
                    ),
                    color_input("class_name"),
                ]
            ),
            ft.Row(
                [
                    ft.Text(
                        "Decorator",
                        size=11,
                        color=COLORS["text_secondary"],
                        width=80,
                        font_family="Inter",
                    ),
                    color_input("decorator"),
                ]
            ),
            ft.Row(
                [
                    ft.Text(
                        "Instance",
                        size=11,
                        color=COLORS["text_secondary"],
                        width=80,
                        font_family="Inter",
                    ),
                    color_input("instance"),
                ]
            ),
        ]
        if page.controls:
            ui_colors_column.update()
            syntax_colors_column.update()

    rebuild_colors()

    # --- Settings Panel Layout ---

    settings_content = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=20,
        controls=[
            # Header
            ft.Container(
                content=ft.Text(
                    "Settings",
                    size=18,
                    weight=ft.FontWeight.W_600,
                    color=COLORS["text_primary"],
                    font_family="Inter",
                ),
                padding=ft.padding.only(top=8, bottom=4),
            ),
            # Language & Theme
            ft.Column(
                [
                    section_header("EDITOR"),
                    setting_card(
                        [
                            setting_row(
                                "Language",
                                dropdown_select(
                                    list(LANGUAGES.keys()),
                                    state["current_lang"],
                                    on_language_change,
                                    width=110,
                                ),
                                "Syntax highlighting",
                            ),
                            setting_row(
                                "Theme",
                                dropdown_select(
                                    THEMES,
                                    state["current_theme"],
                                    on_theme_change,
                                    width=110,
                                ),
                                "Color scheme",
                                show_border=False,
                            ),
                        ]
                    ),
                ],
                spacing=0,
            ),
            # Typography
            ft.Column(
                [
                    section_header("TYPOGRAPHY"),
                    setting_card(
                        [
                            setting_row(
                                "Font Family",
                                dropdown_select(
                                    FONTS,
                                    current_config.font_family,
                                    on_font_change,
                                    width=140,
                                ),
                            ),
                            setting_row(
                                "Font Size",
                                slider_with_value(
                                    min_val=8,
                                    max_val=32,
                                    value=current_config.font_size,
                                    on_change=on_font_size_change,
                                    label_ref=font_size_label_ref,
                                    divisions=24,
                                ),
                                "8 - 32 px",
                            ),
                            setting_row(
                                "Line Height",
                                slider_with_value(
                                    min_val=1.0,
                                    max_val=2.5,
                                    value=state["line_height_mult"],
                                    on_change=on_line_height_change,
                                    label_ref=line_height_label_ref,
                                    divisions=15,
                                    format_fn=lambda v: f"{v:.1f}",
                                ),
                                "1.0 - 2.5x",
                                show_border=False,
                            ),
                        ]
                    ),
                ],
                spacing=0,
            ),
            # Display Options
            ft.Column(
                [
                    section_header("DISPLAY"),
                    setting_card(
                        [
                            setting_row(
                                "Line Numbers",
                                toggle_switch(
                                    current_config.show_line_numbers,
                                    on_toggle("show_line_numbers"),
                                ),
                                "Show gutter",
                            ),
                            setting_row(
                                "Whitespace",
                                toggle_switch(
                                    current_config.show_spaces, on_toggle("show_spaces")
                                ),
                                "Render spaces",
                            ),
                            setting_row(
                                "Tabs",
                                toggle_switch(
                                    current_config.show_tabs, on_toggle("show_tabs")
                                ),
                                "Render tabs",
                            ),
                            setting_row(
                                "Line Breaks",
                                toggle_switch(
                                    current_config.show_line_breaks,
                                    on_toggle("show_line_breaks"),
                                ),
                                "Render newlines",
                                show_border=False,
                            ),
                        ]
                    ),
                ],
                spacing=0,
            ),
            # UI Colors
            ft.Column(
                [
                    section_header("INTERFACE COLORS"),
                    ft.Container(
                        content=ui_colors_column,
                        bgcolor=COLORS["bg_card"],
                        border=ft.border.all(1, COLORS["border"]),
                        border_radius=10,
                        padding=14,
                    ),
                ],
                spacing=0,
            ),
            # Syntax Colors
            ft.Column(
                [
                    section_header("SYNTAX COLORS"),
                    ft.Container(
                        content=syntax_colors_column,
                        bgcolor=COLORS["bg_card"],
                        border=ft.border.all(1, COLORS["border"]),
                        border_radius=10,
                        padding=14,
                    ),
                ],
                spacing=0,
            ),
            # Footer
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text(
                            "flet-code-editor",
                            size=11,
                            color=COLORS["text_tertiary"],
                            font_family="Inter",
                        ),
                        ft.Text(
                            "v0.1.0",
                            size=11,
                            color=COLORS["text_tertiary"],
                            font_family="Inter",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                padding=ft.padding.only(top=8, bottom=16),
            ),
        ],
    )

    settings_panel = ft.Container(
        content=settings_content,
        width=300,
        bgcolor=COLORS["bg_elevated"],
        padding=ft.padding.symmetric(horizontal=16),
        border=ft.border.only(left=ft.BorderSide(1, COLORS["border"])),
    )

    layout = ft.Row([editor_with_search, settings_panel], expand=True, spacing=0)

    def handle_keyboard(e):
        if state["editor_keyboard_enabled"]:
            editor.handle_keyboard_event(e)

    page.on_keyboard_event = handle_keyboard
    page.add(layout)


if __name__ == "__main__":
    ft.app(target=main)
