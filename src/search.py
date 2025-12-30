"""Search functionality for the code editor."""

import re
from dataclasses import dataclass
from typing import List, Optional, Callable


@dataclass
class SearchMatch:
    """Represents a single search match."""

    line: int
    start_col: int
    end_col: int
    text: str

    def __eq__(self, other):
        if not isinstance(other, SearchMatch):
            return False
        return (
            self.line == other.line
            and self.start_col == other.start_col
            and self.end_col == other.end_col
        )


class Search:
    """Handles search and replace operations in the document."""

    def __init__(self, document, on_change: Optional[Callable] = None):
        """
        Initialize the search.

        Args:
            document: The Document instance to search in
            on_change: Optional callback when search state changes
        """
        self.document = document
        self.on_change = on_change

        # Search state
        self._query: str = ""
        self._regex: bool = False
        self._case_sensitive: bool = False
        self._whole_word: bool = False

        # Results
        self._matches: List[SearchMatch] = []
        self._current_index: int = -1

    @property
    def query(self) -> str:
        """Current search query."""
        return self._query

    @property
    def is_regex(self) -> bool:
        """Whether regex mode is enabled."""
        return self._regex

    @property
    def is_case_sensitive(self) -> bool:
        """Whether case-sensitive mode is enabled."""
        return self._case_sensitive

    @property
    def is_whole_word(self) -> bool:
        """Whether whole-word mode is enabled."""
        return self._whole_word

    @property
    def matches(self) -> List[SearchMatch]:
        """List of all matches."""
        return self._matches.copy()

    @property
    def match_count(self) -> int:
        """Total number of matches."""
        return len(self._matches)

    @property
    def current_index(self) -> int:
        """Index of the currently selected match (-1 if none)."""
        return self._current_index

    @property
    def current_match(self) -> Optional[SearchMatch]:
        """The currently selected match, or None."""
        if 0 <= self._current_index < len(self._matches):
            return self._matches[self._current_index]
        return None

    def _notify_change(self):
        """Notify listeners of state change."""
        if self.on_change:
            self.on_change()

    def _build_pattern(self, query: str) -> Optional[re.Pattern]:
        """Build a regex pattern from the query."""
        if not query:
            return None

        try:
            if self._regex:
                pattern = query
            else:
                pattern = re.escape(query)

            if self._whole_word:
                pattern = rf"\b{pattern}\b"

            flags = 0 if self._case_sensitive else re.IGNORECASE
            return re.compile(pattern, flags)
        except re.error:
            return None

    def find(
        self,
        query: str,
        regex: bool = False,
        case_sensitive: bool = False,
        whole_word: bool = False,
    ) -> int:
        """
        Search for all occurrences of the query.

        Args:
            query: The search string or regex pattern
            regex: Enable regex mode
            case_sensitive: Enable case-sensitive matching
            whole_word: Match whole words only

        Returns:
            Number of matches found
        """
        self._query = query
        self._regex = regex
        self._case_sensitive = case_sensitive
        self._whole_word = whole_word
        self._matches = []
        self._current_index = -1

        if not query:
            self._notify_change()
            return 0

        pattern = self._build_pattern(query)
        if not pattern:
            self._notify_change()
            return 0

        # Search all lines
        for line_num, line_text in enumerate(self.document.lines):
            for match in pattern.finditer(line_text):
                self._matches.append(
                    SearchMatch(
                        line=line_num,
                        start_col=match.start(),
                        end_col=match.end(),
                        text=match.group(),
                    )
                )

        # Select first match if any
        if self._matches:
            self._current_index = 0

        self._notify_change()
        return len(self._matches)

    def find_next(self) -> Optional[SearchMatch]:
        """
        Move to the next match.

        Returns:
            The next match, or None if no matches
        """
        if not self._matches:
            return None

        self._current_index = (self._current_index + 1) % len(self._matches)
        self._notify_change()
        return self.current_match

    def find_previous(self) -> Optional[SearchMatch]:
        """
        Move to the previous match.

        Returns:
            The previous match, or None if no matches
        """
        if not self._matches:
            return None

        self._current_index = (self._current_index - 1) % len(self._matches)
        self._notify_change()
        return self.current_match

    def go_to_match(self, index: int) -> Optional[SearchMatch]:
        """
        Go to a specific match by index.

        Args:
            index: The match index to go to

        Returns:
            The match at that index, or None if invalid
        """
        if not self._matches or not (0 <= index < len(self._matches)):
            return None

        self._current_index = index
        self._notify_change()
        return self.current_match

    def select_current_match(self):
        """Select the current match in the document (move cursor and create selection)."""
        match = self.current_match
        if not match:
            return

        self.document.cursor.line = match.line
        self.document.cursor.column = match.start_col
        self.document.cursor.anchor_line = match.line
        self.document.cursor.anchor_column = match.end_col

    def replace_current(self, replacement: str) -> bool:
        """
        Replace the current match with the replacement text.

        Args:
            replacement: The replacement text

        Returns:
            True if replacement was made, False otherwise
        """
        match = self.current_match
        if not match:
            return False

        # Handle regex backreferences in replacement
        actual_replacement = replacement
        if self._regex:
            try:
                pattern = self._build_pattern(self._query)
                if pattern:
                    actual_replacement = pattern.sub(
                        replacement, match.text, count=1
                    )
            except re.error:
                pass

        # Select and delete the match
        self.document.cursor.line = match.line
        self.document.cursor.column = match.start_col
        self.document.cursor.anchor_line = match.line
        self.document.cursor.anchor_column = match.end_col
        self.document.delete_selected_text()

        # Insert replacement
        self.document.insert_text(actual_replacement)

        # Re-run search to update matches
        old_index = self._current_index
        self.find(self._query, self._regex, self._case_sensitive, self._whole_word)

        # Try to stay at same index or move to next
        if self._matches:
            self._current_index = min(old_index, len(self._matches) - 1)
            if self._current_index < 0:
                self._current_index = 0

        self._notify_change()
        return True

    def replace_all(self, replacement: str) -> int:
        """
        Replace all matches with the replacement text.

        Args:
            replacement: The replacement text

        Returns:
            Number of replacements made
        """
        if not self._matches:
            return 0

        count = 0
        # Replace from bottom to top to preserve line/column positions
        for match in reversed(self._matches):
            actual_replacement = replacement
            if self._regex:
                try:
                    pattern = self._build_pattern(self._query)
                    if pattern:
                        actual_replacement = pattern.sub(
                            replacement, match.text, count=1
                        )
                except re.error:
                    pass

            # Select and delete the match
            self.document.cursor.line = match.line
            self.document.cursor.column = match.start_col
            self.document.cursor.anchor_line = match.line
            self.document.cursor.anchor_column = match.end_col
            self.document.delete_selected_text()

            # Insert replacement
            self.document.insert_text(actual_replacement)
            count += 1

        # Clear matches after replace all
        self._matches = []
        self._current_index = -1
        self._notify_change()

        return count

    def clear(self):
        """Clear the search state."""
        self._query = ""
        self._matches = []
        self._current_index = -1
        self._notify_change()

    def refresh(self):
        """Re-run the current search (useful after document changes)."""
        if self._query:
            self.find(self._query, self._regex, self._case_sensitive, self._whole_word)
