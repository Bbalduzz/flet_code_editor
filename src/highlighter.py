"""Syntax highlighting for the code editor."""

import re
import threading
from typing import List, Optional

import flet as ft

try:
    from tree_sitter import Language as TSLanguage, Parser, Query

    TREE_SITTER_AVAILABLE = True
except ImportError:
    TREE_SITTER_AVAILABLE = False

from .config import CodeEditorConfig
from .document import Document


class Highlighter:
    """Handles syntax highlighting using tree-sitter with regex fallback."""

    def __init__(self, config: CodeEditorConfig):
        self.config = config
        self.theme = config.theme
        self.language = config.language
        self.parser: Optional[Parser] = None
        self.query = None
        self.use_regex_fallback = False

        # State
        self.last_parsed_version = -1
        self.cached_captures = []
        self.line_byte_offsets = [0]

        # Debouncing Logic
        self._parse_timer = None
        self._lock = threading.Lock()

        # Try to initialize tree-sitter
        if TREE_SITTER_AVAILABLE and self.language:
            try:
                ts_lang = self.language.get_tree_sitter_language()
                if ts_lang is not None:
                    lang_obj = TSLanguage(ts_lang)
                    self.parser = Parser(lang_obj)
                    self.query = Query(lang_obj, self.language.tree_sitter_query)
                else:
                    self.use_regex_fallback = True
            except Exception as e:
                print(f"Tree-sitter init failed: {e}")
                self.use_regex_fallback = True
        else:
            self.use_regex_fallback = True

        # Build regex rules from language patterns
        self.regex_rules = self._build_regex_rules()

    def _build_regex_rules(self) -> List[tuple]:
        """Build regex rules from language patterns."""
        if not self.language or not self.language.regex_patterns:
            return []

        rules = []
        for pattern, token_type in self.language.regex_patterns:
            color = self._get_token_color(token_type)
            rules.append((pattern, color))
        return rules

    def _get_token_color(self, token_type: str) -> str:
        """Map token type to theme color."""
        if token_type.startswith("comment"):
            return self.theme.comment
        if token_type.startswith("string"):
            return self.theme.string
        if token_type.startswith("function"):
            return self.theme.function
        if token_type in ("type", "class"):
            return self.theme.class_name
        if token_type == "keyword":
            return self.theme.keyword
        if token_type == "constant.builtin":
            return self.theme.builtin
        if token_type == "decorator":
            return self.theme.decorator
        if token_type == "number":
            return self.theme.number
        if token_type in ("property", "instance"):
            return self.theme.instance
        return self.theme.editor_fg

    def _get_capture_color(self, capture_name: str) -> str:
        """Map tree-sitter capture names to theme colors."""
        if capture_name.startswith("comment"):
            return self.theme.comment
        if capture_name.startswith("string"):
            return self.theme.string
        if capture_name.startswith("function"):
            return self.theme.function
        if capture_name == "type":
            return self.theme.class_name
        if capture_name == "keyword":
            return self.theme.keyword
        if capture_name == "constant.builtin":
            return self.theme.builtin
        if capture_name == "decorator":
            return self.theme.decorator
        if capture_name == "number":
            return self.theme.number
        if capture_name == "property":
            return self.theme.instance
        return self.theme.editor_fg

    def _update_offsets(self, document: Document):
        """Calculate byte offset for every line start."""
        offsets = [0]
        current = 0
        for line in document.lines:
            current += len(bytes(line, "utf8")) + 1
            offsets.append(current)
        self.line_byte_offsets = offsets

    def _trigger_parse(self, document: Document):
        """Debounced trigger to parse the document in background."""
        if self._parse_timer:
            self._parse_timer.cancel()

        if self.last_parsed_version == -1:
            self._parse_worker(document)
        else:
            self._parse_timer = threading.Timer(
                0.05, self._parse_worker, args=[document]
            )
            self._parse_timer.start()

    def _parse_worker(self, document: Document):
        """Parse the document (may run on separate thread)."""
        try:
            full_text = document.get_full_text()
            current_version = document.version

            text_bytes = bytes(full_text, "utf8")

            with self._lock:
                tree = self.parser.parse(text_bytes)

                new_captures = []
                import tree_sitter

                cursor = None
                try:
                    if hasattr(tree_sitter, "QueryCursor"):
                        try:
                            cursor = tree_sitter.QueryCursor(self.query)
                        except:
                            cursor = tree_sitter.QueryCursor()
                        new_captures = (
                            cursor.captures(tree.root_node)
                            if hasattr(cursor, "captures")
                            else cursor.captures(self.query, tree.root_node)
                        )
                except:
                    if hasattr(self.query, "captures"):
                        new_captures = self.query.captures(tree.root_node)
                    elif hasattr(self.query, "matches"):
                        for _, d in self.query.matches(tree.root_node):
                            for k, v in d.items():
                                nodes = v if isinstance(v, list) else [v]
                                name = (
                                    self.query.capture_names[k]
                                    if isinstance(k, int)
                                    else k
                                )
                                for n in nodes:
                                    new_captures.append((n, name))

                final_captures = []

                def get_name(n):
                    return self.query.capture_names[n] if isinstance(n, int) else n

                if isinstance(new_captures, dict):
                    for name, nodes in new_captures.items():
                        for n in nodes if isinstance(nodes, list) else [nodes]:
                            final_captures.append((n, get_name(name)))
                elif isinstance(new_captures, list):
                    for item in new_captures:
                        if hasattr(item, "node"):
                            final_captures.append((item.node, get_name(item.index)))
                        elif isinstance(item, tuple):
                            final_captures.append((item[0], get_name(item[1])))

                final_captures.sort(key=lambda x: x[0].start_byte)

                self.cached_captures = final_captures
                self.last_parsed_version = current_version
                self._update_offsets(document)

        except Exception as e:
            print(f"Background parse error: {e}")

    def run(
        self,
        line_text: str,
        line_num: int,
        document: Document,
        search_matches: List = None,
        current_match_index: int = -1,
    ) -> List[ft.TextSpan]:
        """
        Generate highlighted text spans for a line.

        Args:
            line_text: The text content of the line
            line_num: The line number (0-indexed)
            document: The document instance
            search_matches: Optional list of SearchMatch objects
            current_match_index: Index of the currently selected match
        """
        style_map = [self.theme.editor_fg] * len(line_text)
        search_bg_map = [None] * len(line_text)  # Track search highlighting

        # Apply search match highlighting
        if search_matches:
            for idx, match in enumerate(search_matches):
                if match.line == line_num:
                    bg_color = (
                        self.theme.search_current_bg
                        if idx == current_match_index
                        else self.theme.search_match_bg
                    )
                    for i in range(match.start_col, min(match.end_col, len(line_text))):
                        search_bg_map[i] = bg_color

        if not self.use_regex_fallback:
            if document.version != self.last_parsed_version:
                self._trigger_parse(document)

            if len(self.line_byte_offsets) > line_num:
                current_byte_offset = self.line_byte_offsets[line_num]
                line_len_bytes = len(bytes(line_text, "utf8"))
                line_end_offset = current_byte_offset + line_len_bytes

                for node, capture_name in self.cached_captures:
                    if node.end_byte <= current_byte_offset:
                        continue
                    if node.start_byte >= line_end_offset:
                        break

                    start_local = max(0, node.start_byte - current_byte_offset)
                    end_local = min(line_len_bytes, node.end_byte - current_byte_offset)

                    color = self._get_capture_color(capture_name)
                    if capture_name == "variable":
                        if line_text[start_local:end_local] in ["self", "cls"]:
                            color = self.theme.instance

                    for i in range(start_local, end_local):
                        if i < len(style_map):
                            style_map[i] = color
            else:
                for pattern, color in self.regex_rules:
                    for match in re.finditer(pattern, line_text):
                        for i in range(match.start(), match.end()):
                            style_map[i] = color
        else:
            for pattern, color in self.regex_rules:
                for match in re.finditer(pattern, line_text):
                    for i in range(match.start(), match.end()):
                        style_map[i] = color

        # Span merging
        spans = []
        cur = document.cursor.normalized()

        sel_start_idx = -1
        sel_end_idx = -1
        is_line_selected = False

        if cur.has_selection():
            if cur.line < line_num < cur.anchor_line:
                is_line_selected = True
            elif cur.line == line_num:
                sel_start_idx = cur.column
                if cur.anchor_line == line_num:
                    sel_end_idx = cur.anchor_column
                else:
                    sel_end_idx = len(line_text) + 1
            elif cur.anchor_line == line_num:
                sel_start_idx = 0
                sel_end_idx = cur.anchor_column

        current_text = ""
        current_color = self.theme.editor_fg
        current_bg = self.theme.selection_bg if is_line_selected else None

        loop_len = len(line_text)

        for i in range(loop_len + 1):
            is_end = i == loop_len
            char = line_text[i] if not is_end else ""
            char_color = style_map[i] if not is_end else None
            char_bg = None

            if not is_end:
                # Priority: selection > search highlight
                if is_line_selected:
                    char_bg = self.theme.selection_bg
                elif sel_start_idx != -1 and sel_start_idx <= i < sel_end_idx:
                    char_bg = self.theme.selection_bg
                elif search_bg_map[i]:
                    char_bg = search_bg_map[i]

                if self.config.show_spaces and char == " ":
                    char = "\u00B7"
                    char_color = self.theme.invisible_fg
                elif self.config.show_tabs and char == "\t":
                    char = "\u25B8"
                    char_color = self.theme.invisible_fg

            is_cursor = line_num == document.cursor.line and i == document.cursor.column

            if (
                is_end
                or (char_color != current_color)
                or (char_bg != current_bg)
                or is_cursor
            ):
                if current_text:
                    spans.append(
                        ft.TextSpan(
                            current_text,
                            style=ft.TextStyle(
                                font_family=self.config.font_family,
                                size=self.config.font_size,
                                color=current_color,
                                bgcolor=current_bg,
                            ),
                        )
                    )

                if is_cursor:
                    cursor_ch = char if not is_end else "\u00A0"
                    if cursor_ch == "\n":
                        cursor_ch = "\u00A0"
                    spans.append(
                        ft.TextSpan(
                            cursor_ch,
                            style=ft.TextStyle(
                                font_family=self.config.font_family,
                                size=self.config.font_size,
                                color=self.theme.cursor_fg,
                                bgcolor=self.theme.cursor_bg,
                            ),
                        )
                    )
                    current_text = ""
                    current_color = char_color
                    current_bg = char_bg
                    continue

                current_text = ""
                current_color = char_color
                current_bg = char_bg

            if not is_end:
                current_text += char

        # Add line break symbol at end of line (except last line)
        if self.config.show_line_breaks and line_num < len(document.lines) - 1:
            spans.append(
                ft.TextSpan(
                    "\u00AC",
                    style=ft.TextStyle(
                        font_family=self.config.font_family,
                        size=self.config.font_size,
                        color=self.theme.invisible_fg,
                    ),
                )
            )

        return spans
