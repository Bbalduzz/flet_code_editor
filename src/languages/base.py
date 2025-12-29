"""Base language class for syntax highlighting."""

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional


class Language(ABC):
    """Abstract base class for language definitions."""

    name: str = "unknown"
    tree_sitter_module: Optional[str] = None
    tree_sitter_query: str = ""
    regex_patterns: List[Tuple[str, str]] = []  # List of (pattern, token_type)

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
