"""Flet Code Editor - A syntax-highlighting code editor component for Flet."""

from .src import (
    CodeEditorConfig,
    Theme,
    Document,
    CodeEditor,
    Highlighter,
    Cursor,
    OpCode,
    Operation,
    View,
    ViewLine,
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
