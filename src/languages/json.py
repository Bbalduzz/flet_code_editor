"""JSON language definition for syntax highlighting."""

from .base import Language


class JSON(Language):
    """JSON language syntax highlighting."""

    name = "json"
    tree_sitter_module = "tree_sitter_json"

    tree_sitter_query = """
(string) @string
(number) @number
(true) @constant.builtin
(false) @constant.builtin
(null) @constant.builtin
(pair key: (string) @property)
"""

    regex_patterns = [
        (r'"(?:[^"\\]|\\.)*"', "string"),
        (r"-?\b\d+(?:\.\d+)?(?:[eE][+-]?\d+)?\b", "number"),
        (r"\b(?:true|false)\b", "constant.builtin"),
        (r"\bnull\b", "constant.builtin"),
    ]

    # JSON doesn't have traditional indent triggers, but braces/brackets start blocks
    indent_triggers = ["{", "["]
    indent_size = 2
