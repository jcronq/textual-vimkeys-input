"""VimTextArea - TextArea with vim keybindings and modes."""

from textual.widgets import TextArea
from textual.message import Message
from textual.reactive import reactive
from .vim_modes import VimMode, ModeIndicator


class VimTextArea(TextArea):
    """TextArea with vim keybindings and modes."""

    DEFAULT_CSS = """
    VimTextArea {
        border: solid $primary;
    }

    VimTextArea.insert-mode {
        border: solid green;
    }

    VimTextArea.command-mode {
        border: solid blue;
    }

    VimTextArea.visual-mode {
        border: solid yellow;
    }
    """

    # Reactive properties
    vim_mode = reactive(VimMode.INSERT)

    class Submitted(Message):
        """Posted when user submits text (Enter in insert mode)."""

        def __init__(self, text: str):
            super().__init__()
            self.text = text

    class ModeChanged(Message):
        """Posted when vim mode changes."""

        def __init__(self, mode: VimMode):
            super().__init__()
            self.mode = mode

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Vim state
        self.vim_mode = VimMode.INSERT
        self.visual_start = None  # For visual mode
        self.pending_command = None  # For dd, yy, gg, etc.
        self.last_f_search = None  # For f/t commands
        self.yank_register = ""  # Copied text

        # Initialize CSS class
        self._update_mode_display()

    def _update_mode_display(self):
        """Update CSS class and emit mode change event."""
        # Remove all mode classes
        self.remove_class("insert-mode", "command-mode", "visual-mode")

        # Add current mode class
        self.add_class(ModeIndicator.get_border_style(self.vim_mode))

        # Post mode change event
        self.post_message(self.ModeChanged(self.vim_mode))

    def on_key(self, event):
        """Main key event handler - routes based on vim mode."""

        # ESC always goes to command mode
        if event.key == "escape":
            self._enter_command_mode()
            event.prevent_default()
            return

        # Route to mode-specific handler
        if self.vim_mode == VimMode.INSERT:
            self._handle_insert_mode(event)
        elif self.vim_mode == VimMode.COMMAND:
            self._handle_command_mode(event)
        elif self.vim_mode == VimMode.VISUAL:
            self._handle_visual_mode(event)

    # === MODE TRANSITIONS ===

    def _enter_insert_mode(self):
        """Enter insert mode."""
        self.vim_mode = VimMode.INSERT
        self._update_mode_display()

    def _enter_command_mode(self):
        """Enter command mode."""
        self.vim_mode = VimMode.COMMAND
        self.visual_start = None
        self.pending_command = None  # Clear any pending commands
        self._update_mode_display()

    def _enter_visual_mode(self):
        """Enter visual mode."""
        self.vim_mode = VimMode.VISUAL
        self.visual_start = self.cursor_location
        self._update_mode_display()

    # === INSERT MODE ===

    def _handle_insert_mode(self, event):
        """Handle keys in insert mode."""

        # Enter submits (can be customized)
        if event.key == "enter":
            text = self.text
            self.clear()
            self.post_message(self.Submitted(text))
            event.prevent_default()
            return

        # Everything else: default TextArea behavior
        # (typing, backspace, arrows, etc.)

    # === COMMAND MODE ===

    def _handle_command_mode(self, event):
        """Handle keys in command mode."""
        key = event.key

        # Handle pending commands first (dd, yy, gg, etc.)
        if self.pending_command:
            self._handle_pending_command(event)
            event.prevent_default()
            return

        # === NAVIGATION ===

        # Basic movement (hjkl)
        if key == "h":
            self.action_cursor_left()
            event.prevent_default()
        elif key == "j":
            self.action_cursor_down()
            event.prevent_default()
        elif key == "k":
            self.action_cursor_up()
            event.prevent_default()
        elif key == "l":
            self.action_cursor_right()
            event.prevent_default()

        # Word movement
        elif key == "w":
            self.action_cursor_word_right()
            event.prevent_default()
        elif key == "b":
            self.action_cursor_word_left()
            event.prevent_default()
        elif key == "e":
            self._move_to_word_end()
            event.prevent_default()

        # Line movement
        elif key == "0":
            self.action_cursor_line_start()
            event.prevent_default()
        elif key == "dollar":  # $
            self.action_cursor_line_end()
            event.prevent_default()
        elif key == "circumflex":  # ^
            self._move_to_first_non_whitespace()
            event.prevent_default()

        # Document movement
        elif key == "g":
            # Next 'g' will trigger gg
            self.pending_command = "g"
            event.prevent_default()
        elif key == "G":  # Shift+g
            self._move_to_end_of_document()
            event.prevent_default()

        # === MODE CHANGES ===

        # Enter insert mode
        elif key == "i":
            self._enter_insert_mode()
            event.prevent_default()
        elif key == "I":  # Insert at line start
            self.action_cursor_line_start()
            self._enter_insert_mode()
            event.prevent_default()
        elif key == "a":
            self.action_cursor_right()
            self._enter_insert_mode()
            event.prevent_default()
        elif key == "A":  # Append at line end
            self.action_cursor_line_end()
            self._enter_insert_mode()
            event.prevent_default()
        elif key == "o":  # Open line below
            self._open_line_below()
            self._enter_insert_mode()
            event.prevent_default()
        elif key == "O":  # Open line above
            self._open_line_above()
            self._enter_insert_mode()
            event.prevent_default()

        # Enter visual mode
        elif key == "v":
            self._enter_visual_mode()
            event.prevent_default()

        # === EDITING ===

        # Delete character
        elif key == "x":
            self.action_delete_right()
            event.prevent_default()
        elif key == "X":  # Delete left
            self.action_delete_left()
            event.prevent_default()

        # Delete line (dd)
        elif key == "d":
            self.pending_command = "d"
            event.prevent_default()

        # Yank/copy line (yy)
        elif key == "y":
            self.pending_command = "y"
            event.prevent_default()

        # Paste
        elif key == "p":
            self._paste_after()
            event.prevent_default()
        elif key == "P":  # Paste before
            self._paste_before()
            event.prevent_default()

        # Replace character (r)
        elif key == "r":
            self.pending_command = "r"
            event.prevent_default()

        # Undo/redo
        elif key == "u":
            self.action_undo()
            event.prevent_default()
        elif key == "ctrl+r":
            self.action_redo()
            event.prevent_default()

        # === SEARCH ===

        # Find character (f/F/t/T)
        elif key == "f":
            self.pending_command = "f"
            event.prevent_default()
        elif key == "F":
            self.pending_command = "F"
            event.prevent_default()
        elif key == "t":
            self.pending_command = "t"
            event.prevent_default()
        elif key == "T":
            self.pending_command = "T"
            event.prevent_default()

    def _handle_pending_command(self, event):
        """Handle second key of multi-key commands (dd, yy, gg, etc.)."""
        key = event.key
        pending = self.pending_command

        # dd - delete line
        if pending == "d" and key == "d":
            self._delete_line()

        # yy - yank line
        elif pending == "y" and key == "y":
            self._yank_line()

        # gg - go to top
        elif pending == "g" and key == "g":
            self._move_to_start_of_document()

        # r{char} - replace character
        elif pending == "r":
            self._replace_character(key)

        # f{char} - find character forward
        elif pending == "f":
            self._find_character_forward(key)

        # F{char} - find character backward
        elif pending == "F":
            self._find_character_backward(key)

        # t{char} - till character forward
        elif pending == "t":
            self._till_character_forward(key)

        # T{char} - till character backward
        elif pending == "T":
            self._till_character_backward(key)

        # Clear pending command
        self.pending_command = None

    # === VISUAL MODE ===

    def _handle_visual_mode(self, event):
        """Handle keys in visual mode."""
        key = event.key

        # Navigation extends selection
        if key == "h":
            self.action_cursor_left_select()
            event.prevent_default()
        elif key == "j":
            self.action_cursor_down_select()
            event.prevent_default()
        elif key == "k":
            self.action_cursor_up_select()
            event.prevent_default()
        elif key == "l":
            self.action_cursor_right_select()
            event.prevent_default()

        # Word movement with selection
        elif key == "w":
            self.action_cursor_word_right_select()
            event.prevent_default()
        elif key == "b":
            self.action_cursor_word_left_select()
            event.prevent_default()

        # Yank selection
        elif key == "y":
            self._yank_selection()
            self._enter_command_mode()
            event.prevent_default()

        # Delete selection
        elif key == "d" or key == "x":
            self._delete_selection()
            self._enter_command_mode()
            event.prevent_default()

    # === VIM OPERATIONS ===

    def _delete_line(self):
        """Delete current line (dd)."""
        # Get current line text
        cursor = self.cursor_location
        line_text = self.get_line(cursor[0])

        # Save to yank register
        self.yank_register = line_text

        # Delete line using TextArea action
        self.action_delete_line()

    def _yank_line(self):
        """Yank (copy) current line (yy)."""
        cursor = self.cursor_location
        line_text = self.get_line(cursor[0])
        self.yank_register = line_text

    def _paste_after(self):
        """Paste after cursor (p)."""
        if self.yank_register:
            # Move cursor right, then insert
            self.action_cursor_right()
            self.insert(self.yank_register)

    def _paste_before(self):
        """Paste before cursor (P)."""
        if self.yank_register:
            self.insert(self.yank_register)

    def _yank_selection(self):
        """Yank (copy) selected text."""
        if self.selected_text:
            self.yank_register = self.selected_text

    def _delete_selection(self):
        """Delete selected text."""
        if self.selected_text:
            self.yank_register = self.selected_text
            self.action_delete()

    def _replace_character(self, char: str):
        """Replace character under cursor (r{char})."""
        # Delete current character
        self.action_delete_right()
        # Insert new character
        self.insert(char)
        # Stay in command mode (don't move cursor)
        self.action_cursor_left()

    def _open_line_below(self):
        """Open new line below current line (o)."""
        self.action_cursor_line_end()
        self.insert("\n")

    def _open_line_above(self):
        """Open new line above current line (O)."""
        self.action_cursor_line_start()
        self.insert("\n")
        self.action_cursor_up()

    def _move_to_word_end(self):
        """Move to end of word (e)."""
        # TextArea doesn't have word_end, approximate with word_right then back
        self.action_cursor_word_right()
        self.action_cursor_left()

    def _move_to_first_non_whitespace(self):
        """Move to first non-whitespace character (^)."""
        # For now, just go to line start
        # TODO: Could enhance to skip whitespace
        self.action_cursor_line_start()

    def _move_to_start_of_document(self):
        """Move to start of document (gg)."""
        # Move to document start using built-in action
        self.cursor_location = (0, 0)

    def _move_to_end_of_document(self):
        """Move to end of document (G)."""
        # Move to last line
        line_count = self.document.line_count
        self.cursor_location = (line_count - 1, 0)

    def _find_character_forward(self, char: str):
        """Find character forward (f{char})."""
        # Store for repeat with ; or ,
        self.last_f_search = ("f", char)

        # Get current line
        cursor = self.cursor_location
        line = self.get_line(cursor[0])

        # Search for character after cursor
        col = cursor[1]
        if col + 1 < len(line):
            idx = line.find(char, col + 1)
            if idx != -1:
                self.cursor_location = (cursor[0], idx)

    def _find_character_backward(self, char: str):
        """Find character backward (F{char})."""
        self.last_f_search = ("F", char)

        # Get current line
        cursor = self.cursor_location
        line = self.get_line(cursor[0])

        # Search for character before cursor
        col = cursor[1]
        if col > 0:
            idx = line.rfind(char, 0, col)
            if idx != -1:
                self.cursor_location = (cursor[0], idx)

    def _till_character_forward(self, char: str):
        """Till character forward (t{char})."""
        self.last_f_search = ("t", char)

        # Find character, then move back one
        cursor_before = self.cursor_location
        self._find_character_forward(char)
        cursor_after = self.cursor_location

        # If we moved, go back one
        if cursor_after != cursor_before:
            self.action_cursor_left()

    def _till_character_backward(self, char: str):
        """Till character backward (T{char})."""
        self.last_f_search = ("T", char)

        # Find character, then move forward one
        cursor_before = self.cursor_location
        self._find_character_backward(char)
        cursor_after = self.cursor_location

        # If we moved, go forward one
        if cursor_after != cursor_before:
            self.action_cursor_right()
