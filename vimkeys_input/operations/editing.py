"""Editing operations for vim mode."""


class EditingMixin:
    """Mixin providing vim editing operations."""

    # === CHARACTER OPERATIONS ===

    def edit_delete_char(self) -> None:
        """Delete character under cursor (x)."""
        self.action_delete_right()

    def edit_delete_char_back(self) -> None:
        """Delete character before cursor (X)."""
        self.action_delete_left()

    def edit_replace_char(self, char: str) -> None:
        """Replace character under cursor (r{char}).

        Args:
            char: Character to replace with
        """
        # Delete current character
        self.action_delete_right()
        # Insert new character
        self.insert(char)
        # Move back to stay on the character
        self.action_cursor_left()

    # === LINE OPERATIONS ===

    def edit_delete_line(self) -> None:
        """Delete current line (dd)."""
        row, col = self.cursor_location
        line_text = str(str(self.get_line(row)))

        # Save to yank register
        self.yank_register = line_text

        # Delete the line
        self.action_delete_line()

    def edit_yank_line(self) -> None:
        """Yank (copy) current line (yy)."""
        row, col = self.cursor_location
        line_text = str(str(self.get_line(row)))
        self.yank_register = line_text

    def edit_delete_to_line_end(self) -> None:
        """Delete from cursor to end of line (D)."""
        row, col = self.cursor_location
        line = str(str(self.get_line(row)))

        # Save deleted text to yank register
        self.yank_register = line[col:]

        # Delete to end of line
        self.action_delete_to_end_of_line()

    def edit_delete_to_line_start(self) -> None:
        """Delete from cursor to start of line."""
        row, col = self.cursor_location
        line = str(str(self.get_line(row)))

        # Save deleted text to yank register
        self.yank_register = line[:col]

        # Delete to start of line
        self.action_delete_to_start_of_line()

    def edit_change_line(self) -> None:
        """Delete line and enter insert mode (cc)."""
        self.edit_delete_line()
        self._enter_insert_mode()

    # === PASTE OPERATIONS ===

    def edit_paste_after(self) -> None:
        """Paste after cursor (p)."""
        if not self.yank_register:
            return

        # Check if we yanked a full line (ends with newline)
        if self.yank_register.endswith("\n"):
            # Paste line below current line
            self.action_cursor_line_end()
            self.insert("\n" + self.yank_register.rstrip("\n"))
        else:
            # Paste after cursor
            self.action_cursor_right()
            self.insert(self.yank_register)

    def edit_paste_before(self) -> None:
        """Paste before cursor (P)."""
        if not self.yank_register:
            return

        # Check if we yanked a full line
        if self.yank_register.endswith("\n"):
            # Paste line above current line
            self.action_cursor_line_start()
            self.insert(self.yank_register)
            self.action_cursor_up()
        else:
            # Paste before cursor
            self.insert(self.yank_register)

    # === OPEN LINE OPERATIONS ===

    def edit_open_line_below(self) -> None:
        """Open new line below current line (o)."""
        self.action_cursor_line_end()
        self.insert("\n")

    def edit_open_line_above(self) -> None:
        """Open new line above current line (O)."""
        self.action_cursor_line_start()
        self.insert("\n")
        self.action_cursor_up()

    # === WORD OPERATIONS ===

    def edit_delete_word(self) -> None:
        """Delete word forward (dw)."""
        # Save cursor position
        start_row, start_col = self.cursor_location

        # Move to end of word
        self.action_cursor_word_right()

        end_row, end_col = self.cursor_location

        # If on same line, delete the range
        if start_row == end_row:
            line = str(str(self.get_line(start_row)))
            deleted = line[start_col:end_col]
            self.yank_register = deleted

            # Move back and delete
            self.cursor_location = (start_row, start_col)
            for _ in range(end_col - start_col):
                self.action_delete_right()

    def edit_change_word(self) -> None:
        """Change word (cw)."""
        self.edit_delete_word()
        self._enter_insert_mode()

    # === UNDO/REDO ===

    def edit_undo(self) -> None:
        """Undo last change (u)."""
        self.action_undo()

    def edit_redo(self) -> None:
        """Redo last undone change (Ctrl+r)."""
        self.action_redo()

    # === JOIN LINES ===

    def edit_join_lines(self) -> None:
        """Join current line with next line (J)."""
        row, col = self.cursor_location
        line_count = self.document.line_count

        # Can't join if on last line
        if row >= line_count - 1:
            return

        # Get current and next line
        current_line = str(str(self.get_line(row)))
        next_line = str(str(self.get_line(row + 1)))

        # Delete next line
        self.cursor_location = (row + 1, 0)
        self.action_delete_line()

        # Add space and next line content to current line
        self.cursor_location = (row, len(current_line))
        self.insert(" " + next_line.lstrip())

    # === INDENT ===

    def edit_indent(self) -> None:
        """Indent current line (>>)."""
        self.action_indent()

    def edit_dedent(self) -> None:
        """Dedent current line (<<)."""
        self.action_dedent()
