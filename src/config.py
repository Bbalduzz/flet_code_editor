"""Configuration dataclasses for the Flet Code Editor."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, Type

if TYPE_CHECKING:
    from .languages.base import Language


@dataclass
class Theme:
    """Color theme configuration for the editor."""

    name: str = "GitHub Dark"

    # Editor UI colors
    editor_bg: str = "#0D1117"
    editor_fg: str = "#c9d1d9"
    line_number_fg: str = "#484f58"
    line_number_bg: str = "#0D1117"
    selection_bg: str = "#264f78"
    cursor_bg: str = "#c9d1d9"
    cursor_fg: str = "#0D1117"
    invisible_fg: str = "#30363d"

    # Syntax highlighting colors
    keyword: str = "#ff7b72"
    function: str = "#d2a8ff"
    string: str = "#a5d6ff"
    comment: str = "#8b949e"
    class_name: str = "#79c0ff"
    number: str = "#79c0ff"
    docstring: str = "#a5d6ff"
    decorator: str = "#d2a8ff"
    instance: str = "#ffa657"
    builtin: str = "#79c0ff"
    exception: str = "#f85149"
    function_call: str = "#d2a8ff"


@dataclass
class CodeEditorConfig:
    """Configuration for the code editor."""

    theme: Theme = field(default_factory=Theme)
    language: Optional[Type[Language]] = None  # Defaults to Python
    font_family: str = "Consolas"
    font_size: int = 14
    line_height_px: int = 20
    show_line_numbers: bool = True
    show_tabs: bool = False
    show_spaces: bool = False

    def __post_init__(self):
        if self.language is None:
            from .languages import Python
            self.language = Python
