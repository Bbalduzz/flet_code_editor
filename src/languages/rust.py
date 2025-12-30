"""Rust language definition for syntax highlighting."""

from .base import Language


class Rust(Language):
    """Rust language syntax highlighting."""

    name = "rust"
    tree_sitter_module = "tree_sitter_rust"

    # Rust uses braces for blocks
    indent_triggers = ["{", "(", "["]
    indent_size = 4

    tree_sitter_query = """
; Match the impl block with attribute
(attribute_item
  (attribute
    (identifier) @attr_name
    (token_tree) @attr_args))

(impl_item
  (type_parameters
    (lifetime (identifier) @lifetime)
    (type_identifier) @type_param) @type_params
  (type_identifier) @trait_name
  (generic_type
    (type_identifier) @impl_type
    (type_arguments
      (lifetime (identifier) @impl_lifetime)
      (type_identifier) @impl_type_arg)*) @generic_type
  (where_clause
    (where_predicate
      (type_identifier) @where_type
      (trait_bounds
        (function_type
          (parameters
            (reference_type
              (type_identifier) @fn_param_type))
          (primitive_type) @fn_return_type)))) @where_clause
  (declaration_list
    (associated_type
      (type_identifier) @assoc_type_name
      (reference_type
        (lifetime (identifier) @assoc_lifetime)
        (array_type
          (type_identifier) @array_type))) @associated_type
    (function_item
      (attribute_item
        (attribute (identifier) @fn_attr))
      (identifier) @fn_name
      (parameters
        (self_parameter (self) @self_param))
      (generic_type
        (type_identifier) @return_type) @fn_return
      (block) @fn_body)*))
"""

    regex_patterns = [
        (r"//[^\n]*", "comment"),
        (r"/\*[\s\S]*?\*/", "comment"),
        (r'"[^"\\]*(?:\\.[^"\\]*)*"', "string"),
        (r"'[^'\\]*(?:\\.[^'\\]*)*'", "string"),
        (r"r#*\"[\s\S]*?\"#*", "string"),
        (
            r"\b(?:fn|let|mut|const|static|if|else|match|loop|while|for|in|return|break|continue|pub|mod|use|struct|enum|impl|trait|type|where|as|ref|self|Self|async|await|move|dyn|unsafe|extern|crate|super)\b",
            "keyword",
        ),
        (
            r"\b(?:i8|i16|i32|i64|i128|isize|u8|u16|u32|u64|u128|usize|f32|f64|bool|char|str|String|Vec|Option|Result)\b",
            "type",
        ),
        (r"\b(?:true|false|None|Some|Ok|Err)\b", "constant.builtin"),
        (r"\b\d+\.?\d*(?:e[+-]?\d+)?(?:f32|f64|i32|i64|u32|u64)?\b", "number"),
        (r"\bself\b", "instance"),
    ]
