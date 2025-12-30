# Flet Code Editor
A syntax-highlighting code editor component for [Flet](https://flet.dev) (v0.28.3).

<img width="3006" height="1580" alt="demo" src="https://github.com/user-attachments/assets/cb89e0b4-c0ff-43b3-b862-75c56e4a91b2" />

## Features

- Python syntax highlighting (tree-sitter with regex fallback)
- 6 built-in themes (GitHub Dark, Monokai, Dracula, Solarized Dark, One Dark, Ayu Dark)
- Cursor navigation and text selection
- Undo/redo support
- Smart indentation (auto-indent after `:`, `{`, etc.)
- Search & Replace with regex support
- Customizable fonts, colors, and display options
- Extensible language support

## Installation

```bash
pip install flet tree-sitter tree-sitter-python
```

## Usage

```python
import flet as ft
from flet_code_editor import CodeEditor, CodeEditorConfig, CodeEditorTheme

def main(page: ft.Page):
    config = CodeEditorConfig(theme=CodeEditorTheme.AYU_DARK)
    editor = CodeEditor("# Your code here", config)

    page.on_keyboard_event = editor.handle_keyboard_event
    page.add(editor)

ft.app(target=main)
```

## Themes

```python
from flet_code_editor import CodeEditorConfig, CodeEditorTheme

# Available themes (with IDE autocompletion)
CodeEditorTheme.GITHUB_DARK
CodeEditorTheme.MONOKAI
CodeEditorTheme.DRACULA
CodeEditorTheme.SOLARIZED_DARK
CodeEditorTheme.ONE_DARK
CodeEditorTheme.AYU_DARK

# Use a theme
config = CodeEditorConfig(theme=CodeEditorTheme.DRACULA)
```

## Languages

```python
from flet_code_editor import CodeEditorConfig, Python, Language

# Use built-in Python language (default)
config = CodeEditorConfig(language=Python)

# Create a custom language
class MyLanguage(Language):
    name = "mylang"
    tree_sitter_module = "tree_sitter_mylang"  # Optional
    tree_sitter_query = """..."""              # Tree-sitter query
    regex_patterns = [                          # Fallback regex patterns
        (r"#[^\n]*", "comment"),
        (r'"[^"]*"', "string"),
        (r"\b(if|else|while)\b", "keyword"),
    ]

    # Smart indentation settings
    indent_triggers = [":"]      # Characters that trigger auto-indent
    dedent_triggers = []         # Keywords that trigger dedent
    indent_size = 4              # Spaces per indent level

config = CodeEditorConfig(language=MyLanguage)
```

See `src/languages/rust.py` for a complete example of implementing a custom language.

## Configuration

```python
from flet_code_editor import CodeEditorConfig, Theme, Python

config = CodeEditorConfig(
    theme=Theme(),           # Color theme
    language=Python,         # Language for highlighting
    font_family="Consolas",  # Font family
    font_size=14,            # Font size in pixels
    line_height_px=20,       # Line height in pixels
    show_line_numbers=True,  # Show line number gutter
    show_spaces=False,       # Show space characters as ·
    show_tabs=False,         # Show tab characters as →
    show_line_breaks=False,  # Show line breaks as ↵
)
```

## API

### Basic Operations

```python
editor = CodeEditor(text="", config=None)

# Methods
editor.get_text()              # Get editor content
editor.set_text("new content") # Set editor content
editor.update_config(config)   # Update configuration
editor.handle_keyboard_event   # Set as page.on_keyboard_event
```

### Search & Replace

```python
# Find all matches
count = editor.find(
    query="search term",
    regex=False,           # Enable regex patterns
    case_sensitive=False,  # Case-sensitive matching
    whole_word=False,      # Match whole words only
)

# Navigate between matches
editor.find_next()         # Go to next match
editor.find_previous()     # Go to previous match

# Replace
editor.replace_current("replacement")  # Replace current match
editor.replace_all("replacement")      # Replace all matches

# Clear search
editor.clear_search()

# Properties
editor.search_matches        # List[SearchMatch] - all matches
editor.search_match_count    # int - total match count
editor.current_search_index  # int - current match index (-1 if none)
```

### SearchMatch Object

```python
match = editor.search_matches[0]
match.line       # Line number (0-indexed)
match.start_col  # Start column
match.end_col    # End column
match.text       # Matched text
```

### Advanced Search Access

```python
# Access the Search object directly for advanced use
editor.search.is_regex
editor.search.is_case_sensitive
editor.search.is_whole_word
editor.search.query
editor.search.current_match
editor.search.refresh()  # Re-run search after external document changes
```

## Theme Customization

```python
from flet_code_editor import Theme

theme = Theme(
    # Editor UI colors
    editor_bg="#0D1117",
    editor_fg="#c9d1d9",
    line_number_fg="#484f58",
    line_number_bg="#0D1117",
    selection_bg="#264f78",
    cursor_bg="#c9d1d9",
    cursor_fg="#0D1117",
    invisible_fg="#30363d",
    search_match_bg="#613315",      # Background for search matches
    search_current_bg="#9e6a03",    # Background for current match

    # Syntax highlighting colors
    keyword="#ff7b72",
    function="#d2a8ff",
    string="#a5d6ff",
    comment="#8b949e",
    class_name="#79c0ff",
    number="#79c0ff",
    decorator="#d2a8ff",
    instance="#ffa657",
    # ... and more
)
```

## Run Demo

```bash
cd flet_code_editor
python demo.py
```

The demo includes a search bar with all search features and a settings panel to customize the editor.
