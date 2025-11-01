"""VimTextArea - TextArea with vim keybindings and modes.

This module provides the main VimTextArea widget that combines all vim operations
through mixins for better code organization.
"""

from textual.widgets import TextArea
from textual.message import Message
from textual.reactive import reactive
from .vim_modes import VimMode, ModeIndicator
from .operations import NavigationMixin, EditingMixin, VisualMixin, SearchMixin, TextObjectMixin
from .count_handler import CountHandler
from .marks import MarksManager
from .operator_pending import OperatorPendingState, OperatorMotionHandler


class VimTextArea(NavigationMixin, EditingMixin, VisualMixin, SearchMixin, TextObjectMixin, TextArea):
    """TextArea with vim keybindings and modal editing.

    This widget extends Textual's TextArea to provide vim-style modal editing with:
    - INSERT, COMMAND, and VISUAL modes
    - Complete vim navigation (hjkl, w/b/e, 0/$, gg/G, etc.)
    - Line operations (dd, yy, p, P)
    - Visual selection with operations
    - Character search (f, t, F, T)
    - Count support (5j, 3dd, 2w, etc.) [Phase 2]
    - Text objects (diw, ci", da(, etc.) [Phase 2]
    - Marks (ma, 'a, `a) [Phase 2]
    - Undo/redo support

    The implementation uses mixins for organization:
    - NavigationMixin: Cursor movement operations
    - EditingMixin: Text editing operations
    - VisualMixin: Visual mode operations
    - SearchMixin: Character and word search
    - TextObjectMixin: Text object operations [Phase 2]
    """

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
        self.last_f_search = None  # For f/t commands (type, char)
        self.last_search_word = None  # For * and # searches
        self.yank_register = ""  # Copied text

        # Phase 2 features
        self.count_handler = CountHandler()  # For number prefixes (5j, 3dd)
        self.marks_manager = MarksManager()  # For marks (ma, 'a, `a)
        self.text_object_state = None  # For pending text object operations (d + i + w)
        self.operator_pending = OperatorPendingState()  # For operator + motion (dw, c$, y3w)

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

    # === KEY EVENT ROUTING ===

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
        self.pending_command = None
        self.count_handler.clear()  # Clear any pending count
        self.text_object_state = None  # Clear text object state
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

        # Handle number input for counts (5j, 3dd, etc.)
        if key.isdigit():
            # If we're in operator-pending mode, this is motion count (d3w)
            if self.operator_pending.is_pending():
                self.operator_pending.set_motion_count(
                    self.operator_pending.motion_count * 10 + int(key)
                )
            else:
                self.count_handler.add_digit(key)
            event.prevent_default()
            return

        # Handle operator-pending mode (dw, c$, y3j, etc.)
        if self.operator_pending.is_pending():
            if self._handle_operator_motion(event):
                event.prevent_default()
                return

        # Handle pending commands first (dd, yy, gg, etc.)
        if self.pending_command:
            self._handle_pending_command(event)
            event.prevent_default()
            return

        # === NAVIGATION ===

        # Basic movement (hjkl) - with count support
        if key == "h":
            count = self.count_handler.get_count()
            for _ in range(count):
                self.nav_left()
            self.count_handler.clear()
            event.prevent_default()
        elif key == "j":
            count = self.count_handler.get_count()
            for _ in range(count):
                self.nav_down()
            self.count_handler.clear()
            event.prevent_default()
        elif key == "k":
            count = self.count_handler.get_count()
            for _ in range(count):
                self.nav_up()
            self.count_handler.clear()
            event.prevent_default()
        elif key == "l":
            count = self.count_handler.get_count()
            for _ in range(count):
                self.nav_right()
            self.count_handler.clear()
            event.prevent_default()

        # Word movement - with count support
        elif key == "w":
            count = self.count_handler.get_count()
            for _ in range(count):
                self.nav_word_forward()
            self.count_handler.clear()
            event.prevent_default()
        elif key == "b":
            count = self.count_handler.get_count()
            for _ in range(count):
                self.nav_word_backward()
            self.count_handler.clear()
            event.prevent_default()
        elif key == "e":
            count = self.count_handler.get_count()
            for _ in range(count):
                self.nav_word_end()
            self.count_handler.clear()
            event.prevent_default()

        # Line movement
        elif key == "0":
            self.nav_line_start()
            event.prevent_default()
        elif key == "dollar":  # $
            self.nav_line_end()
            event.prevent_default()
        elif key == "circumflex":  # ^
            self.nav_first_non_whitespace()
            event.prevent_default()

        # Document movement
        elif key == "g":
            self.pending_command = "g"
            event.prevent_default()
        elif key == "G":  # Shift+g
            self.nav_document_end()
            event.prevent_default()

        # Page movement
        elif key == "ctrl+d":
            self.nav_page_down()
            event.prevent_default()
        elif key == "ctrl+u":
            self.nav_page_up()
            event.prevent_default()

        # Paragraph movement
        elif key == "braceleft":  # {
            self.nav_paragraph_backward()
            event.prevent_default()
        elif key == "braceright":  # }
            self.nav_paragraph_forward()
            event.prevent_default()

        # === MODE CHANGES ===

        # Enter insert mode
        elif key == "i":
            self._enter_insert_mode()
            event.prevent_default()
        elif key == "I":  # Insert at line start
            self.nav_line_start()
            self._enter_insert_mode()
            event.prevent_default()
        elif key == "a":
            self.nav_right()
            self._enter_insert_mode()
            event.prevent_default()
        elif key == "A":  # Append at line end
            self.nav_line_end()
            self._enter_insert_mode()
            event.prevent_default()
        elif key == "o":  # Open line below
            self.edit_open_line_below()
            self._enter_insert_mode()
            event.prevent_default()
        elif key == "O":  # Open line above
            self.edit_open_line_above()
            self._enter_insert_mode()
            event.prevent_default()

        # Enter visual mode
        elif key == "v":
            self._enter_visual_mode()
            event.prevent_default()

        # === EDITING ===

        # Delete character
        elif key == "x":
            self.edit_delete_char()
            event.prevent_default()
        elif key == "X":  # Delete left
            self.edit_delete_char_back()
            event.prevent_default()

        # Delete/change/yank - enter operator-pending mode
        elif key == "d":
            count = self.count_handler.get_count(0)  # 0 means no count
            self.operator_pending.set_operator("d", count)
            self.count_handler.clear()
            event.prevent_default()
        elif key == "D":
            self.edit_delete_to_line_end()
            event.prevent_default()
        elif key == "c":
            count = self.count_handler.get_count(0)
            self.operator_pending.set_operator("c", count)
            self.count_handler.clear()
            event.prevent_default()
        elif key == "C":
            self.edit_delete_to_line_end()
            self._enter_insert_mode()
            event.prevent_default()

        # Yank - enter operator-pending mode
        elif key == "y":
            count = self.count_handler.get_count(0)
            self.operator_pending.set_operator("y", count)
            self.count_handler.clear()
            event.prevent_default()

        # Paste
        elif key == "p":
            self.edit_paste_after()
            event.prevent_default()
        elif key == "P":  # Paste before
            self.edit_paste_before()
            event.prevent_default()

        # Replace character (r)
        elif key == "r":
            self.pending_command = "r"
            event.prevent_default()

        # Join lines (J)
        elif key == "J":
            self.edit_join_lines()
            event.prevent_default()

        # Indent/dedent
        elif key == "greater_than":  # >
            self.pending_command = ">"
            event.prevent_default()
        elif key == "less_than":  # <
            self.pending_command = "<"
            event.prevent_default()

        # Undo/redo
        elif key == "u":
            self.edit_undo()
            event.prevent_default()
        elif key == "ctrl+r":
            self.edit_redo()
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

        # Repeat search
        elif key == "semicolon":  # ;
            self.search_repeat()
            event.prevent_default()
        elif key == "comma":  # ,
            self.search_repeat_reverse()
            event.prevent_default()

        # Word search
        elif key == "asterisk":  # *
            self.search_word_under_cursor(forward=True)
            event.prevent_default()
        elif key == "numbersign":  # #
            self.search_word_under_cursor(forward=False)
            event.prevent_default()

    def _handle_operator_motion(self, event) -> bool:
        """Handle motion key when in operator-pending mode.

        Args:
            event: Key event

        Returns:
            True if motion was handled
        """
        key = event.key
        operator = self.operator_pending.get_operator()

        # Handle same operator (dd, yy, cc) - line-wise operation
        if key == operator:
            count = self.operator_pending.get_total_count()
            success = OperatorMotionHandler.execute_line_operator(self, operator, count)
            self.operator_pending.clear()
            return success

        # Map keys to motion functions
        motion_map = {
            'h': self.nav_left,
            'j': self.nav_down,
            'k': self.nav_up,
            'l': self.nav_right,
            'w': self.nav_word_forward,
            'b': self.nav_word_backward,
            'e': self.nav_word_end,
            '0': self.nav_line_start,
            'dollar': self.nav_line_end,  # $
            'circumflex': self.nav_first_non_whitespace,  # ^
        }

        if key in motion_map:
            count = self.operator_pending.get_total_count()
            success = OperatorMotionHandler.execute_operator_motion(
                self, operator, motion_map[key], count
            )
            self.operator_pending.clear()
            return success

        # ESC cancels operator-pending
        if key == "escape":
            self.operator_pending.clear()
            return True

        return False

    def _handle_pending_command(self, event):
        """Handle second key of multi-key commands (dd, yy, gg, etc.)."""
        key = event.key
        pending = self.pending_command

        # dd - delete line
        if pending == "d" and key == "d":
            self.edit_delete_line()

        # dw - delete word
        elif pending == "d" and key == "w":
            self.edit_delete_word()

        # yy - yank line
        elif pending == "y" and key == "y":
            self.edit_yank_line()

        # cc - change line
        elif pending == "c" and key == "c":
            self.edit_change_line()

        # cw - change word
        elif pending == "c" and key == "w":
            self.edit_change_word()

        # gg - go to top
        elif pending == "g" and key == "g":
            self.nav_document_start()

        # >> - indent
        elif pending == ">" and key == "greater_than":
            self.edit_indent()

        # << - dedent
        elif pending == "<" and key == "less_than":
            self.edit_dedent()

        # r{char} - replace character
        elif pending == "r":
            self.edit_replace_char(key)

        # f{char} - find character forward
        elif pending == "f":
            self.search_char_forward(key)

        # F{char} - find character backward
        elif pending == "F":
            self.search_char_backward(key)

        # t{char} - till character forward
        elif pending == "t":
            self.search_till_forward(key)

        # T{char} - till character backward
        elif pending == "T":
            self.search_till_backward(key)

        # Clear pending command
        self.pending_command = None

    # === VISUAL MODE ===

    def _handle_visual_mode(self, event):
        """Handle keys in visual mode."""
        key = event.key

        # Navigation extends selection
        if key == "h":
            self.visual_left()
            event.prevent_default()
        elif key == "j":
            self.visual_down()
            event.prevent_default()
        elif key == "k":
            self.visual_up()
            event.prevent_default()
        elif key == "l":
            self.visual_right()
            event.prevent_default()

        # Word movement with selection
        elif key == "w":
            self.visual_word_forward()
            event.prevent_default()
        elif key == "b":
            self.visual_word_backward()
            event.prevent_default()

        # Line movement with selection
        elif key == "0":
            self.visual_line_start()
            event.prevent_default()
        elif key == "dollar":  # $
            self.visual_line_end()
            event.prevent_default()

        # Yank selection
        elif key == "y":
            self.visual_yank()
            self._enter_command_mode()
            event.prevent_default()

        # Delete selection
        elif key == "d" or key == "x":
            self.visual_delete()
            self._enter_command_mode()
            event.prevent_default()

        # Change selection
        elif key == "c":
            self.visual_change()
            event.prevent_default()

        # Indent/dedent selection
        elif key == "greater_than":  # >
            self.visual_indent()
            event.prevent_default()
        elif key == "less_than":  # <
            self.visual_dedent()
            event.prevent_default()

        # Case operations
        elif key == "tilde":  # ~
            self.visual_toggle_case()
            event.prevent_default()
        elif key == "u":
            self.visual_lowercase()
            event.prevent_default()
        elif key == "U":
            self.visual_uppercase()
            event.prevent_default()
