"""Visual mode operations for vim."""


class VisualMixin:
    """Mixin providing visual mode operations."""

    # === VISUAL MODE NAVIGATION ===

    def visual_left(self) -> None:
        """Extend selection left (h in visual mode)."""
        self.action_cursor_left_select()

    def visual_down(self) -> None:
        """Extend selection down (j in visual mode)."""
        self.action_cursor_down_select()

    def visual_up(self) -> None:
        """Extend selection up (k in visual mode)."""
        self.action_cursor_up_select()

    def visual_right(self) -> None:
        """Extend selection right (l in visual mode)."""
        self.action_cursor_right_select()

    def visual_word_forward(self) -> None:
        """Extend selection to next word (w in visual mode)."""
        self.action_cursor_word_right_select()

    def visual_word_backward(self) -> None:
        """Extend selection to previous word (b in visual mode)."""
        self.action_cursor_word_left_select()

    def visual_line_start(self) -> None:
        """Extend selection to line start (0 in visual mode)."""
        # Store current position
        start_row, start_col = self.cursor_location

        # Move to line start
        self.action_cursor_line_start()

        # If we moved, ensure selection extends correctly
        # TextArea handles this automatically with _select actions

    def visual_line_end(self) -> None:
        """Extend selection to line end ($ in visual mode)."""
        # TextArea will handle selection extension
        row, col = self.cursor_location
        line = str(self.get_line(row))

        # Move to end of line while selecting
        target_col = len(line)
        if col < target_col:
            for _ in range(target_col - col):
                self.action_cursor_right_select()
        elif col > target_col:
            for _ in range(col - target_col):
                self.action_cursor_left_select()

    # === VISUAL MODE OPERATIONS ===

    def visual_yank(self) -> None:
        """Yank (copy) selected text (y in visual mode)."""
        if self.selected_text:
            self.yank_register = self.selected_text

    def visual_delete(self) -> None:
        """Delete selected text (d or x in visual mode)."""
        if self.selected_text:
            self.yank_register = self.selected_text
            self.action_delete()

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
            self.cursor_location = (row, 0)
            self.action_indent()

    def visual_dedent(self) -> None:
        """Dedent selected lines (< in visual mode)."""
        # Get selection range
        if not self.selection:
            return

        start_row = min(self.selection.start[0], self.selection.end[0])
        end_row = max(self.selection.start[0], self.selection.end[0])

        # Dedent each line in selection
        for row in range(start_row, end_row + 1):
            self.cursor_location = (row, 0)
            self.action_dedent()

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
