# VimKeys Input Examples

This guide explains each example application included with VimKeys Input.

## Overview

The examples demonstrate different use cases and features:

1. **01_spike.py** - Basic vim modal editing
2. **02_simple_chat.py** - Simple chat bot with vim input
3. **03_streaming_chat.py** - Advanced chat with streaming, history, and animations

## Running Examples

```bash
# Basic functionality
uv run python examples/01_spike.py

# Simple chat
uv run python examples/02_simple_chat.py

# Advanced streaming chat
uv run python examples/03_streaming_chat.py

# Development mode with hot reload
textual run --dev examples/01_spike.py
```

## Example 1: Basic Spike (01_spike.py)

### Purpose

Demonstrates the fundamental features of VimTextArea in a minimal application.

### Features Shown

- Basic VimTextArea widget integration
- Mode switching (INSERT, COMMAND, VISUAL)
- Visual mode indicator in the header
- Text submission handling
- Mode change event handling

### Code Structure

```python
class SpikeApp(App):
    """Minimal app demonstrating VimTextArea."""

    def compose(self) -> ComposeResult:
        yield Header()
        yield VimTextArea(id="input")
        yield Footer()

    def on_mount(self):
        """Set initial mode display."""
        self.query_one("#input").focus()
        self.update_mode_display()

    def on_vim_text_area_mode_changed(self, event):
        """Update header when mode changes."""
        self.update_mode_display()

    def on_vim_text_area_submitted(self, event):
        """Handle text submission."""
        self.notify(f"Submitted: {event.text}")
        event.text_area.clear()
```

### What to Try

1. **Insert Mode**
   - Type some text
   - Notice green border

2. **Command Mode**
   - Press `ESC`
   - Border turns blue
   - Try navigation: `h`, `j`, `k`, `l`, `w`, `b`

3. **Visual Mode**
   - Press `v` in COMMAND mode
   - Border turns yellow
   - Extend selection with `h`, `j`, `k`, `l`
   - Press `d` to delete selection

4. **Editing**
   - In COMMAND mode: `dd` to delete line
   - `yy` to copy line
   - `p` to paste

5. **Submission**
   - In INSERT mode, press Enter
   - Notice the notification

### Learning Points

- VimTextArea integrates seamlessly with Textual
- Mode changes trigger events you can handle
- Border color provides visual feedback
- Submit event fires on Enter in INSERT mode

## Example 2: Simple Chat (02_simple_chat.py)

### Purpose

Shows how to build a simple chat bot interface with vim-style input.

### Features Shown

- RichLog for displaying chat history
- VimTextArea for input
- Message handling and display
- Bot response simulation
- Layout with Vertical container

### Code Structure

```python
class SimpleChatApp(App):
    """Chat bot with vim-style input."""

    def compose(self) -> ComposeResult:
        with Vertical():
            yield RichLog(id="history")
            yield VimTextArea(id="input")
```

### What to Try

1. **Basic Chat**
   - Type a message
   - Press Enter to send
   - Bot responds automatically

2. **Vim Editing**
   - Type a long message
   - Press `ESC`, use `w`/`b` to navigate
   - Use `dw` to delete words
   - Use `ciw` to change words

3. **Copy/Paste**
   - Type a message
   - `yy` to copy
   - Send it
   - `p` to paste and send again

4. **Multi-line Input**
   - Type text with newlines (Shift+Enter)
   - Navigate with `j`/`k`
   - Edit across lines

### Learning Points

- RichLog displays formatted chat history
- VimTextArea handles multi-line input
- Clear input after submission
- Bot logic runs asynchronously

## Example 3: Streaming Chat (03_streaming_chat.py)

### Purpose

Demonstrates advanced features in a production-like chat application.

### Features Shown

- Token-by-token streaming responses
- Animated "thinking" indicator
- Input history navigation (up/down arrows)
- Text wrapping in history
- Command palette integration
- Custom VimTextArea subclass (HistoryVimTextArea)
- Conversation persistence
- Save/load functionality

### Code Structure

```python
class HistoryVimTextArea(VimTextArea):
    """VimTextArea with input history navigation."""

    def on_key(self, event: events.Key) -> None:
        """Handle up/down for history navigation."""
        # Custom history navigation logic
        ...

class StreamingChatApp(App):
    """Advanced chat with streaming and history."""

    async def animate_thinking_dots(self):
        """Animate the thinking indicator."""
        # Cycles through ".", "..", "..."
        ...

    async def stream_ai_response(self, prompt: str):
        """Stream response token by token."""
        # Yields tokens one at a time
        ...
```

### What to Try

1. **Streaming Responses**
   - Send a message
   - Watch "AI is thinking" animate
   - See response stream in token-by-token

2. **Input History**
   - Send several messages
   - Move cursor to (0, 0) with arrow keys
   - Press up arrow to load previous messages
   - Press down arrow to cycle forward

3. **Vim Commands**
   - Use all standard vim commands
   - Try operator+motion: `dw`, `c$`, `y3w`
   - Use text objects: `ciw`, `di"`, `da(`
   - Test visual mode

4. **Command Palette**
   - Press `Ctrl+\\` (or textual command palette key)
   - Try "clear", "save", "new" commands

5. **Save Conversation**
   - Have a conversation
   - Press `Ctrl+s`
   - Check saved markdown file

### Advanced Features Explained

#### Input History Navigation

```python
def on_key(self, event: events.Key) -> None:
    if event.key == "up" and self.cursor_location == (0, 0):
        # Load previous history entry
        if self.input_history:
            self.text = self.input_history[-1]
```

Only activates when cursor is at top-left, so normal navigation still works.

#### Animated Thinking Indicator

```python
async def animate_thinking_dots(self):
    messages = [
        "AI is thinking",
        "AI is thinking.",
        "AI is thinking..",
        "AI is thinking...",
    ]
    while self.is_streaming:
        # Update last line with animation frame
        self.display_lines[-1] = messages[dots]
        await asyncio.sleep(0.5)
```

Updates the display every 500ms to show animated dots.

#### Token Streaming

```python
async for token in self.stream_ai_response(prompt):
    full_response += token
    # Update display with accumulated response
    self.display_lines[-1] = f"AI: {full_response}"
    self._refresh_history()
```

Each token triggers a display refresh, creating a streaming effect.

### Learning Points

- Subclassing VimTextArea adds custom features
- Async tasks enable animations and streaming
- Input history enhances UX
- Command palette integrates with Textual
- Text wrapping prevents horizontal scroll
- Conversation state can be persisted

## Common Patterns

### Pattern 1: Basic Input

```python
def compose(self) -> ComposeResult:
    yield VimTextArea(id="input")

def on_vim_text_area_submitted(self, event):
    text = event.text
    self.process(text)
    event.text_area.clear()
```

### Pattern 2: With Display

```python
def compose(self) -> ComposeResult:
    with Vertical():
        yield RichLog(id="output")
        yield VimTextArea(id="input")

def on_vim_text_area_submitted(self, event):
    output = self.query_one("#output", RichLog)
    output.write(f"Input: {event.text}")
    event.text_area.clear()
```

### Pattern 3: Mode-Aware UI

```python
def on_vim_text_area_mode_changed(self, event):
    if event.mode == VimMode.INSERT:
        self.sub_title = "Editing"
    elif event.mode == VimMode.COMMAND:
        self.sub_title = "Command"
```

### Pattern 4: Custom Styling

```python
class MyApp(App):
    CSS = """
    #input {
        height: auto;
        max-height: 10;
    }

    #input.insert-mode {
        border: solid green;
    }

    #input.command-mode {
        border: solid blue;
    }
    """
```

## Building Your Own

### Chat Bot Template

```python
from textual.app import App, ComposeResult
from textual.widgets import RichLog
from textual.containers import Vertical
from vimkeys_input import VimTextArea

class MyChatBot(App):
    def compose(self) -> ComposeResult:
        with Vertical():
            yield RichLog(id="history", wrap=True)
            yield VimTextArea(id="input")

    def on_mount(self):
        self.query_one("#input").focus()

    async def on_vim_text_area_submitted(self, event):
        if not event.text.strip():
            return

        # Show user message
        history = self.query_one("#history")
        history.write(f"[bold cyan]You:[/bold cyan] {event.text}")

        # Generate and show bot response
        response = await self.get_bot_response(event.text)
        history.write(f"[bold green]Bot:[/bold green] {response}")

        event.text_area.clear()

    async def get_bot_response(self, message: str) -> str:
        """Your bot logic here."""
        return f"You said: {message}"

if __name__ == "__main__":
    MyChatBot().run()
```

### Form Input Template

```python
from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.widgets import Label, Button
from vimkeys_input import VimTextArea

class MyForm(App):
    def compose(self) -> ComposeResult:
        with Grid():
            yield Label("Name:")
            yield VimTextArea(id="name")
            yield Label("Email:")
            yield VimTextArea(id="email")
            yield Button("Submit", id="submit")

    def on_button_pressed(self, event):
        name = self.query_one("#name").text
        email = self.query_one("#email").text
        self.process_form(name, email)

    def process_form(self, name, email):
        self.notify(f"Submitted: {name} <{email}>")
```

## Next Steps

- Read the [User Guide](user-guide.md) for detailed vim command reference
- Check the [API Reference](api-reference.md) for complete API docs
- See [Contributing](../CONTRIBUTING.md) to add your own examples

## Tips for Example Development

1. **Start Simple** - Begin with basic functionality, add features incrementally
2. **Use Dev Mode** - `textual run --dev` enables hot reload
3. **Test Vim Commands** - Try all vim operations to ensure they work
4. **Add Comments** - Explain non-obvious code for learners
5. **Handle Edge Cases** - Empty input, long text, special characters
6. **Style Consistently** - Use CSS for professional appearance
