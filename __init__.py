"""Flet Code Editor - A syntax-highlighting code editor component for Flet."""

from .src import (
    AYU_DARK,
    DRACULA,
    GITHUB_DARK,
    JSON,
    MONOKAI,
    ONE_DARK,
    SOLARIZED_DARK,
    CodeEditor,
    CodeEditorConfig,
    CodeEditorTheme,
    Cursor,
    Document,
    Highlighter,
    Language,
    OpCode,
    Operation,
    Python,
    Rust,
    Theme,
    View,
    ViewLine,
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
    "JSON",
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

__version__ = "0.1.0"
