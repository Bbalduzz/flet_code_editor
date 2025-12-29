# Flet Code Editor

A syntax-highlighting code editor component for [Flet](https://flet.dev) (v0.28.x).

## Features

- Python syntax highlighting (tree-sitter with regex fallback)
- 6 built-in themes (GitHub Dark, Monokai, Dracula, Solarized Dark, One Dark, Ayu Dark)
- Cursor navigation and text selection
- Undo/redo support
- Customizable fonts, colors, and display options

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

## Configuration

```python
from flet_code_editor import CodeEditorConfig, Theme

config = CodeEditorConfig(
    theme=Theme(),           # Color theme
    font_family="Consolas",  # Font family
    font_size=14,            # Font size in pixels
    line_height_px=20,       # Line height in pixels
    show_line_numbers=True,  # Show line number gutter
    show_spaces=False,       # Show space characters as dots
    show_tabs=False,         # Show tab characters as arrows
)
```

## API

```python
editor = CodeEditor(text="", config=None)

# Methods
editor.get_text()              # Get editor content
editor.set_text("new content") # Set editor content
editor.update_config(config)   # Update configuration
editor.handle_keyboard_event   # Set as page.on_keyboard_event
```

## Run Demo

```bash
cd flet_code_editor
python demo.py
```
