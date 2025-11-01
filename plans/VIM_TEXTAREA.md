# VimTextArea Widget - Implementation Guide

**Component**: Custom Textual widget with vim keybindings and modes
**Base Class**: `textual.widgets.TextArea`
**Estimated Effort**: 10-14 days
**Status**: Design phase

---

## Overview

VimTextArea is a custom Textual widget that extends `TextArea` to provide vim-like editing capabilities with modal editing (insert, command, visual modes) and vim keybindings.

### Design Principles

1. **Extend, don't replace** - Build on TextArea's solid foundation
2. **Mode-based behavior** - Different key handling based on vim mode
3. **Visual feedback** - Clear indication of current mode
4. **Textual patterns** - Follow Textual's widget patterns and conventions
5. **Testable** - Unit testable behavior for all vim operations

---

## Architecture

### Class Hierarchy

```
Widget (Textual)
  └── TextArea (Textual)
        └── VimTextArea (Our custom widget)
```

### Component Structure

```
textbox/
├── vim_textarea.py          # Main VimTextArea widget
├── vim_modes.py             # VimMode enum and mode state
├── vim_operations.py        # Vim command implementations
└── vim_keymaps.py           # Key mapping configurations
```

---

## Core Components

### 1. VimMode Enum

```python
# textbox/vim_modes.py

from enum import Enum

class VimMode(Enum):
    """Vim editing modes."""
    INSERT = "INSERT"
    COMMAND = "COMMAND"
    VISUAL = "VISUAL"
    VISUAL_LINE = "VISUAL_LINE"  # For future

class ModeIndicator:
    """Helper for mode display."""

    @staticmethod
    def get_display(mode: VimMode) -> str:
        """Get display string for mode."""
        return {
            VimMode.INSERT: "-- INSERT --",
            VimMode.COMMAND: "",  # Command mode shows nothing (vim default)
            VimMode.VISUAL: "-- VISUAL --",
            VimMode.VISUAL_LINE: "-- VISUAL LINE --",
        }[mode]

    @staticmethod
    def get_border_style(mode: VimMode) -> str:
        """Get CSS class for mode."""
        return {
            VimMode.INSERT: "insert-mode",
            VimMode.COMMAND: "command-mode",
            VimMode.VISUAL: "visual-mode",
            VimMode.VISUAL_LINE: "visual-line-mode",
        }[mode]
```

### 2. VimTextArea Widget

```python
# textbox/vim_textarea.py

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
        self.pending_command = None  # For dd, yy, etc.
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

        # Handle pending commands first (dd, yy, etc.)
        if self.pending_command:
            self._handle_pending_command(event)
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
            event.prevent_default()

        # yy - yank line
        elif pending == "y" and key == "y":
            self._yank_line()
            event.prevent_default()

        # gg - go to top
        elif pending == "g" and key == "g":
            self._move_to_start_of_document()
            event.prevent_default()

        # r{char} - replace character
        elif pending == "r":
            self._replace_character(key)
            event.prevent_default()

        # f{char} - find character forward
        elif pending == "f":
            self._find_character_forward(key)
            event.prevent_default()

        # F{char} - find character backward
        elif pending == "F":
            self._find_character_backward(key)
            event.prevent_default()

        # t{char} - till character forward
        elif pending == "t":
            self._till_character_forward(key)
            event.prevent_default()

        # T{char} - till character backward
        elif pending == "T":
            self._till_character_backward(key)
            event.prevent_default()

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
            self.action_delete_to_start_of_line()  # Or appropriate delete action

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
        self.action_cursor_line_start()
        # Skip whitespace (would need TextArea API support)
        # For now, just go to line start

    def _move_to_start_of_document(self):
        """Move to start of document (gg)."""
        # TextArea has this action
        self.action_cursor_document_start()

    def _move_to_end_of_document(self):
        """Move to end of document (G)."""
        self.action_cursor_document_end()

    def _find_character_forward(self, char: str):
        """Find character forward (f{char})."""
        # Would need to search current line for character
        # Store for repeat with ; or ,
        self.last_f_search = ("f", char)
        # Implementation depends on TextArea API

    def _find_character_backward(self, char: str):
        """Find character backward (F{char})."""
        self.last_f_search = ("F", char)
        # Implementation depends on TextArea API

    def _till_character_forward(self, char: str):
        """Till character forward (t{char})."""
        self.last_f_search = ("t", char)
        # Find, then move back one

    def _till_character_backward(self, char: str):
        """Till character backward (T{char})."""
        self.last_f_search = ("T", char)
        # Find, then move forward one
```

---

## TextArea Actions Available

Textual's TextArea provides these built-in actions we can use:

### Cursor Movement
- `action_cursor_left()`
- `action_cursor_right()`
- `action_cursor_up()`
- `action_cursor_down()`
- `action_cursor_word_left()`
- `action_cursor_word_right()`
- `action_cursor_line_start()`
- `action_cursor_line_end()`
- `action_cursor_page_up()`
- `action_cursor_page_down()`
- `action_cursor_document_start()`  # For gg
- `action_cursor_document_end()`    # For G

### Selection (for visual mode)
- `action_cursor_left_select()`
- `action_cursor_right_select()`
- `action_cursor_up_select()`
- `action_cursor_down_select()`
- `action_cursor_word_left_select()`
- `action_cursor_word_right_select()`
- `action_select_all()`

### Editing
- `action_delete_left()` (backspace)
- `action_delete_right()` (delete)
- `action_delete_line()`
- `action_delete_to_start_of_line()`
- `action_delete_to_end_of_line()`
- `action_delete_word_left()`
- `action_delete_word_right()`

### Undo/Redo
- `action_undo()`
- `action_redo()`

### Properties
- `text` - full document text
- `selected_text` - currently selected text
- `cursor_location` - (row, column) tuple
- `selection` - Selection object

---

## Testing Strategy

### Unit Tests

```python
# tests/test_vim_textarea.py

import pytest
from textual.app import App
from textbox import VimTextArea, VimMode

@pytest.fixture
async def vim_widget():
    """Create VimTextArea widget for testing."""
    app = App()
    async with app.run_test() as pilot:
        widget = VimTextArea()
        await pilot.app.mount(widget)
        yield widget

class TestVimModes:
    """Test mode switching."""

    async def test_starts_in_insert_mode(self, vim_widget):
        assert vim_widget.vim_mode == VimMode.INSERT

    async def test_escape_enters_command_mode(self, vim_widget):
        await vim_widget.press("escape")
        assert vim_widget.vim_mode == VimMode.COMMAND

    async def test_i_enters_insert_mode(self, vim_widget):
        await vim_widget.press("escape")  # Command mode
        await vim_widget.press("i")
        assert vim_widget.vim_mode == VimMode.INSERT

    async def test_v_enters_visual_mode(self, vim_widget):
        await vim_widget.press("escape")  # Command mode
        await vim_widget.press("v")
        assert vim_widget.vim_mode == VimMode.VISUAL

class TestCommandMode:
    """Test command mode navigation."""

    async def test_hjkl_navigation(self, vim_widget):
        vim_widget.text = "hello\nworld"
        await vim_widget.press("escape")

        # Test h (left)
        vim_widget.cursor_location = (0, 3)
        await vim_widget.press("h")
        assert vim_widget.cursor_location == (0, 2)

        # Test j (down)
        await vim_widget.press("j")
        assert vim_widget.cursor_location[0] == 1

        # Test k (up)
        await vim_widget.press("k")
        assert vim_widget.cursor_location[0] == 0

        # Test l (right)
        await vim_widget.press("l")
        assert vim_widget.cursor_location == (0, 3)

    async def test_word_navigation(self, vim_widget):
        vim_widget.text = "hello world foo bar"
        await vim_widget.press("escape")
        vim_widget.cursor_location = (0, 0)

        # Test w (next word)
        await vim_widget.press("w")
        assert vim_widget.cursor_location[1] == 6  # Start of "world"

        # Test b (previous word)
        await vim_widget.press("b")
        assert vim_widget.cursor_location[1] == 0  # Start of "hello"

    async def test_line_navigation(self, vim_widget):
        vim_widget.text = "  hello world  "
        await vim_widget.press("escape")
        vim_widget.cursor_location = (0, 5)

        # Test 0 (line start)
        await vim_widget.press("0")
        assert vim_widget.cursor_location[1] == 0

        # Test $ (line end)
        await vim_widget.press("dollar")
        assert vim_widget.cursor_location[1] == len(vim_widget.text) - 1

class TestEditing:
    """Test editing operations."""

    async def test_x_deletes_character(self, vim_widget):
        vim_widget.text = "hello"
        await vim_widget.press("escape")
        vim_widget.cursor_location = (0, 1)  # On 'e'

        await vim_widget.press("x")
        assert vim_widget.text == "hllo"

    async def test_dd_deletes_line(self, vim_widget):
        vim_widget.text = "line1\nline2\nline3"
        await vim_widget.press("escape")
        vim_widget.cursor_location = (1, 0)  # On line2

        await vim_widget.press("d")
        await vim_widget.press("d")
        assert "line2" not in vim_widget.text
        assert "line1\nline3" in vim_widget.text

    async def test_yy_and_p_copy_paste(self, vim_widget):
        vim_widget.text = "hello"
        await vim_widget.press("escape")

        # Yank line
        await vim_widget.press("y")
        await vim_widget.press("y")

        # Paste
        await vim_widget.press("p")
        assert "hello" in vim_widget.text
        # (exact assertion depends on paste behavior)

class TestVisualMode:
    """Test visual mode selection."""

    async def test_visual_mode_selection(self, vim_widget):
        vim_widget.text = "hello world"
        await vim_widget.press("escape")
        vim_widget.cursor_location = (0, 0)

        # Enter visual mode
        await vim_widget.press("v")
        assert vim_widget.vim_mode == VimMode.VISUAL

        # Select 5 characters
        for _ in range(5):
            await vim_widget.press("l")

        # Delete selection
        await vim_widget.press("d")
        assert vim_widget.text == " world"
```

---

## Implementation Phases

### Phase 1A: Basic Structure (2 days)

**Goal**: VimTextArea widget exists with mode tracking

**Tasks**:
- [ ] Create `vim_modes.py` with VimMode enum
- [ ] Create `vim_textarea.py` with VimTextArea class
- [ ] Extend TextArea
- [ ] Add mode tracking (insert/command)
- [ ] Add CSS for mode-based borders
- [ ] Mode change events

**Tests**:
- [ ] Widget creation
- [ ] Mode initialization (starts in INSERT)
- [ ] ESC switches to COMMAND
- [ ] Mode change events fire

### Phase 1B: Basic Navigation (3 days)

**Goal**: hjkl, 0, $, gg, G work in command mode

**Tasks**:
- [ ] Implement hjkl (cursor movement)
- [ ] Implement 0 and $ (line start/end)
- [ ] Implement gg and G (document start/end)
- [ ] Handle pending commands (gg requires two keys)

**Tests**:
- [ ] hjkl navigation
- [ ] 0 and $ navigation
- [ ] gg and G navigation
- [ ] Navigation only works in command mode

### Phase 1C: Mode Switching (2 days)

**Goal**: i, a, I, A, o, O enter insert mode correctly

**Tasks**:
- [ ] Implement i (insert at cursor)
- [ ] Implement a (append after cursor)
- [ ] Implement I (insert at line start)
- [ ] Implement A (append at line end)
- [ ] Implement o (open line below)
- [ ] Implement O (open line above)

**Tests**:
- [ ] Each command enters insert mode
- [ ] Cursor position correct after each command
- [ ] Can type in insert mode

**Milestone**: Basic vim navigation and mode switching works

---

### Phase 2A: Word Navigation (2 days)

**Goal**: w, b, e word motions work

**Tasks**:
- [ ] Implement w (next word start)
- [ ] Implement b (previous word start)
- [ ] Implement e (word end)
- [ ] Test with various text (spaces, punctuation)

**Tests**:
- [ ] w navigates to next word
- [ ] b navigates to previous word
- [ ] e navigates to word end
- [ ] Edge cases (beginning/end of line)

### Phase 2B: Editing Operations (3 days)

**Goal**: x, dd, yy, p work

**Tasks**:
- [ ] Implement x (delete character)
- [ ] Implement X (delete left)
- [ ] Implement dd (delete line)
- [ ] Implement yy (yank line)
- [ ] Implement p (paste after)
- [ ] Implement P (paste before)
- [ ] Yank register management

**Tests**:
- [ ] x deletes character
- [ ] dd deletes line
- [ ] yy + p copies and pastes
- [ ] Multiple dd/yy operations
- [ ] Paste at various positions

### Phase 2C: Visual Mode (3-4 days)

**Goal**: Visual selection works

**Tasks**:
- [ ] Implement v (enter visual mode)
- [ ] Navigation extends selection (hjkl, w, b)
- [ ] Implement y (yank selection)
- [ ] Implement d (delete selection)
- [ ] Visual feedback (highlight selection)

**Tests**:
- [ ] Visual mode activates
- [ ] Selection extends with navigation
- [ ] Yank and delete work on selection
- [ ] ESC exits visual mode

**Milestone**: Complete basic vim editing

---

### Phase 3: Advanced Features (Optional, 2-3 days)

**Goal**: Additional vim niceties

**Tasks**:
- [ ] Implement r (replace character)
- [ ] Implement f/F/t/T (find character)
- [ ] Implement ; and , (repeat find)
- [ ] Implement ^ (first non-whitespace)
- [ ] Implement Ctrl+d/Ctrl+u (page down/up)

---

## Integration Example

### Using VimTextArea in a Chat App

```python
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, RichLog
from textbox import VimTextArea

class ChatApp(App):
    """Chat with vim input."""

    CSS = """
    #output {
        height: 1fr;
    }

    #input {
        height: auto;
        max-height: 10;
    }

    Footer {
        background: $panel;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield RichLog(id="output")
        yield VimTextArea(id="input")
        yield Footer()

    def on_mount(self):
        """Initialize on mount."""
        self.query_one("#input").focus()
        self.update_footer()

    async def on_vim_text_area_mode_changed(self, event):
        """Update footer when vim mode changes."""
        self.update_footer()

    async def on_vim_text_area_submitted(self, event):
        """Handle message submission."""
        output = self.query_one("#output")
        output.write(f"[cyan]You:[/cyan] {event.text}")

        # Stream response
        output.write("[green]AI:[/green] ", end="")
        async for token in self.get_ai_response(event.text):
            output.write(token, end="")
        output.write("")

    def update_footer(self):
        """Update footer with vim mode."""
        input_widget = self.query_one("#input")
        mode_text = ModeIndicator.get_display(input_widget.vim_mode)
        # Update footer text (Textual API)
        # self.query_one(Footer).update(mode_text)

    async def get_ai_response(self, prompt: str):
        """Get AI response (placeholder)."""
        import asyncio
        for word in prompt.split():
            yield word + " "
            await asyncio.sleep(0.1)

if __name__ == "__main__":
    app = ChatApp()
    app.run()
```

---

## Known Limitations

### TextArea Constraints

Some vim features may be difficult due to TextArea limitations:

1. **Character search (f/t)** - No API to search within line
2. **Marks** - No API to set/jump to marks
3. **Macros** - No macro recording system
4. **Registers** - Only one yank register (no named registers)
5. **Text objects** - No `diw` (delete inner word) etc.

**Mitigation**: Focus on most-used features first, add advanced features if TextArea API allows.

---

## Success Criteria

### Phase 1 Complete (Basic Vim)
- [ ] Insert/command modes work
- [ ] hjkl navigation
- [ ] Mode switching (i, a, ESC)
- [ ] Visual feedback (border colors)
- [ ] Mode indicator
- [ ] All basic tests pass

### Phase 2 Complete (Advanced Vim)
- [ ] Word motions (w, b, e)
- [ ] Editing (x, dd, yy, p)
- [ ] Visual mode
- [ ] Undo/redo
- [ ] All tests pass

### Production Ready
- [ ] 80%+ test coverage
- [ ] Documentation complete
- [ ] Examples work
- [ ] No known critical bugs
- [ ] Feels natural to use

---

## Next Steps

1. **Review this design** - Approve approach
2. **Start Phase 1A** - Basic structure
3. **Iterate** - Build incrementally with tests

See [IMPLEMENTATION.md](IMPLEMENTATION.md) for detailed day-by-day plan.
