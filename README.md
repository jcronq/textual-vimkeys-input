# VimKeys Input

A comprehensive Vim-style modal editing widget for [Textual](https://textual.textualize.io/), bringing the power of Vim keybindings to your terminal applications.

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Textual Version](https://img.shields.io/badge/textual-0.47%2B-purple.svg)](https://textual.textualize.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

### Core Vim Functionality
- **Modal Editing**: Full INSERT, COMMAND, and VISUAL mode support
- **Operator + Motion System**: Complete implementation of vim's composable commands (e.g., `dw`, `c$`, `y3j`)
- **Count Support**: Numeric prefixes for commands (e.g., `5j`, `3dd`, `2d3w`)
- **Text Objects**: Semantic editing with `iw`, `i"`, `i(`, `da{`, etc.
- **Marks**: Position bookmarks with `ma`, `'a`, `` `a ``
- **Visual Selection**: Character-wise selection with operators

### Navigation
- **Basic Movement**: `hjkl` for directional navigation
- **Word Motion**: `w`, `b`, `e` for word-based navigation
- **Line Navigation**: `0`, `$`, `^` for line start/end/first non-whitespace
- **Document Navigation**: `gg`, `G` for document start/end
- **Count Support**: All motions support counts (e.g., `5j`, `3w`)

### Editing
- **Delete**: `x`, `dd`, `d<motion>` (e.g., `dw`, `d$`, `d3e`)
- **Change**: `cc`, `c<motion>` (e.g., `cw`, `c$`, `cb`)
- **Yank (Copy)**: `yy`, `y<motion>` (e.g., `y3j`, `yw`)
- **Paste**: `p`, `P` for paste after/before cursor
- **Undo/Redo**: `u`, `Ctrl+r` with full history
- **Insert Modes**: `i`, `a`, `I`, `A`, `o`, `O` for various insert positions

### Advanced Features
- **Search**: `/` for forward search, `n`/`N` for next/previous
- **Replace**: `r` for single character replacement
- **Join Lines**: `J` to join current line with next
- **Visual Mode**: `v` for character-wise selection, operators work in visual mode
- **Case Change**: `~` to toggle case (planned)
- **Line Change**: `S`, `C` for line/tail change (planned)

### Visual Feedback
- **Mode Indicators**: Border colors change based on current mode
  - Green: INSERT mode
  - Blue: COMMAND mode
  - Yellow: VISUAL mode
- **CSS Customization**: Full control over mode styling via CSS classes

### Events
- **Submitted**: Fires when user presses Enter in INSERT mode
- **ModeChanged**: Fires whenever vim mode changes

## Installation

### From PyPI (when published)
```bash
pip install vimkeys-input
```

### From Source (Development)
```bash
# Clone the repository
git clone https://github.com/yourusername/vimkeys-input.git
cd vimkeys-input

# Using uv (recommended)
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"

# Or using pip
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Quick Start

### Basic Example

```python
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from vimkeys_input import VimTextArea

class MyApp(App):
    """A simple app with vim-style input."""

    def compose(self) -> ComposeResult:
        yield Header()
        yield VimTextArea(id="input")
        yield Footer()

    def on_vim_text_area_submitted(self, event: VimTextArea.Submitted):
        """Handle text submission."""
        self.notify(f"You entered: {event.text}")
        event.text_area.clear()

if __name__ == "__main__":
    app = MyApp()
    app.run()
```

### Chat Application Example

```python
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, RichLog
from textual.containers import Vertical
from vimkeys_input import VimTextArea

class ChatApp(App):
    """A chat application with vim-style input."""

    CSS = """
    #history {
        height: 1fr;
        border: solid $primary;
    }

    #input {
        height: auto;
        max-height: 10;
        margin: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield RichLog(id="history", markup=True, wrap=True)
            yield VimTextArea(id="input")
        yield Footer()

    def on_mount(self):
        history = self.query_one("#history", RichLog)
        history.write("Welcome to the chat!")

    def on_vim_text_area_submitted(self, event: VimTextArea.Submitted):
        if not event.text.strip():
            return

        history = self.query_one("#history", RichLog)
        history.write(f"[bold cyan]You:[/bold cyan] {event.text}")
        event.text_area.clear()

if __name__ == "__main__":
    app = ChatApp()
    app.run()
```

## Complete Keybinding Reference

### Mode Switching

| Key | Action | Description |
|-----|--------|-------------|
| `ESC` | Enter COMMAND mode | Exit INSERT/VISUAL mode |
| `i` | Insert at cursor | Enter INSERT mode at cursor |
| `a` | Append after cursor | Enter INSERT mode after cursor |
| `I` | Insert at line start | Enter INSERT mode at first non-whitespace |
| `A` | Append at line end | Enter INSERT mode at end of line |
| `o` | Open line below | Create new line below and enter INSERT mode |
| `O` | Open line above | Create new line above and enter INSERT mode |
| `v` | Visual mode | Enter character-wise VISUAL mode |

### Navigation (COMMAND Mode)

| Key | Action | Count Support | Description |
|-----|--------|---------------|-------------|
| `h` | Left | ✓ | Move cursor left |
| `j` | Down | ✓ | Move cursor down |
| `k` | Up | ✓ | Move cursor up |
| `l` | Right | ✓ | Move cursor right |
| `w` | Next word | ✓ | Move to start of next word |
| `b` | Previous word | ✓ | Move to start of previous word |
| `e` | End of word | ✓ | Move to end of current/next word |
| `0` | Line start | - | Move to beginning of line |
| `$` | Line end | - | Move to end of line |
| `^` | First non-blank | - | Move to first non-whitespace character |
| `gg` | Document start | - | Move to first line |
| `G` | Document end | - | Move to last line |

### Operators (COMMAND Mode)

Operators can be combined with motions and counts for powerful editing:

| Operator | Description | Example | Result |
|----------|-------------|---------|--------|
| `d` | Delete | `dw` | Delete word |
| | | `d$` | Delete to end of line |
| | | `d3j` | Delete 3 lines down |
| | | `dd` | Delete current line |
| `c` | Change (delete + INSERT) | `cw` | Change word |
| | | `c$` | Change to end of line |
| | | `cb` | Change previous word |
| | | `cc` | Change entire line |
| `y` | Yank (copy) | `yw` | Yank word |
| | | `y$` | Yank to end of line |
| | | `y3j` | Yank 3 lines down |
| | | `yy` | Yank current line |

### Text Objects (COMMAND Mode)

Use with operators for semantic editing:

| Text Object | Description | Example | Result |
|-------------|-------------|---------|--------|
| `iw` | Inner word | `diw` | Delete word under cursor |
| `aw` | A word (with space) | `daw` | Delete word + surrounding space |
| `i"` | Inside quotes | `di"` | Delete text inside quotes |
| `a"` | Around quotes | `da"` | Delete text + quotes |
| `i(` / `i)` | Inside parens | `di(` | Delete text inside parentheses |
| `a(` / `a)` | Around parens | `da(` | Delete text + parentheses |
| `i{` / `i}` | Inside braces | `di{` | Delete text inside braces |
| `a{` / `a}` | Around braces | `da{` | Delete text + braces |
| `i[` / `i]` | Inside brackets | `di[` | Delete text inside brackets |
| `a[` / `a]` | Around brackets | `da[` | Delete text + brackets |

### Editing (COMMAND Mode)

| Key | Action | Count Support | Description |
|-----|--------|---------------|-------------|
| `x` | Delete char | ✓ | Delete character under cursor |
| `r` | Replace char | - | Replace character under cursor |
| `p` | Paste after | ✓ | Paste after cursor/line |
| `P` | Paste before | ✓ | Paste before cursor/line |
| `u` | Undo | - | Undo last change |
| `Ctrl+r` | Redo | - | Redo last undone change |
| `J` | Join lines | - | Join current line with next |
| `~` | Toggle case | ✓ | Toggle case of character(s) |

### Search (COMMAND Mode)

| Key | Action | Description |
|-----|--------|-------------|
| `/` | Search forward | Enter search pattern |
| `n` | Next match | Jump to next search result |
| `N` | Previous match | Jump to previous search result |

### Marks (COMMAND Mode)

| Key | Action | Description |
|-----|--------|-------------|
| `m{a-z}` | Set mark | Set mark at cursor position (e.g., `ma`) |
| `'{a-z}` | Jump to mark line | Jump to line of mark (e.g., `'a`) |
| `` `{a-z} `` | Jump to mark pos | Jump to exact position of mark (e.g., `` `a ``) |

### Visual Mode

| Key | Action | Description |
|-----|--------|-------------|
| `v` | Enter visual | Start character-wise selection |
| `h/j/k/l` | Extend selection | Extend selection with movement |
| `w/b/e` | Extend by word | Extend selection by words |
| `d` | Delete selection | Delete selected text |
| `c` | Change selection | Delete selected text and enter INSERT |
| `y` | Yank selection | Copy selected text |
| `ESC` | Exit visual | Return to COMMAND mode |

### Count System

Vim counts work in multiple ways:

```
{count}{motion}     Example: 5j (move down 5 lines)
{count}{operator}   Example: 3dd (delete 3 lines)
{operator}{count}{motion}   Example: d3w (delete 3 words)
{count1}{operator}{count2}{motion}   Example: 2d3w (delete 6 words total)
```

### INSERT Mode

| Key | Action | Description |
|-----|--------|-------------|
| `Enter` | Submit | Fire Submitted event (customizable) |
| `ESC` | Exit INSERT | Return to COMMAND mode |
| All standard keys | Insert text | Normal text input |
| Arrow keys, Backspace, Delete, etc. | Edit | Standard editing operations |

## Examples

The package includes several example applications demonstrating different use cases:

### 01_spike.py - Basic Functionality
```bash
uv run python examples/01_spike.py
```
Demonstrates basic vim modal editing with a simple text input.

### 02_simple_chat.py - Chat Bot
```bash
uv run python examples/02_simple_chat.py
```
A simple chat bot application showing how to integrate VimTextArea in a conversational UI.

### 03_streaming_chat.py - Advanced Chat
```bash
uv run python examples/03_streaming_chat.py
```
An advanced chat application featuring:
- Token-by-token streaming responses
- Animated "thinking" indicator
- Input history navigation (up/down arrows)
- Text wrapping
- Command palette integration

## API Reference

### VimTextArea

The main widget class extending Textual's `TextArea`.

#### Constructor

```python
VimTextArea(
    text: str = "",
    language: str | None = None,
    theme: str = "css",
    *,
    id: str | None = None,
    classes: str | None = None,
)
```

All parameters from Textual's `TextArea` are supported.

#### Properties

```python
@property
def mode(self) -> VimMode:
    """Get current vim mode."""

@mode.setter
def mode(self, new_mode: VimMode) -> None:
    """Set vim mode and update visual feedback."""

@property
def yank_register(self) -> str:
    """Get contents of yank (copy) register."""
```

#### Methods

```python
def clear(self) -> None:
    """Clear the text area and reset to INSERT mode."""

def get_line(self, row: int) -> Text:
    """Get the text content of a specific line."""

def set_cursor(self, row: int, col: int) -> None:
    """Set cursor position."""
```

#### Events

```python
class Submitted(Message):
    """Posted when user presses Enter in INSERT mode."""

    @property
    def text(self) -> str:
        """The submitted text."""

    @property
    def text_area(self) -> VimTextArea:
        """The VimTextArea that was submitted."""

class ModeChanged(Message):
    """Posted when vim mode changes."""

    @property
    def mode(self) -> VimMode:
        """The new mode."""

    @property
    def previous_mode(self) -> VimMode:
        """The previous mode."""
```

### VimMode

Enum representing vim modes:

```python
class VimMode(Enum):
    INSERT = "insert"     # Normal text input
    COMMAND = "command"   # Vim command mode
    VISUAL = "visual"     # Visual selection mode
```

### CSS Classes

VimTextArea automatically applies CSS classes based on mode:

- `.insert-mode` - Applied in INSERT mode
- `.command-mode` - Applied in COMMAND mode
- `.visual-mode` - Applied in VISUAL mode

## Customization

### Styling Modes

Customize the appearance of different modes with CSS:

```python
class MyApp(App):
    CSS = """
    VimTextArea.insert-mode {
        border: solid green;
        background: $surface;
    }

    VimTextArea.command-mode {
        border: solid blue;
        background: $surface;
    }

    VimTextArea.visual-mode {
        border: solid yellow;
        background: $boost;
    }

    VimTextArea {
        height: auto;
        max-height: 20;
        min-height: 3;
    }
    """
```

### Handling Events

Listen to vim-specific events:

```python
def on_vim_text_area_mode_changed(self, event: VimTextArea.ModeChanged):
    """React to mode changes."""
    if event.mode == VimMode.INSERT:
        self.sub_title = "Editing"
    elif event.mode == VimMode.COMMAND:
        self.sub_title = "Command"

def on_vim_text_area_submitted(self, event: VimTextArea.Submitted):
    """Handle text submission."""
    self.process_input(event.text)
    event.text_area.clear()
```

### Extending VimTextArea

Subclass to add custom functionality:

```python
from vimkeys_input import VimTextArea
from textual import events

class HistoryVimTextArea(VimTextArea):
    """VimTextArea with input history navigation."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_history = []
        self.history_index = -1

    def add_to_history(self, text: str):
        """Add entry to history."""
        if text.strip():
            self.input_history.append(text)

    def on_key(self, event: events.Key) -> None:
        """Handle up/down for history navigation."""
        if event.key == "up" and self.cursor_location == (0, 0):
            # Load previous history entry
            if self.input_history and self.history_index < len(self.input_history) - 1:
                self.history_index += 1
                self.text = self.input_history[-(self.history_index + 1)]
                event.prevent_default()
                return

        return super().on_key(event)
```

## Architecture

VimTextArea is built using a modular mixin architecture:

```
VimTextArea (vim_textarea.py)
├── NavigationMixin (operations/navigation.py)
│   └── Handles h, j, k, l, w, b, e, 0, $, gg, G
├── EditingMixin (operations/editing.py)
│   └── Handles x, r, p, P, u, Ctrl+r, J
├── VisualMixin (operations/visual.py)
│   └── Handles visual mode selection and operations
├── SearchMixin (operations/search.py)
│   └── Handles /, n, N search operations
├── TextObjectMixin (operations/text_objects.py)
│   └── Handles iw, aw, i", a", i(, a(, etc.
├── CountHandler (count_handler.py)
│   └── Manages numeric count state
├── OperatorPendingState (operator_pending.py)
│   └── Manages operator+motion combinations
└── MarksManager (marks.py)
    └── Manages position bookmarks

All built on Textual's TextArea widget
```

This modular design keeps the codebase maintainable and extensible.

## Development

### Project Structure

```
vimkeys-input/
├── vimkeys_input/           # Main package
│   ├── __init__.py         # Public API exports
│   ├── vim_modes.py        # VimMode enum
│   ├── vim_textarea.py     # Main widget class
│   ├── count_handler.py    # Count support
│   ├── operator_pending.py # Operator+motion system
│   ├── marks.py            # Position bookmarks
│   └── operations/         # Modular operation mixins
│       ├── __init__.py
│       ├── navigation.py   # Movement commands
│       ├── editing.py      # Edit commands
│       ├── visual.py       # Visual mode
│       ├── search.py       # Search functionality
│       └── text_objects.py # Text object support
├── examples/               # Example applications
│   ├── 01_spike.py
│   ├── 02_simple_chat.py
│   └── 03_streaming_chat.py
├── tests/                  # Test suite (124 tests)
├── docs/                   # Additional documentation
├── plans/                  # Development planning docs
├── pyproject.toml         # Package configuration
└── README.md              # This file
```

### Running Tests

```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_navigation.py

# Run with coverage
pytest --cov=vimkeys_input tests/

# Run with verbose output
pytest -v tests/
```

### Development Mode

Use Textual's dev mode for live reload during development:

```bash
textual run --dev examples/01_spike.py

# Or with console for debugging
textual console
textual run --dev examples/01_spike.py
```

### Code Quality

The project uses:
- **pytest** for testing
- **ruff** for linting and formatting
- **mypy** for type checking (planned)

```bash
# Format code
ruff format vimkeys_input/

# Lint code
ruff check vimkeys_input/

# Type check
mypy vimkeys_input/
```

## Implementation Status

### ✅ Phase 0: Spike (Complete)
- Basic structure and mode switching
- Core navigation (hjkl)
- Basic editing (x, dd, yy, p)
- Visual selection
- Example applications

### ✅ Phase 1: Refactoring (Complete)
- Modular mixin architecture
- Comprehensive test suite (124 tests, 82% passing)
- All navigation commands
- All mode transitions
- Undo/redo integration

### ✅ Phase 2: Advanced Features (Complete)
- Operator + motion system (dw, c$, y3j)
- Count support (5j, 3dd, 2d3w)
- Text objects (diw, ci", da()
- Marks system (ma, 'a, `a)
- Search functionality (/, n, N)
- Join lines (J)
- Replace character (r)

### 🚧 Phase 3: Polish (In Progress)
- Comprehensive documentation
- Additional examples
- Performance optimization
- PyPI package preparation
- Case toggle (~)
- Line operations (S, C)
- Visual line mode (V)

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure tests pass (`pytest tests/`)
6. Commit with descriptive messages
7. Push to your fork
8. Open a Pull Request

## Roadmap

- [ ] Visual line mode (V)
- [ ] Visual block mode (Ctrl+v)
- [ ] Case change operations (~, gu, gU)
- [ ] Line operations (S, C)
- [ ] Repeat command (.)
- [ ] Macros (q, @)
- [ ] More text objects (sentences, paragraphs)
- [ ] Ex commands (`:w`, `:q`)
- [ ] Configuration system
- [ ] Plugin architecture

## FAQ

**Q: Does this support all vim commands?**
A: No, this implements core vim modal editing and the most common commands. It's designed for text input in terminal apps, not as a full vim replacement.

**Q: Can I use this with Textual's built-in TextArea features?**
A: Yes! VimTextArea extends TextArea, so features like syntax highlighting, themes, and language support all work.

**Q: How do I disable vim mode temporarily?**
A: Set `text_area.mode = VimMode.INSERT` to keep the widget in INSERT mode, or subclass and override key handling.

**Q: Does this work on Windows?**
A: Yes! VimTextArea works on all platforms supported by Textual (Linux, macOS, Windows).

**Q: Can I customize which keys trigger which commands?**
A: Currently no, but this is planned for a future release. For now, you can subclass and override key handlers.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Credits

- Built with [Textual](https://textual.textualize.io/) by [Textualize](https://www.textualize.io/)
- Inspired by [Vim](https://www.vim.org/) by Bram Moolenaar
- Created and maintained by contributors

## Links

- **Documentation**: [Full documentation](https://github.com/yourusername/vimkeys-input/docs)
- **Examples**: [Example applications](https://github.com/yourusername/vimkeys-input/tree/main/examples)
- **Issues**: [Bug reports and feature requests](https://github.com/yourusername/vimkeys-input/issues)
- **Discussions**: [Community discussions](https://github.com/yourusername/vimkeys-input/discussions)

---

Made with ❤️ for the Textual community
