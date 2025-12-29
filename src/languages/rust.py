"""Rust language definition for syntax highlighting."""

from .base import Language


class Rust(Language):
    """Rust language syntax highlighting."""

    name = "rust"
    tree_sitter_module = "tree_sitter_rust"

    tree_sitter_query = """
(line_comment) @comment
(block_comment) @comment
(string_literal) @string
(char_literal) @string
(raw_string_literal) @string
(boolean_literal) @constant.builtin
(integer_literal) @number
(float_literal) @number
(type_identifier) @type
(primitive_type) @type
(function_item name: (identifier) @function)
(call_expression function: (identifier) @function.call)
(call_expression function: (field_expression field: (field_identifier) @function.call))
(macro_invocation macro: (identifier) @function.call)
(attribute_item) @decorator
(
  [
    "fn" "let" "mut" "const" "static" "if" "else" "match" "loop" "while"
    "for" "in" "return" "break" "continue" "pub" "mod" "use" "struct"
    "enum" "impl" "trait" "type" "where" "as" "ref" "self" "Self"
    "async" "await" "move" "dyn" "unsafe" "extern" "crate" "super"
  ] @keyword
)
(self) @instance
(identifier) @variable
(field_identifier) @property
"""

    regex_patterns = [
        (r"//[^\n]*", "comment"),
        (r"/\*[\s\S]*?\*/", "comment"),
        (r'"[^"\\]*(?:\\.[^"\\]*)*"', "string"),
        (r"'[^'\\]*(?:\\.[^'\\]*)*'", "string"),
        (r"r#*\"[\s\S]*?\"#*", "string"),
        (r"\b(?:fn|let|mut|const|static|if|else|match|loop|while|for|in|return|break|continue|pub|mod|use|struct|enum|impl|trait|type|where|as|ref|self|Self|async|await|move|dyn|unsafe|extern|crate|super)\b", "keyword"),
        (r"\b(?:i8|i16|i32|i64|i128|isize|u8|u16|u32|u64|u128|usize|f32|f64|bool|char|str|String|Vec|Option|Result)\b", "type"),
        (r"\b(?:true|false|None|Some|Ok|Err)\b", "constant.builtin"),
        (r"\b\d+\.?\d*(?:e[+-]?\d+)?(?:f32|f64|i32|i64|u32|u64)?\b", "number"),
        (r"\bself\b", "instance"),
    ]
