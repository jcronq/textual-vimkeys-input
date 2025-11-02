"""Visual mode operations for vim."""

from textual.widgets.text_area import Selection


class VisualMixin:
    """Mixin providing visual mode operations."""

    # === VISUAL MODE NAVIGATION ===

    def _make_inclusive_end(self, row: int, col: int) -> tuple[int, int]:
        """Convert a cursor position to an inclusive selection end.

        TextArea selections are exclusive at the end (like Python slices),
        but vim visual mode is inclusive. This extends the end position by 1.
        """
        line = str(self.get_line(row))
        # Don't extend past the line end
        if col < len(line):
            return (row, col + 1)
        return (row, col)

    def _extend_selection(self, new_row: int, new_col: int) -> None:
        """Extend selection to a new cursor position."""
        if self.selection.start == self.selection.end:
            # No selection yet, start from current cursor
            start = self.cursor_location
        else:
            # Keep the selection start, extend the end
            start = self.selection.start

        # Make the selection inclusive (vim behavior)
        inclusive_end = self._make_inclusive_end(new_row, new_col)
        self.selection = Selection(start=start, end=inclusive_end)
        self.cursor_location = (new_row, new_col)

    def visual_left(self) -> None:
        """Extend selection left (h in visual mode)."""
        row, col = self.cursor_location
        if col > 0:
            self._extend_selection(row, col - 1)

    def visual_down(self) -> None:
        """Extend selection down (j in visual mode)."""
        row, col = self.cursor_location
        if row < self.document.line_count - 1:
            self._extend_selection(row + 1, col)

    def visual_up(self) -> None:
        """Extend selection up (k in visual mode)."""
        row, col = self.cursor_location
        if row > 0:
            self._extend_selection(row - 1, col)

    def visual_right(self) -> None:
        """Extend selection right (l in visual mode)."""
        row, col = self.cursor_location
        line = str(self.get_line(row))
        if col < len(line):
            self._extend_selection(row, col + 1)

    def visual_word_forward(self) -> None:
        """Extend selection to next word (w in visual mode)."""
        # Save selection start before navigation (which clears selection)
        selection_start = (
            self.selection.start
            if self.selection.start != self.selection.end
            else self.cursor_location
        )
        # Use navigation to find next word
        self.nav_word_forward()
        # Restore and extend selection to new position (inclusive)
        new_row, new_col = self.cursor_location
        inclusive_end = self._make_inclusive_end(new_row, new_col)
        self.selection = Selection(start=selection_start, end=inclusive_end)

    def visual_word_backward(self) -> None:
        """Extend selection to previous word (b in visual mode)."""
        # Save selection start before navigation (which clears selection)
        selection_start = (
            self.selection.start
            if self.selection.start != self.selection.end
            else self.cursor_location
        )
        # Use navigation to find previous word
        self.nav_word_backward()
        # Restore and extend selection to new position (inclusive)
        new_row, new_col = self.cursor_location
        inclusive_end = self._make_inclusive_end(new_row, new_col)
        self.selection = Selection(start=selection_start, end=inclusive_end)

    def visual_word_end(self) -> None:
        """Extend selection to end of word (e in visual mode)."""
        # Save selection start before navigation (which clears selection)
        selection_start = (
            self.selection.start
            if self.selection.start != self.selection.end
            else self.cursor_location
        )
        # Use navigation to find word end
        self.nav_word_end()
        # Restore and extend selection to new position (inclusive)
        new_row, new_col = self.cursor_location
        inclusive_end = self._make_inclusive_end(new_row, new_col)
        self.selection = Selection(start=selection_start, end=inclusive_end)

    def visual_line_start(self) -> None:
        """Extend selection to line start (0 in visual mode)."""
        # Get current position
        row, _ = self.cursor_location
        # Extend selection to start of line
        self._extend_selection(row, 0)

    def visual_line_end(self) -> None:
        """Extend selection to line end ($ in visual mode)."""
        # Get current position
        row, _ = self.cursor_location
        line = str(self.get_line(row))
        # Position cursor at last character of line (or 0 if empty)
        last_col = max(0, len(line) - 1) if len(line) > 0 else 0
        # Extend selection to end of line (inclusive)
        self._extend_selection(row, last_col)

    def visual_document_start(self) -> None:
        """Extend selection to document start (gg in visual mode)."""
        # Save selection start before navigation (which clears selection)
        selection_start = (
            self.selection.start
            if self.selection.start != self.selection.end
            else self.cursor_location
        )
        # Navigate to document start
        self.nav_document_start()
        # Restore and extend selection to new position (inclusive)
        new_row, new_col = self.cursor_location
        inclusive_end = self._make_inclusive_end(new_row, new_col)
        self.selection = Selection(start=selection_start, end=inclusive_end)

    def visual_document_end(self) -> None:
        """Extend selection to document end (G in visual mode)."""
        # Save selection start before navigation (which clears selection)
        selection_start = (
            self.selection.start
            if self.selection.start != self.selection.end
            else self.cursor_location
        )
        # Navigate to document end
        self.nav_document_end()
        # Restore and extend selection to new position (inclusive)
        new_row, new_col = self.cursor_location
        inclusive_end = self._make_inclusive_end(new_row, new_col)
        self.selection = Selection(start=selection_start, end=inclusive_end)

    # === VISUAL MODE OPERATIONS ===

    def visual_yank(self) -> None:
        """Yank (copy) selected text (y in visual mode)."""
        if self.selected_text:
            self.yank_register = self.selected_text

    def visual_delete(self) -> None:
        """Delete selected text (d or x in visual mode)."""
        if self.selected_text:
            self.yank_register = self.selected_text
            # Use TextArea's replace method to delete (replace with empty string)
            self.replace("", self.selection.start, self.selection.end)

    def visual_change(self) -> None:
        """Delete selected text and enter insert mode (c in visual mode)."""
        self.visual_delete()
        self._enter_insert_mode()

    def visual_indent(self) -> None:
        """Indent selected lines (> in visual mode)."""
        # Get selection range
        if not self.selection:
            return

        start_row = min(self.selection.start[0], self.selection.end[0])
        end_row = max(self.selection.start[0], self.selection.end[0])

        # Indent each line in selection
        for row in range(start_row, end_row + 1):
            line = str(self.get_line(row))
            # Add 4 spaces at start of line
            self.replace("    " + line, (row, 0), (row, len(line)))

    def visual_dedent(self) -> None:
        """Dedent selected lines (< in visual mode)."""
        # Get selection range
        if not self.selection:
            return

        start_row = min(self.selection.start[0], self.selection.end[0])
        end_row = max(self.selection.start[0], self.selection.end[0])

        # Dedent each line in selection
        for row in range(start_row, end_row + 1):
            line = str(self.get_line(row))
            # Remove up to 4 leading spaces
            dedented = line[4:] if line.startswith("    ") else line.lstrip(" ", 1)
            self.replace(dedented, (row, 0), (row, len(line)))

    def visual_toggle_case(self) -> None:
        """Toggle case of selected text (~)."""
        if not self.selected_text:
            return

        # Toggle case
        toggled = self.selected_text.swapcase()

        # Replace selection
        self.action_delete()
        self.insert(toggled)

    def visual_uppercase(self) -> None:
        """Convert selected text to uppercase (U in visual mode)."""
        if not self.selected_text:
            return

        uppercased = self.selected_text.upper()
        self.action_delete()
        self.insert(uppercased)

    def visual_lowercase(self) -> None:
        """Convert selected text to lowercase (u in visual mode)."""
        if not self.selected_text:
            return

        lowercased = self.selected_text.lower()
        self.action_delete()
        self.insert(lowercased)
