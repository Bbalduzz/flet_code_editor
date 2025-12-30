"""Base language class for syntax highlighting."""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple


class Language(ABC):
    """Abstract base class for language definitions."""

    name: str = "unknown"
    tree_sitter_module: Optional[str] = None
    tree_sitter_query: str = ""
    regex_patterns: List[Tuple[str, str]] = []  # List of (pattern, token_type)

    # Smart indentation settings
    indent_triggers: List[str] = [
        ":"
    ]  # Characters that trigger extra indent on newline
    dedent_triggers: List[
        str
    ] = []  # Keywords that trigger dedent (e.g., "return", "break")
    indent_size: int = 4  # Number of spaces per indent level

    @classmethod
    def get_tree_sitter_language(cls):
        """Get the tree-sitter language object."""
        if cls.tree_sitter_module is None:
            return None
        try:
            import importlib

            module = importlib.import_module(cls.tree_sitter_module)
            return module.language()
        except ImportError:
            return None

    @classmethod
    def should_increase_indent(cls, line: str) -> bool:
        """Check if line should trigger increased indentation on next line."""
        stripped = line.rstrip()
        if not stripped:
            return False
        for trigger in cls.indent_triggers:
            if stripped.endswith(trigger):
                return True
        return False

    @classmethod
    def get_line_indent(cls, line: str) -> str:
        """Get the leading whitespace from a line."""
        return line[: len(line) - len(line.lstrip())]
