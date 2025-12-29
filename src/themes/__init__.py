"""Pre-built color themes for the code editor."""

from ..config import Theme


class CodeEditorTheme:
    """Pre-built editor themes with IDE autocompletion support."""

    GITHUB_DARK: Theme
    MONOKAI: Theme
    DRACULA: Theme
    SOLARIZED_DARK: Theme
    ONE_DARK: Theme
    AYU_DARK: Theme
    RUST_DARK: Theme


# Theme definitions

GITHUB_DARK = Theme(
    name="GitHub Dark",
    editor_bg="#0D1117",
    editor_fg="#c9d1d9",
    line_number_fg="#484f58",
    line_number_bg="#0D1117",
    selection_bg="#264f78",
    cursor_bg="#c9d1d9",
    cursor_fg="#0D1117",
    invisible_fg="#30363d",
    keyword="#ff7b72",
    function="#d2a8ff",
    string="#a5d6ff",
    comment="#8b949e",
    class_name="#79c0ff",
    number="#79c0ff",
    docstring="#a5d6ff",
    decorator="#d2a8ff",
    instance="#ffa657",
    builtin="#79c0ff",
    exception="#f85149",
    function_call="#d2a8ff",
)

MONOKAI = Theme(
    name="Monokai",
    editor_bg="#272822",
    editor_fg="#f8f8f2",
    line_number_fg="#90908a",
    line_number_bg="#272822",
    selection_bg="#49483e",
    cursor_bg="#f8f8f0",
    cursor_fg="#272822",
    invisible_fg="#3b3a32",
    keyword="#f92672",
    function="#a6e22e",
    string="#e6db74",
    comment="#75715e",
    class_name="#66d9ef",
    number="#ae81ff",
    docstring="#e6db74",
    decorator="#a6e22e",
    instance="#fd971f",
    builtin="#66d9ef",
    exception="#f92672",
    function_call="#a6e22e",
)

DRACULA = Theme(
    name="Dracula",
    editor_bg="#282a36",
    editor_fg="#f8f8f2",
    line_number_fg="#6272a4",
    line_number_bg="#282a36",
    selection_bg="#44475a",
    cursor_bg="#f8f8f2",
    cursor_fg="#282a36",
    invisible_fg="#44475a",
    keyword="#ff79c6",
    function="#50fa7b",
    string="#f1fa8c",
    comment="#6272a4",
    class_name="#8be9fd",
    number="#bd93f9",
    docstring="#f1fa8c",
    decorator="#50fa7b",
    instance="#ffb86c",
    builtin="#8be9fd",
    exception="#ff5555",
    function_call="#50fa7b",
)

SOLARIZED_DARK = Theme(
    name="Solarized Dark",
    editor_bg="#002b36",
    editor_fg="#839496",
    line_number_fg="#586e75",
    line_number_bg="#002b36",
    selection_bg="#073642",
    cursor_bg="#839496",
    cursor_fg="#002b36",
    invisible_fg="#073642",
    keyword="#859900",
    function="#268bd2",
    string="#2aa198",
    comment="#586e75",
    class_name="#b58900",
    number="#d33682",
    docstring="#2aa198",
    decorator="#6c71c4",
    instance="#cb4b16",
    builtin="#b58900",
    exception="#dc322f",
    function_call="#268bd2",
)

ONE_DARK = Theme(
    name="One Dark",
    editor_bg="#282c34",
    editor_fg="#abb2bf",
    line_number_fg="#4b5263",
    line_number_bg="#282c34",
    selection_bg="#3e4451",
    cursor_bg="#528bff",
    cursor_fg="#282c34",
    invisible_fg="#3b4048",
    keyword="#c678dd",
    function="#61afef",
    string="#98c379",
    comment="#5c6370",
    class_name="#e5c07b",
    number="#d19a66",
    docstring="#98c379",
    decorator="#c678dd",
    instance="#e06c75",
    builtin="#e5c07b",
    exception="#e06c75",
    function_call="#61afef",
)

AYU_DARK = Theme(
    name="Ayu Dark",
    editor_bg="#0b0e14",
    editor_fg="#bfbdb6",
    line_number_fg="#6c7380",
    line_number_bg="#0b0e14",
    selection_bg="#409fff44",
    cursor_bg="#e6b450",
    cursor_fg="#0b0e14",
    invisible_fg="#6c7380",
    keyword="#ff8f40",
    function="#ffb454",
    string="#aad94c",
    comment="#acb6bf8c",
    class_name="#59c2ff",
    number="#d2a6ff",
    docstring="#aad94c",
    decorator="#e6b673",
    instance="#f29668",
    builtin="#59c2ff",
    exception="#d95757",
    function_call="#ffb454",
)

RUST_DARK = Theme(
    name="Rust Dark",
    editor_bg="#282c34",  # Dark blue-gray background
    editor_fg="#abb2bf",  # Light gray default text
    line_number_fg="#5c6370",
    line_number_bg="#282c34",
    selection_bg="#3e4451",
    cursor_bg="#528bff",
    cursor_fg="#282c34",
    invisible_fg="#3b4048",
    keyword="#c678dd",  # Purple - for 'impl', 'where', 'fn', 'if', 'match', 'let', 'return'
    function="#61afef",  # Blue - for function names like 'next', 'size_hint'
    string="#98c379",  # Green - for strings like "rust1", "1.0.0"
    comment="#5c6370",  # Gray - for comments
    class_name="#e5c07b",  # Yellow/gold - for types like 'Iterator', 'Split', 'Option'
    number="#d19a66",  # Orange - for numbers like 0, 1
    docstring="#98c379",  # Green
    decorator="#e5c07b",  # Yellow/gold - for attributes like #[stable], #[inline]
    instance="#e06c75",  # Red/pink - for 'self'
    builtin="#56b6c2",  # Cyan - for 'None', 'Some', 'true', 'bool'
    exception="#e06c75",  # Red
    function_call="#61afef",  # Blue - for method calls like .iter(), .position()
)

# Assign to CodeEditorTheme class for better API
CodeEditorTheme.GITHUB_DARK = GITHUB_DARK
CodeEditorTheme.MONOKAI = MONOKAI
CodeEditorTheme.DRACULA = DRACULA
CodeEditorTheme.SOLARIZED_DARK = SOLARIZED_DARK
CodeEditorTheme.ONE_DARK = ONE_DARK
CodeEditorTheme.AYU_DARK = AYU_DARK
CodeEditorTheme.RUST_DARK = RUST_DARK

ALL_THEMES = {
    "github_dark": GITHUB_DARK,
    "monokai": MONOKAI,
    "dracula": DRACULA,
    "solarized_dark": SOLARIZED_DARK,
    "one_dark": ONE_DARK,
    "ayu_dark": AYU_DARK,
    "rust_dark": RUST_DARK,
}


def get_theme(name: str) -> Theme:
    """Get a theme by name.

    Args:
        name: Theme name (github_dark, monokai, dracula, solarized_dark, one_dark)

    Returns:
        Theme instance, or GitHub Dark if name not found
    """
    return ALL_THEMES.get(name.lower().replace(" ", "_").replace("-", "_"), GITHUB_DARK)


def list_themes() -> list[str]:
    """Return a list of available theme names."""
    return list(ALL_THEMES.keys())
