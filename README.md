# VimKeys Input

A custom Textual widget that adds vim-style keybindings and modal editing to `TextArea`.

## Features

- **Modal Editing**: Insert, Command, and Visual modes
- **Vim Navigation**: hjkl, w/b/e, 0/$, gg/G, and more
- **Vim Editing**: dd, yy, p, x, u, and visual selection
- **Visual Feedback**: Border colors change based on mode
- **TextArea Base**: Built on Textual's robust TextArea widget

## Installation

```bash
# Using uv (recommended)
uv venv .venv
uv pip install -e .

# Or using pip
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .

# With development dependencies
uv pip install -e ".[dev]"
```

## Quick Start

### Basic Usage

```python
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from vimkeys_input import VimTextArea

class MyApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield VimTextArea(id="input")
        yield Footer()

    def on_vim_text_area_submitted(self, event: VimTextArea.Submitted):
        print(f"User entered: {event.text}")

app = MyApp()
app.run()
```

### Run Examples

```bash
# Spike test - basic functionality
python examples/01_spike.py

# Simple chat bot
python examples/02_simple_chat.py

# Streaming chat (simulated)
python examples/03_streaming_chat.py
```

## Vim Keybindings

### Modes

- **ESC** - Enter command mode
- **i** - Insert at cursor
- **a** - Append after cursor
- **I** - Insert at line start
- **A** - Append at line end
- **o** - Open line below
- **O** - Open line above
- **v** - Visual mode

### Navigation (Command Mode)

- **hjkl** - Move cursor left/down/up/right
- **w** - Next word
- **b** - Previous word
- **e** - End of word
- **0** - Line start
- **$** - Line end
- **gg** - Document start
- **G** - Document end

### Editing (Command Mode)

- **x** - Delete character
- **dd** - Delete line
- **yy** - Yank (copy) line
- **p** - Paste after
- **P** - Paste before
- **u** - Undo
- **Ctrl+r** - Redo

### Visual Mode

- **hjkl** - Extend selection
- **w/b** - Select words
- **y** - Yank selection
- **d** - Delete selection

### Insert Mode

- **Enter** - Submit text (customizable)
- **Backspace, arrows, etc.** - Standard editing

## Development

### Project Structure

```
vimkeys-input/
├── vimkeys_input/        # Main package
│   ├── __init__.py
│   ├── vim_modes.py      # VimMode enum
│   └── vim_textarea.py   # VimTextArea widget
├── examples/             # Example applications
│   ├── 01_spike.py
│   ├── 02_simple_chat.py
│   └── 03_streaming_chat.py
├── tests/                # Test suite
├── docs/                 # Documentation
└── plans/                # Planning documents
```

### Running Tests

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run tests
pytest tests/
```

### Development Mode

Use Textual's dev mode for hot reload:

```bash
textual run --dev examples/01_spike.py
```

## Architecture

VimTextArea extends Textual's `TextArea` widget:

- **Base**: Uses TextArea's editing, undo/redo, and cursor management
- **Mode System**: Adds vim modal editing on top
- **Key Handling**: Intercepts keys and routes based on current mode
- **Visual Feedback**: CSS classes change based on mode

## Customization

### CSS Styling

```python
class MyApp(App):
    CSS = """
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
```

### Events

Listen to mode changes and submissions:

```python
def on_vim_text_area_mode_changed(self, event: VimTextArea.ModeChanged):
    print(f"Mode changed to: {event.mode}")

def on_vim_text_area_submitted(self, event: VimTextArea.Submitted):
    print(f"Submitted: {event.text}")
```

## Implementation Status

### Phase 0: Spike ✅ (Current)
- [x] Basic structure
- [x] Mode switching (INSERT/COMMAND/VISUAL)
- [x] hjkl navigation
- [x] Basic editing (x, dd, yy, p)
- [x] Visual selection
- [x] Example applications

### Phase 1: Basic Vim (Next)
- [ ] All navigation (w, b, e, 0, $, gg, G)
- [ ] All mode transitions (i, a, I, A, o, O)
- [ ] Undo/redo
- [ ] Unit tests

### Phase 2: Advanced Vim (Future)
- [ ] Character search (f, t, F, T)
- [ ] Replace (r)
- [ ] Advanced operations
- [ ] Complete test coverage

### Phase 3: Polish (Future)
- [ ] Documentation
- [ ] More examples
- [ ] Performance optimization
- [ ] PyPI package

## Contributing

This project follows the implementation plan in `plans/`. See:

- `plans/INDEX.md` - Overview
- `plans/SPIKE_GUIDE.md` - Current phase
- `plans/VIM_TEXTAREA.md` - Widget design
- `plans/IMPLEMENTATION.md` - Full timeline

## License

MIT License - See LICENSE file for details.

## Credits

Built with [Textual](https://textual.textualize.io/) by Textualize
