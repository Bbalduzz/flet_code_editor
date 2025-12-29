"""Main editor component with input handling."""

import threading
from typing import Callable

import flet as ft

from .config import CodeEditorConfig
from .document import Document
from .highlighter import Highlighter
from .operations import OpCode
from .view import View


class InputListener(ft.Stack):
    """Handles keyboard input for the editor."""

    def __init__(self, child: ft.Control, document: Document, on_change: Callable):
        super().__init__()
        self.child_control = child
        self.document = document
        self.on_change_callback = on_change
        self.proxy_input = ft.TextField(
            width=0,
            height=0,
            opacity=0,
            multiline=True,
            on_submit=self._handle_submit,
            on_change=self._handle_text_input,
        )
        self.controls = [self.child_control, self.proxy_input]

        # Key repeat state
        self.key_repeat_active = False
        self.key_repeat_timer = None
        self.current_key = None
        self.current_modifiers = {}

    def _handle_text_input(self, e):
        """Handle text input from the proxy TextField."""
        val = self.proxy_input.value
        if val:
            self.document.execute_operation(OpCode.INSERT_CHAR, char=val)
            self.proxy_input.value = ""
            self.proxy_input.update()
            self.on_change_callback()
            self.proxy_input.focus()

    def _handle_submit(self, e):
        """Handle Enter key press."""
        self.document.execute_operation(OpCode.NEWLINE)
        self.proxy_input.value = ""
        self.proxy_input.focus()
        self.on_change_callback()

    def _execute_key_operation(
        self, key: str, shift: bool = False, ctrl: bool = False, meta: bool = False
    ):
        """Execute the operation for a given key."""
        if key == "Arrow Left":
            self.document.execute_operation(OpCode.MOVE_CURSOR_LEFT, keep_anchor=shift)
        elif key == "Arrow Right":
            self.document.execute_operation(OpCode.MOVE_CURSOR_RIGHT, keep_anchor=shift)
        elif key == "Arrow Up":
            self.document.execute_operation(OpCode.MOVE_CURSOR_UP, keep_anchor=shift)
        elif key == "Arrow Down":
            self.document.execute_operation(OpCode.MOVE_CURSOR_DOWN, keep_anchor=shift)
        elif key == "Backspace":
            self.document.execute_operation(OpCode.BACKSPACE)
        elif key == "Delete":
            self.document.execute_operation(OpCode.DELETE_CHAR)
        elif key == "Tab":
            self.document.execute_operation(OpCode.TAB)
        elif (meta or ctrl) and len(key) == 1:
            k = key.lower()
            if k == "a":
                self.document.execute_operation(OpCode.SELECT_ALL)
            elif k == "c":
                self.document.execute_operation(OpCode.COPY)
            elif k == "v":
                self.document.execute_operation(OpCode.PASTE)
            elif k == "x":
                self.document.execute_operation(OpCode.CUT)
            elif k == "z":
                self.document.execute_operation(OpCode.UNDO)
            elif k == "y":
                self.document.execute_operation(OpCode.REDO)

        self.on_change_callback()

    def start_key_repeat(
        self, key: str, shift: bool = False, ctrl: bool = False, meta: bool = False
    ):
        """Start repeating a key operation."""
        self.proxy_input.focus()

        if self.key_repeat_timer:
            self.key_repeat_timer.cancel()

        self.current_key = key
        self.current_modifiers = {"shift": shift, "ctrl": ctrl, "meta": meta}
        self.key_repeat_active = True

        self._execute_key_operation(key, shift, ctrl, meta)

        def repeat():
            if self.key_repeat_active:
                self._execute_key_operation(
                    self.current_key,
                    self.current_modifiers["shift"],
                    self.current_modifiers["ctrl"],
                    self.current_modifiers["meta"],
                )
                self.key_repeat_timer = threading.Timer(0.05, repeat)
                self.key_repeat_timer.start()

        self.key_repeat_timer = threading.Timer(0.5, repeat)
        self.key_repeat_timer.start()

    def stop_key_repeat(self):
        """Stop key repeat."""
        self.key_repeat_active = False
        if self.key_repeat_timer:
            self.key_repeat_timer.cancel()
            self.key_repeat_timer = None
        self.current_key = None
        self.current_modifiers = {}


class CodeEditor(ft.Container):
    """Main code editor component."""

    REPEATABLE_KEYS = [
        "Arrow Left",
        "Arrow Right",
        "Arrow Up",
        "Arrow Down",
        "Backspace",
        "Delete",
    ]

    def __init__(self, text: str = "", config: CodeEditorConfig = None):
        super().__init__()
        self.config = config or CodeEditorConfig()
        self.document = Document()
        self.document.lines = text.split("\n")
        self.highlighter = Highlighter(self.config)
        self.view = View(self.document, self.highlighter, self.config)
        self.input_listener = InputListener(
            self.view, self.document, self.on_document_change
        )
        self.content = self.input_listener
        self.expand = True
        self.on_click = self._on_click

        # Keyboard state
        self._key_release_timer = None
        self._last_key_combo = None

    def _on_click(self, e):
        """Handle click - focus the editor."""
        self.input_listener.proxy_input.focus()

    def will_unmount(self):
        """Called when the control is removed from the page."""
        self.input_listener.stop_key_repeat()
        if self._key_release_timer:
            self._key_release_timer.cancel()

    def handle_keyboard_event(self, e: ft.KeyboardEvent):
        """Handle global keyboard events. Set this as page.on_keyboard_event."""
        if e.key in self.REPEATABLE_KEYS or e.meta or e.ctrl:
            key_combo = f"{e.key}_{e.shift}_{e.ctrl}_{e.meta}"

            if key_combo == self._last_key_combo:
                if self._key_release_timer:
                    self._key_release_timer.cancel()
            else:
                if self._last_key_combo:
                    self.input_listener.stop_key_repeat()

            if e.key in self.REPEATABLE_KEYS:
                self.input_listener.start_key_repeat(e.key, e.shift, e.ctrl, e.meta)
            else:
                self.input_listener._execute_key_operation(
                    e.key, e.shift, e.ctrl, e.meta
                )

            self._last_key_combo = key_combo

            if self._key_release_timer:
                self._key_release_timer.cancel()

            def on_key_released():
                self.input_listener.stop_key_repeat()
                self._last_key_combo = None

            self._key_release_timer = threading.Timer(0.2, on_key_released)
            self._key_release_timer.start()

    def on_document_change(self):
        """Called when the document content changes."""
        self.view.render()

    def update_config(self, new_config: CodeEditorConfig):
        """Update the editor configuration."""
        self.config = new_config
        self.highlighter = Highlighter(self.config)
        self.view.config = self.config
        self.view.item_extent = self.config.line_height_px
        self.view.highlighter = self.highlighter
        self.view.render()

    def get_text(self) -> str:
        """Get the full text content of the editor."""
        return self.document.get_full_text()

    def set_text(self, text: str):
        """Set the text content of the editor."""
        self.document.lines = text.split("\n")
        self.document.cursor.line = 0
        self.document.cursor.column = 0
        self.document.cursor.anchor_line = 0
        self.document.cursor.anchor_column = 0
        self.view.render()
