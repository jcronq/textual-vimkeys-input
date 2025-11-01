"""Navigation operations for vim mode."""


class NavigationMixin:
    """Mixin providing vim navigation operations."""

    # === BASIC NAVIGATION ===

    def nav_left(self) -> None:
        """Move cursor left (h)."""
        self.action_cursor_left()

    def nav_down(self) -> None:
        """Move cursor down (j)."""
        self.action_cursor_down()

    def nav_up(self) -> None:
        """Move cursor up (k)."""
        self.action_cursor_up()

    def nav_right(self) -> None:
        """Move cursor right (l)."""
        self.action_cursor_right()

    # === WORD NAVIGATION ===

    def nav_word_forward(self) -> None:
        """Move to start of next word (w)."""
        self.action_cursor_word_right()

    def nav_word_backward(self) -> None:
        """Move to start of previous word (b)."""
        self.action_cursor_word_left()

    def nav_word_end(self) -> None:
        """Move to end of current/next word (e)."""
        # TextArea doesn't have word_end action, so approximate
        self.action_cursor_word_right()
        # Move back one if we're not at line end
        row, col = self.cursor_location
        line = str(str(self.get_line(row)))
        if col > 0 and col < len(line):
            self.action_cursor_left()

    # === LINE NAVIGATION ===

    def nav_line_start(self) -> None:
        """Move to start of line (0)."""
        self.action_cursor_line_start()

    def nav_line_end(self) -> None:
        """Move to end of line ($)."""
        self.action_cursor_line_end()

    def nav_first_non_whitespace(self) -> None:
        """Move to first non-whitespace character (^)."""
        row, _ = self.cursor_location
        line = str(str(self.get_line(row)))

        # Find first non-whitespace character
        for i, char in enumerate(line):
            if not char.isspace():
                self.cursor_location = (row, i)
                return

        # If all whitespace or empty, go to line start
        self.action_cursor_line_start()

    # === DOCUMENT NAVIGATION ===

    def nav_document_start(self) -> None:
        """Move to start of document (gg)."""
        self.cursor_location = (0, 0)

    def nav_document_end(self) -> None:
        """Move to end of document (G)."""
        line_count = self.document.line_count
        if line_count > 0:
            self.cursor_location = (line_count - 1, 0)

    def nav_page_down(self) -> None:
        """Move page down (Ctrl+d)."""
        self.action_cursor_page_down()

    def nav_page_up(self) -> None:
        """Move page up (Ctrl+u)."""
        self.action_cursor_page_up()

    # === PARAGRAPH NAVIGATION ===

    def nav_paragraph_forward(self) -> None:
        """Move to next paragraph ({)."""
        row, col = self.cursor_location
        line_count = self.document.line_count

        # Find next blank line
        found_text = False
        for i in range(row + 1, line_count):
            line = str(self.get_line(i)).strip()
            if line:
                found_text = True
            elif found_text:
                # Found blank line after text
                self.cursor_location = (i, 0)
                return

        # If no blank line found, go to end
        self.nav_document_end()

    def nav_paragraph_backward(self) -> None:
        """Move to previous paragraph (})."""
        row, col = self.cursor_location

        # Find previous blank line
        found_text = False
        for i in range(row - 1, -1, -1):
            line = str(self.get_line(i)).strip()
            if line:
                found_text = True
            elif found_text:
                # Found blank line after text (going backwards)
                self.cursor_location = (i, 0)
                return

        # If no blank line found, go to start
        self.nav_document_start()

    # === LINE NUMBERS ===

    def nav_goto_line(self, line_num: int) -> None:
        """Go to specific line number (:<number>).

        Args:
            line_num: Line number (1-indexed)
        """
        line_count = self.document.line_count
        # Convert to 0-indexed and clamp to valid range
        target = max(0, min(line_num - 1, line_count - 1))
        self.cursor_location = (target, 0)
