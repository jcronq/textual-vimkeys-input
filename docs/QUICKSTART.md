# Quick Start Guide

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd textual-vimkeys-input
   ```

2. **Set up virtual environment**
   ```bash
   # Using uv (recommended - faster)
   uv venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

   # Or using standard venv
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install package**
   ```bash
   # Using uv (recommended)
   uv pip install -e .

   # Or using pip
   pip install -e .
   ```

4. **Run tests (optional)**
   ```bash
   # Using uv
   uv pip install -e ".[dev]"
   pytest tests/ -v

   # Or using pip
   pip install -e ".[dev]"
   pytest tests/ -v
   ```

## Running Examples

### Option 1: Using the helper script

```bash
./run_example.sh 01_spike
./run_example.sh 02_simple_chat
./run_example.sh 03_streaming_chat
```

### Option 2: Direct Python execution

```bash
source .venv/bin/activate

python examples/01_spike.py
python examples/02_simple_chat.py
python examples/03_streaming_chat.py
```

## Using VimTextArea in Your App

### Minimal Example

```python
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from vimkeys_input import VimTextArea

class MyApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield VimTextArea()
        yield Footer()

    def on_vim_text_area_submitted(self, event: VimTextArea.Submitted):
        self.notify(f"You entered: {event.text}")

if __name__ == "__main__":
    app = MyApp()
    app.run()
```

### With Mode Indicator

```python
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from vimkeys_input import VimTextArea, VimMode

class MyApp(App):
    CSS = """
    #mode {
        height: 1;
        background: $panel;
        text-align: center;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("-- INSERT --", id="mode")
        yield VimTextArea()
        yield Footer()

    def on_vim_text_area_mode_changed(self, event: VimTextArea.ModeChanged):
        mode_display = self.query_one("#mode")
        mode_text = {
            VimMode.INSERT: "[green]-- INSERT --[/green]",
            VimMode.COMMAND: "[blue]-- COMMAND --[/blue]",
            VimMode.VISUAL: "[yellow]-- VISUAL --[/yellow]",
        }[event.mode]
        mode_display.update(mode_text)

if __name__ == "__main__":
    app = MyApp()
    app.run()
```

## Vim Keybindings Cheat Sheet

### Mode Switching
- `ESC` - Enter command mode (from any mode)
- `i` - Insert at cursor
- `a` - Append after cursor
- `I` - Insert at line start
- `A` - Append at line end
- `o` - Open line below
- `O` - Open line above
- `v` - Visual mode

### Navigation (Command Mode)
- `h/j/k/l` - Left/Down/Up/Right
- `w` - Next word
- `b` - Previous word
- `e` - End of word
- `0` - Line start
- `$` - Line end
- `gg` - Document start
- `G` - Document end

### Editing (Command Mode)
- `x` - Delete character under cursor
- `X` - Delete character before cursor
- `dd` - Delete line
- `yy` - Copy line
- `p` - Paste after cursor
- `P` - Paste before cursor
- `r<char>` - Replace character
- `u` - Undo
- `Ctrl+r` - Redo

### Visual Mode
- `h/j/k/l` - Extend selection
- `w/b` - Select by word
- `y` - Copy selection
- `d` or `x` - Delete selection
- `ESC` - Exit visual mode

### Insert Mode
- `Enter` - Submit text (default behavior, customizable)
- Regular typing, arrows, backspace work normally

## Development Tips

### Hot Reload

Use Textual's dev mode for faster development:

```bash
textual run --dev examples/01_spike.py
```

### Custom CSS

Customize mode colors:

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

### Custom Submit Behavior

Override Enter behavior by handling the event:

```python
def on_vim_text_area_submitted(self, event: VimTextArea.Submitted):
    # Custom logic here
    text = event.text
    # Don't clear if you want to keep the text
    # Widget automatically clears by default
```

## Troubleshooting

### Import Error

```
ModuleNotFoundError: No module named 'textbox'
```

**Solution:** Make sure you're running from the project root and the virtual environment is activated.

### Textual Not Found

```
ModuleNotFoundError: No module named 'textual'
```

**Solution:** Install package with dependencies:
```bash
uv pip install -e .
# or
pip install -e .
```

### Examples Won't Run

**Solution:** Activate the virtual environment first:
```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

## Next Steps

- Read the full [README.md](../README.md) for complete documentation
- Check out [IMPLEMENTATION_SUMMARY.md](../IMPLEMENTATION_SUMMARY.md) for what's been built
- Explore the planning documents in `plans/` for future features
- Look at the example applications in `examples/` for patterns

## Getting Help

- Check the planning docs in `plans/`
- Look at example code in `examples/`
- Review tests in `tests/` for usage patterns
- Read the Textual documentation: https://textual.textualize.io/
