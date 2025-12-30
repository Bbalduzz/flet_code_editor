"""Document model for the code editor."""

from typing import List, Optional, Type

from .operations import Cursor, OpCode, Operation


class Document:
    """Manages the text content, cursor, and operations for the editor."""

    def __init__(self, language: Optional[Type] = None):
        self.lines: List[str] = [""]
        self.cursor = Cursor()
        self.undo_stack: List[Operation] = []
        self.redo_stack: List[Operation] = []
        self.version = 0
        self._language = language  # For smart indentation

    def set_language(self, language: Optional[Type]):
        """Set the language for smart indentation."""
        self._language = language

    def _compute_smart_indent(self) -> str:
        """Compute the indentation for a new line based on the current line."""
        if self.cursor.line >= len(self.lines):
            return ""

        current_line = self.lines[self.cursor.line]
        # Get text before cursor (we indent based on what's before the cursor)
        text_before_cursor = current_line[: self.cursor.column]

        # Get current indentation
        base_indent = ""
        for ch in text_before_cursor:
            if ch in " \t":
                base_indent += ch
            else:
                break

        # Check if we should add extra indentation
        if self._language is not None:
            if self._language.should_increase_indent(text_before_cursor):
                # Add one level of indentation
                base_indent += " " * self._language.indent_size
        else:
            # Default behavior: indent after : { ( [
            stripped = text_before_cursor.rstrip()
            if stripped and stripped[-1] in ":({[":
                base_indent += "    "

        return base_indent

    def get_full_text(self) -> str:
        """Return the full document text."""
        return "\n".join(self.lines)

    def _validate_cursor(self, keep_anchor: bool):
        """Ensure cursor position is within valid bounds."""
        self.cursor.line = max(0, min(self.cursor.line, len(self.lines) - 1))
        self.cursor.column = max(
            0, min(self.cursor.column, len(self.lines[self.cursor.line]))
        )
        if keep_anchor:
            self.cursor.anchor_line = max(
                0, min(self.cursor.anchor_line, len(self.lines) - 1)
            )
            self.cursor.anchor_column = max(
                0,
                min(
                    self.cursor.anchor_column, len(self.lines[self.cursor.anchor_line])
                ),
            )
        else:
            self.cursor.anchor_line = self.cursor.line
            self.cursor.anchor_column = self.cursor.column

    def move_cursor_left(self, count: int = 1, keep_anchor: bool = False):
        """Move cursor left by count characters."""
        self.cursor.column -= count
        if self.cursor.column < 0:
            self.cursor.line -= 1
            if self.cursor.line < 0:
                self.cursor.line = 0
            self.cursor.column = len(self.lines[self.cursor.line])
        self._validate_cursor(keep_anchor)

    def move_cursor_right(self, count: int = 1, keep_anchor: bool = False):
        """Move cursor right by count characters."""
        self.cursor.column += count
        if self.cursor.column > len(self.lines[self.cursor.line]):
            self.cursor.line += 1
            if self.cursor.line >= len(self.lines):
                self.cursor.line = len(self.lines) - 1
                self.cursor.column = len(self.lines[self.cursor.line])
            else:
                self.cursor.column = 0
        self._validate_cursor(keep_anchor)

    def move_cursor_up(self, count: int = 1, keep_anchor: bool = False):
        """Move cursor up by count lines."""
        self.cursor.line -= count
        self._validate_cursor(keep_anchor)

    def move_cursor_down(self, count: int = 1, keep_anchor: bool = False):
        """Move cursor down by count lines."""
        self.cursor.line += count
        self._validate_cursor(keep_anchor)

    def insert_text(self, text: str):
        """Insert text at the current cursor position."""
        self.version += 1
        self.delete_selected_text()
        line = self.lines[self.cursor.line]
        left = line[: self.cursor.column]
        right = line[self.cursor.column :]

        parts = text.split("\n")
        self.lines[self.cursor.line] = (
            left + parts[0] + (right if len(parts) == 1 else "")
        )
        self.cursor.column += len(parts[0])

        if len(parts) > 1:
            for i in range(1, len(parts)):
                content = parts[i] + (right if i == len(parts) - 1 else "")
                self.lines.insert(self.cursor.line + i, content)
            self.cursor.line += len(parts) - 1
            self.cursor.column = len(parts[-1])

        self._validate_cursor(False)

    def delete_text(self):
        """Delete the character at the current cursor position."""
        self.version += 1
        line = self.lines[self.cursor.line]
        if self.cursor.column >= len(line):
            if self.cursor.line + 1 < len(self.lines):
                self.lines[self.cursor.line] += self.lines[self.cursor.line + 1]
                self.lines.pop(self.cursor.line + 1)
        else:
            self.lines[self.cursor.line] = (
                line[: self.cursor.column] + line[self.cursor.column + 1 :]
            )

    def delete_selected_text(self):
        """Delete the currently selected text."""
        self._validate_cursor(True)
        if not self.cursor.has_selection():
            return
        self.version += 1
        cur = self.cursor.normalized()

        if cur.line == cur.anchor_line:
            line = self.lines[cur.line]
            self.lines[cur.line] = line[: cur.column] + line[cur.anchor_column :]
        else:
            self.lines[cur.line] = (
                self.lines[cur.line][: cur.column]
                + self.lines[cur.anchor_line][cur.anchor_column :]
            )
            del self.lines[cur.line + 1 : cur.anchor_line + 1]

        self.cursor.line = cur.line
        self.cursor.column = cur.column
        self._validate_cursor(False)

    def get_char_before_cursor(self) -> str:
        """Get the character before the cursor."""
        self._validate_cursor(False)
        if self.cursor.column > 0:
            return self.lines[self.cursor.line][self.cursor.column - 1]
        elif self.cursor.line > 0:
            return "\n"
        return ""

    def get_text_at_cursor(self) -> str:
        """Get the character at the cursor position."""
        self._validate_cursor(False)
        line = self.lines[self.cursor.line]
        if self.cursor.column >= len(line):
            return "\n"
        return line[self.cursor.column]

    def get_selected_text_content(self) -> str:
        """Get the currently selected text."""
        self._validate_cursor(True)
        if not self.cursor.has_selection():
            return ""
        cur = self.cursor.normalized()
        res = []
        if cur.line == cur.anchor_line:
            return self.lines[cur.line][cur.column : cur.anchor_column]
        res.append(self.lines[cur.line][cur.column :])
        for i in range(cur.line + 1, cur.anchor_line):
            res.append(self.lines[i])
        res.append(self.lines[cur.anchor_line][: cur.anchor_column])
        return "\n".join(res)

    def execute_operation(self, opcode: OpCode, **kwargs) -> bool:
        """Execute an editor operation."""
        record_undo = kwargs.get("record_undo", True)
        op_obj = None
        self._validate_cursor(True)
        prev_cursor = self.cursor.copy()

        if opcode == OpCode.INSERT_CHAR:
            char = kwargs.get("char", "")
            if record_undo:
                op_obj = Operation(
                    OpCode.INSERT_CHAR,
                    prev_cursor.line,
                    prev_cursor.column,
                    text=char,
                    prev_cursor=prev_cursor,
                )
            self.insert_text(char)

        elif opcode == OpCode.NEWLINE:
            # Compute smart indentation before inserting newline
            smart_indent = self._compute_smart_indent()
            newline_text = "\n" + smart_indent
            if record_undo:
                op_obj = Operation(
                    OpCode.NEWLINE,
                    prev_cursor.line,
                    prev_cursor.column,
                    text=newline_text,
                    prev_cursor=prev_cursor,
                )
            self.insert_text(newline_text)

        elif opcode == OpCode.BACKSPACE:
            if self.cursor.has_selection():
                return self.execute_operation(
                    OpCode.DELETE_CHAR, record_undo=record_undo
                )
            deleted_char = self.get_char_before_cursor()
            if not deleted_char:
                return False
            if record_undo:
                op_obj = Operation(
                    OpCode.BACKSPACE,
                    prev_cursor.line,
                    prev_cursor.column,
                    text=deleted_char,
                    prev_cursor=prev_cursor,
                )
            if self.cursor.column > 0:
                self.move_cursor_left()
                self.delete_text()
            elif self.cursor.line > 0:
                self.move_cursor_left()
                self.delete_text()

        elif opcode == OpCode.DELETE_CHAR:
            if self.cursor.has_selection():
                deleted_text = self.get_selected_text_content()
                if record_undo:
                    op_obj = Operation(
                        OpCode.DELETE_CHAR,
                        prev_cursor.line,
                        prev_cursor.column,
                        text=deleted_text,
                        prev_cursor=prev_cursor,
                    )
                self.delete_selected_text()
            else:
                deleted_char = self.get_text_at_cursor()
                if record_undo:
                    op_obj = Operation(
                        OpCode.DELETE_CHAR,
                        prev_cursor.line,
                        prev_cursor.column,
                        text=deleted_char,
                        prev_cursor=prev_cursor,
                    )
                self.delete_text()

        elif opcode == OpCode.UNDO:
            if not self.undo_stack:
                return False
            op = self.undo_stack.pop()
            inverse = op.inverse()
            if inverse.opcode == OpCode.INSERT_CHAR:
                self.cursor.line = min(inverse.line, len(self.lines) - 1)
                self.cursor.column = min(inverse.col, len(self.lines[self.cursor.line]))
                self.cursor.anchor_line = self.cursor.line
                self.cursor.anchor_column = self.cursor.column
                self.insert_text(inverse.text)
                if (
                    op.opcode == OpCode.DELETE_CHAR
                    and op.prev_cursor
                    and op.prev_cursor.has_selection()
                ):
                    self.cursor = op.prev_cursor.copy()
            elif inverse.opcode == OpCode.DELETE_CHAR:
                self.cursor.line = inverse.line
                self.cursor.column = inverse.col
                lines = inverse.text.split("\n")
                if len(lines) == 1:
                    self.cursor.anchor_line = inverse.line
                    self.cursor.anchor_column = inverse.col + len(lines[0])
                else:
                    self.cursor.anchor_line = inverse.line + len(lines) - 1
                    self.cursor.anchor_column = len(lines[-1])
                self.delete_selected_text()
                if op.prev_cursor:
                    self.cursor = op.prev_cursor.copy()
            self.redo_stack.append(op)
            self._validate_cursor(False)
            return True

        elif opcode == OpCode.REDO:
            if not self.redo_stack:
                return False
            op = self.redo_stack.pop()
            if op.prev_cursor:
                self.cursor = op.prev_cursor.copy()
            self.execute_operation(op.opcode, char=op.text, record_undo=True)
            return True

        elif opcode == OpCode.MOVE_CURSOR_LEFT:
            self.move_cursor_left(keep_anchor=kwargs.get("keep_anchor", False))
        elif opcode == OpCode.MOVE_CURSOR_RIGHT:
            self.move_cursor_right(keep_anchor=kwargs.get("keep_anchor", False))
        elif opcode == OpCode.MOVE_CURSOR_UP:
            self.move_cursor_up(keep_anchor=kwargs.get("keep_anchor", False))
        elif opcode == OpCode.MOVE_CURSOR_DOWN:
            self.move_cursor_down(keep_anchor=kwargs.get("keep_anchor", False))
        elif opcode == OpCode.TAB:
            self.insert_text("    ")
        elif opcode == OpCode.SELECT_ALL:
            self.cursor.line = 0
            self.cursor.column = 0
            self.cursor.anchor_line = len(self.lines) - 1
            self.cursor.anchor_column = len(self.lines[-1])

        if record_undo and op_obj:
            self.undo_stack.append(op_obj)
            self.redo_stack.clear()

        return True
