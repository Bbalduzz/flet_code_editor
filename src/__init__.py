"""Source modules for the Flet Code Editor."""

from .config import CodeEditorConfig, Theme
from .document import Document
from .editor import CodeEditor
from .highlighter import Highlighter
from .operations import Cursor, OpCode, Operation
from .view import View, ViewLine
from .languages import Language, Python, Rust
from .themes import (
    CodeEditorTheme,
    GITHUB_DARK,
    MONOKAI,
    DRACULA,
    SOLARIZED_DARK,
    ONE_DARK,
    AYU_DARK,
    get_theme,
    list_themes,
)

__all__ = [
    # Main components
    "CodeEditor",
    "CodeEditorConfig",
    "Theme",
    "Document",
    # Operations
    "OpCode",
    "Operation",
    "Cursor",
    # View
    "View",
    "ViewLine",
    "Highlighter",
    # Languages
    "Language",
    "Python",
    "Rust",
    # Themes
    "CodeEditorTheme",
    "GITHUB_DARK",
    "MONOKAI",
    "DRACULA",
    "SOLARIZED_DARK",
    "ONE_DARK",
    "AYU_DARK",
    "get_theme",
    "list_themes",
]
