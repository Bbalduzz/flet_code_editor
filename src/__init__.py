"""Source modules for the Flet Code Editor."""

from .config import CodeEditorConfig, Theme
from .document import Document
from .editor import CodeEditor
from .highlighter import Highlighter
from .languages import JSON, Language, Python, Rust
from .operations import Cursor, OpCode, Operation
from .search import Search, SearchMatch
from .themes import (
    AYU_DARK,
    DRACULA,
    GITHUB_DARK,
    MONOKAI,
    ONE_DARK,
    SOLARIZED_DARK,
    CodeEditorTheme,
    get_theme,
    list_themes,
)
from .view import View, ViewLine

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
    # Search
    "Search",
    "SearchMatch",
    # View
    "View",
    "ViewLine",
    "Highlighter",
    # Languages
    "Language",
    "JSON",
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
