"""Text object operations for vim.

Text objects allow operating on semantic units like words, quotes, parentheses, etc.
Examples:
    - diw: delete inner word
    - ci": change inside quotes
    - da(: delete around parentheses
    - yi{: yank inside braces
"""

from typing import Tuple, Optional


class TextObjectMixin:
    """Mixin providing text object operations."""

    # Bracket pairs
    BRACKET_PAIRS = {
        "(": ")",
        ")": "(",
        "[": "]",
        "]": "[",
        "{": "}",
        "}": "{",
        "<": ">",
        ">": "<",
    }

    # Quote characters
    QUOTE_CHARS = {'"', "'", "`"}

    def get_text_object(
        self, obj_type: str, obj_char: str, inner: bool = True
    ) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get the range for a text object.

        Args:
            obj_type: Type of object ('w' for word, bracket char, quote char)
            obj_char: The character (for brackets/quotes)
            inner: True for 'inner', False for 'around'

        Returns:
            Tuple of (start_pos, end_pos) or None if not found
            Each pos is (row, col)
        """
        if obj_type == "w":
            return self._get_word_object(inner)
        elif obj_char in self.BRACKET_PAIRS:
            return self._get_bracket_object(obj_char, inner)
        elif obj_char in self.QUOTE_CHARS:
            return self._get_quote_object(obj_char, inner)
        return None

    def _get_word_object(
        self, inner: bool = True
    ) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get word text object range.

        Args:
            inner: True for iw (inner word), False for aw (around word)

        Returns:
            (start_pos, end_pos) or None
        """
        row, col = self.cursor_location
        line = str(self.get_line(row))

        if col >= len(line):
            return None

        # Find word boundaries
        start = col
        end = col

        # Expand left to word start
        while start > 0 and line[start - 1].isalnum():
            start -= 1

        # Expand right to word end
        while end < len(line) and line[end].isalnum():
            end += 1

        # For 'around word' (aw), include trailing whitespace
        if not inner:
            while end < len(line) and line[end].isspace():
                end += 1

        if start == end:
            return None

        return ((row, start), (row, end))

    def _get_bracket_object(
        self, bracket: str, inner: bool = True
    ) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get bracket pair text object range.

        Args:
            bracket: Opening or closing bracket character
            inner: True for inner, False for around (includes brackets)

        Returns:
            (start_pos, end_pos) or None
        """
        # Determine opening and closing brackets
        if bracket in "([{<":
            open_char = bracket
            close_char = self.BRACKET_PAIRS[bracket]
        else:
            close_char = bracket
            open_char = self.BRACKET_PAIRS[bracket]

        row, col = self.cursor_location
        line = str(self.get_line(row))

        # Find the enclosing brackets
        # This is a simplified implementation - real vim does multiline
        open_pos = None
        close_pos = None
        depth = 0

        # Search backward for opening bracket
        for i in range(col, -1, -1):
            if line[i] == close_char:
                depth += 1
            elif line[i] == open_char:
                if depth == 0:
                    open_pos = i
                    break
                depth -= 1

        if open_pos is None:
            return None

        # Search forward for closing bracket
        depth = 0
        for i in range(col, len(line)):
            if line[i] == open_char:
                depth += 1
            elif line[i] == close_char:
                if depth == 0:
                    close_pos = i
                    break
                depth -= 1

        if close_pos is None:
            return None

        # Return based on inner/around
        if inner:
            return ((row, open_pos + 1), (row, close_pos))
        else:
            return ((row, open_pos), (row, close_pos + 1))

    def _get_quote_object(
        self, quote: str, inner: bool = True
    ) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get quoted string text object range.

        Args:
            quote: Quote character (", ', or `)
            inner: True for inner, False for around (includes quotes)

        Returns:
            (start_pos, end_pos) or None
        """
        row, col = self.cursor_location
        line = str(self.get_line(row))

        # Find the enclosing quotes
        # Search backward for opening quote
        open_pos = None
        for i in range(col, -1, -1):
            if line[i] == quote:
                # Check if it's escaped
                if i > 0 and line[i - 1] == "\\":
                    continue
                open_pos = i
                break

        if open_pos is None:
            return None

        # Search forward for closing quote
        close_pos = None
        for i in range(open_pos + 1, len(line)):
            if line[i] == quote:
                # Check if it's escaped
                if line[i - 1] == "\\":
                    continue
                close_pos = i
                break

        if close_pos is None:
            return None

        # Return based on inner/around
        if inner:
            return ((row, open_pos + 1), (row, close_pos))
        else:
            return ((row, open_pos), (row, close_pos + 1))

    # === TEXT OBJECT OPERATIONS ===

    def delete_text_object(self, obj_type: str, obj_char: str = "", inner: bool = True) -> bool:
        """Delete a text object (diw, da", etc.).

        Args:
            obj_type: Type of object ('w', bracket, quote)
            obj_char: Character for bracket/quote objects
            inner: True for inner, False for around

        Returns:
            True if operation succeeded
        """
        text_range = self.get_text_object(obj_type, obj_char, inner)
        if not text_range:
            return False

        start_pos, end_pos = text_range
        # Select the range and delete
        # This is simplified - real implementation would need to handle selection properly
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        if start_row == end_row:
            # Same line - delete the range
            line = str(self.get_line(start_row))
            deleted = line[start_col:end_col]
            self.yank_register = deleted

            # Position cursor and delete characters
            self.cursor_location = start_pos
            for _ in range(end_col - start_col):
                self.action_delete_right()
            return True

        return False

    def change_text_object(self, obj_type: str, obj_char: str = "", inner: bool = True) -> bool:
        """Change a text object (ciw, ca", etc.).

        Args:
            obj_type: Type of object ('w', bracket, quote)
            obj_char: Character for bracket/quote objects
            inner: True for inner, False for around

        Returns:
            True if operation succeeded
        """
        if self.delete_text_object(obj_type, obj_char, inner):
            self._enter_insert_mode()
            return True
        return False

    def yank_text_object(self, obj_type: str, obj_char: str = "", inner: bool = True) -> bool:
        """Yank a text object (yiw, ya", etc.).

        Args:
            obj_type: Type of object ('w', bracket, quote)
            obj_char: Character for bracket/quote objects
            inner: True for inner, False for around

        Returns:
            True if operation succeeded
        """
        text_range = self.get_text_object(obj_type, obj_char, inner)
        if not text_range:
            return False

        start_pos, end_pos = text_range
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        if start_row == end_row:
            line = str(self.get_line(start_row))
            self.yank_register = line[start_col:end_col]
            return True

        return False
