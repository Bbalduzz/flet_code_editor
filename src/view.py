"""View components for the code editor."""

from typing import List, Optional

import flet as ft

from .config import CodeEditorConfig
from .document import Document
from .highlighter import Highlighter


class ViewLine(ft.Container):
    """Renders a single line of the editor with line number gutter."""

    def __init__(
        self,
        line_number: int,
        text: str,
        document: Document,
        highlighter: Highlighter,
        max_line_num: int,
        config: CodeEditorConfig,
        search_matches: Optional[List] = None,
        current_match_index: int = -1,
    ):
        super().__init__()
        gutter_width = len(str(max_line_num)) * (config.font_size * 0.7) + 20
        spans = highlighter.run(
            text, line_number, document, search_matches, current_match_index
        )

        gutter_content = None
        if config.show_line_numbers:
            gutter_content = ft.Text(
                f"{line_number + 1} ",
                size=config.font_size,
                color=config.theme.line_number_fg,
                font_family=config.font_family,
                text_align=ft.TextAlign.RIGHT,
            )

        self.content = ft.Row(
            controls=[
                ft.Container(
                    content=gutter_content,
                    width=gutter_width if config.show_line_numbers else 0,
                    bgcolor=config.theme.line_number_bg,
                    alignment=ft.alignment.center_right,
                    padding=ft.padding.only(right=5),
                ),
                ft.Container(
                    content=ft.Text(
                        spans=spans,
                        size=config.font_size,
                        font_family=config.font_family,
                        no_wrap=False,
                    ),
                    padding=ft.padding.only(left=5),
                    expand=True,
                ),
            ],
            spacing=0,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
        self.bgcolor = config.theme.editor_bg
        self.height = config.line_height_px


class View(ft.ListView):
    """Virtualized view that renders all lines of the document."""

    def __init__(
        self, document: Document, highlighter: Highlighter, config: CodeEditorConfig
    ):
        super().__init__()
        self.document = document
        self.highlighter = highlighter
        self.config = config
        self.spacing = 0
        self.item_extent = config.line_height_px
        self.expand = True
        self.bgcolor = config.theme.editor_bg

        # Search state (set by CodeEditor)
        self.search_matches: Optional[List] = None
        self.current_match_index: int = -1

        self.render(init=True)

    def render(self, init=False):
        """Render all lines of the document."""
        new_controls = []
        max_line = len(self.document.lines)
        for idx, line_text in enumerate(self.document.lines):
            new_controls.append(
                ViewLine(
                    idx,
                    line_text,
                    self.document,
                    self.highlighter,
                    max_line,
                    self.config,
                    self.search_matches,
                    self.current_match_index,
                )
            )
        self.controls = new_controls

        if not init and self.page:
            try:
                self.update()
                self.scroll_to(key=str(self.document.cursor.line), duration=0)
            except:
                pass
