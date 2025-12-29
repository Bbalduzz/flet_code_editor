"""Operation codes, operations, and cursor management for the editor."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class OpCode(Enum):
    """Operation codes for editor actions."""

    INSERT_CHAR = "insert_char"
    DELETE_CHAR = "delete_char"
    BACKSPACE = "backspace"
    NEWLINE = "newline"
    MOVE_CURSOR_LEFT = "move_left"
    MOVE_CURSOR_RIGHT = "move_right"
    MOVE_CURSOR_UP = "move_up"
    MOVE_CURSOR_DOWN = "move_down"
    MOVE_LINE_START = "move_line_start"
    MOVE_LINE_END = "move_line_end"
    MOVE_DOC_START = "move_doc_start"
    MOVE_DOC_END = "move_doc_end"
    DELETE_LINE = "delete_line"
    SELECT_ALL = "select_all"
    COPY = "copy"
    CUT = "cut"
    PASTE = "paste"
    UNDO = "undo"
    REDO = "redo"
    TAB = "tab"


@dataclass
class Cursor:
    """Represents the cursor position and selection anchor."""

    line: int = 0
    column: int = 0
    anchor_line: int = 0
    anchor_column: int = 0

    def copy(self) -> Cursor:
        """Create a copy of this cursor."""
        return Cursor(self.line, self.column, self.anchor_line, self.anchor_column)

    def normalized(self) -> Cursor:
        """Return a cursor with start before end (for selection handling)."""
        res = self.copy()
        if self.line > self.anchor_line or (
            self.line == self.anchor_line and self.column > self.anchor_column
        ):
            res.line, res.column = self.anchor_line, self.anchor_column
            res.anchor_line, res.anchor_column = self.line, self.column
        return res

    def has_selection(self) -> bool:
        """Check if there is an active selection."""
        return self.line != self.anchor_line or self.column != self.anchor_column


@dataclass
class Operation:
    """Represents an editor operation for undo/redo support."""

    opcode: OpCode
    line: int
    col: int
    text: str = ""
    prev_text: str = ""
    prev_cursor: Optional[Cursor] = None

    def inverse(self) -> Operation:
        """Return the inverse operation for undo support."""
        if self.opcode == OpCode.INSERT_CHAR:
            return Operation(
                OpCode.DELETE_CHAR,
                self.line,
                self.col,
                self.text,
                self.prev_text,
                self.prev_cursor,
            )
        elif self.opcode == OpCode.DELETE_CHAR:
            return Operation(
                OpCode.INSERT_CHAR,
                self.line,
                self.col,
                self.text,
                self.prev_text,
                self.prev_cursor,
            )
        elif self.opcode == OpCode.BACKSPACE:
            return Operation(
                OpCode.INSERT_CHAR,
                self.line,
                self.col - len(self.text),
                self.text,
                self.prev_text,
                self.prev_cursor,
            )
        elif self.opcode == OpCode.NEWLINE:
            return Operation(
                OpCode.DELETE_CHAR,
                self.line,
                self.col,
                "\n",
                self.prev_text,
                self.prev_cursor,
            )
        return self
