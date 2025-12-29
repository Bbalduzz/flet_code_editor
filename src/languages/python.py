"""Python language definition for syntax highlighting."""

from .base import Language


class Python(Language):
    """Python language syntax highlighting."""

    name = "python"
    tree_sitter_module = "tree_sitter_python"

    tree_sitter_query = """
(comment) @comment
(string) @string
(escape_sequence) @string.escape
(class_definition name: (identifier) @type)
(function_definition name: (identifier) @function)
(call function: (identifier) @function.call)
(call function: (attribute attribute: (identifier) @function.call))
(decorator) @decorator
(
  [
    "def" "class" "if" "else" "elif" "return" "try" "except" "import" "from"
    "while" "for" "in" "and" "or" "not" "is" "as" "with" "lambda" "pass"
    "break" "continue" "global" "nonlocal" "raise" "yield" "await" "async"
    "assert" "del" "print" "exec"
  ] @keyword
)
(true) @constant.builtin
(false) @constant.builtin
(none) @constant.builtin
(integer) @number
(float) @number
(identifier) @variable
(attribute attribute: (identifier) @property)
"""

    regex_patterns = [
        (r"#[^\n]*", "comment"),
        (r"(?:r|u|f)?'[^'\\\n]*(?:\\.[^'\\\n]*)*'?", "string"),
        (r'(?:r|u|f)?"[^"\\\n]*(?:\\.[^"\\\n]*)*"?', "string"),
        (r"\b(?:def|class|if|else|elif|return|import|from|while|for|in|and|or|not|is|as|with|lambda|pass|break|continue|try|except|raise|yield|await|async)\b", "keyword"),
        (r"\b\d+\.?\d*\b", "number"),
        (r"\b(?:True|False|None)\b", "constant.builtin"),
        (r"\bself\b", "instance"),
        (r"\bcls\b", "instance"),
    ]
