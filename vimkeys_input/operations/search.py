"""Character search operations for vim mode."""


class SearchMixin:
    """Mixin providing character search operations."""

    # === CHARACTER SEARCH ===

    def search_char_forward(self, char: str) -> bool:
        """Find character forward on current line (f{char}).

        Args:
            char: Character to search for

        Returns:
            True if character was found, False otherwise
        """
        row, col = self.cursor_location
        line = str(str(self.get_line(row)))

        # Search for character after cursor
        if col + 1 < len(line):
            idx = line.find(char, col + 1)
            if idx != -1:
                self.cursor_location = (row, idx)
                self.last_f_search = ("f", char)
                return True

        return False

    def search_char_backward(self, char: str) -> bool:
        """Find character backward on current line (F{char}).

        Args:
            char: Character to search for

        Returns:
            True if character was found, False otherwise
        """
        row, col = self.cursor_location
        line = str(str(self.get_line(row)))

        # Search for character before cursor
        if col > 0:
            idx = line.rfind(char, 0, col)
            if idx != -1:
                self.cursor_location = (row, idx)
                self.last_f_search = ("F", char)
                return True

        return False

    def search_till_forward(self, char: str) -> bool:
        """Move till (before) character forward (t{char}).

        Args:
            char: Character to search for

        Returns:
            True if character was found, False otherwise
        """
        row, col = self.cursor_location

        # Find the character
        if self.search_char_forward(char):
            # Move back one to stop before it
            _, new_col = self.cursor_location
            if new_col > col:  # Make sure we actually moved
                self.action_cursor_left()
                self.last_f_search = ("t", char)
                return True
            else:
                # Restore position if we didn't move
                self.cursor_location = (row, col)

        return False

    def search_till_backward(self, char: str) -> bool:
        """Move till (after) character backward (T{char}).

        Args:
            char: Character to search for

        Returns:
            True if character was found, False otherwise
        """
        row, col = self.cursor_location

        # Find the character
        if self.search_char_backward(char):
            # Move forward one to stop after it
            _, new_col = self.cursor_location
            if new_col < col:  # Make sure we actually moved
                self.action_cursor_right()
                self.last_f_search = ("T", char)
                return True
            else:
                # Restore position if we didn't move
                self.cursor_location = (row, col)

        return False

    def search_repeat(self) -> bool:
        """Repeat last f/t search (;).

        Returns:
            True if search was successful, False otherwise
        """
        if not self.last_f_search:
            return False

        search_type, char = self.last_f_search

        if search_type == "f":
            return self.search_char_forward(char)
        elif search_type == "F":
            return self.search_char_backward(char)
        elif search_type == "t":
            return self.search_till_forward(char)
        elif search_type == "T":
            return self.search_till_backward(char)

        return False

    def search_repeat_reverse(self) -> bool:
        """Repeat last f/t search in opposite direction (,).

        Returns:
            True if search was successful, False otherwise
        """
        if not self.last_f_search:
            return False

        search_type, char = self.last_f_search

        # Reverse the direction
        if search_type == "f":
            return self.search_char_backward(char)
        elif search_type == "F":
            return self.search_char_forward(char)
        elif search_type == "t":
            return self.search_till_backward(char)
        elif search_type == "T":
            return self.search_till_forward(char)

        return False

    # === WORD SEARCH ===

    def search_word_under_cursor(self, forward: bool = True) -> bool:
        """Search for word under cursor (* for forward, # for backward).

        Args:
            forward: If True, search forward; if False, search backward

        Returns:
            True if word was found, False otherwise
        """
        row, col = self.cursor_location
        line = str(str(self.get_line(row)))

        # Get word under cursor
        if col >= len(line) or not line[col].isalnum():
            return False

        # Find word boundaries
        start = col
        while start > 0 and line[start - 1].isalnum():
            start -= 1

        end = col
        while end < len(line) and line[end].isalnum():
            end += 1

        word = line[start:end]
        if not word:
            return False

        # Store word for future searches
        self.last_search_word = word

        # Search for next occurrence
        if forward:
            return self._search_word_forward(word, row, end)
        else:
            return self._search_word_backward(word, row, start)

    def _search_word_forward(self, word: str, start_row: int, start_col: int) -> bool:
        """Helper to search for word forward from position."""
        line_count = self.document.line_count

        # Search current line first (from start_col)
        line = str(self.get_line(start_row))[start_col:]
        idx = line.find(word)
        if idx != -1:
            self.cursor_location = (start_row, start_col + idx)
            return True

        # Search following lines
        for row in range(start_row + 1, line_count):
            line = str(str(self.get_line(row)))
            idx = line.find(word)
            if idx != -1:
                self.cursor_location = (row, idx)
                return True

        # Wrap around to beginning
        for row in range(0, start_row):
            line = str(str(self.get_line(row)))
            idx = line.find(word)
            if idx != -1:
                self.cursor_location = (row, idx)
                return True

        return False

    def _search_word_backward(self, word: str, start_row: int, start_col: int) -> bool:
        """Helper to search for word backward from position."""
        # Search current line first (up to start_col)
        line = str(self.get_line(start_row))[:start_col]
        idx = line.rfind(word)
        if idx != -1:
            self.cursor_location = (start_row, idx)
            return True

        # Search previous lines
        for row in range(start_row - 1, -1, -1):
            line = str(str(self.get_line(row)))
            idx = line.rfind(word)
            if idx != -1:
                self.cursor_location = (row, idx)
                return True

        # Wrap around to end
        line_count = self.document.line_count
        for row in range(line_count - 1, start_row, -1):
            line = str(str(self.get_line(row)))
            idx = line.rfind(word)
            if idx != -1:
                self.cursor_location = (row, idx)
                return True

        return False
