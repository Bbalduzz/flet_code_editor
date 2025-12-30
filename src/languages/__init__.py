"""Language definitions for syntax highlighting."""

from .base import Language
from .json import JSON
from .python import Python
from .rust import Rust

__all__ = ["Language", "JSON", "Python", "Rust"]
