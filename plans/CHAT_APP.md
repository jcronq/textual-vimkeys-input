# Chat Application Architecture

**Purpose**: Build a production-ready chat application using Textual + VimTextArea
**Target Audience**: Developers building AI chat interfaces, REPL tools, or interactive CLIs
**Key Features**: Streaming responses, multiple agents, themes, command palette

---

## Overview

This document describes how to build chat applications using the VimTextArea widget within Textual's framework.

### Application Types

1. **Simple Chat** - Single agent, basic input/output
2. **Streaming Chat** - LLM streaming responses
3. **Multi-Agent Chat** - Multiple AI agents in different panels
4. **Multi-Modal Chat** - Text, code, images, tables

---

## Architecture Patterns

### Pattern 1: Simple Chat Application

**Use Case**: Basic question/answer interface

```python
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, RichLog
from textbox import VimTextArea

class SimpleChatApp(App):
    """Simple chat application."""

    CSS = """
    #history {
        height: 1fr;
        border: solid $primary;
        padding: 1;
    }

    #input {
        height: auto;
        max-height: 10;
        margin: 1;
    }

    .user-message {
        color: $text;
    }

    .ai-message {
        color: $success;
    }
    """

    def compose(self) -> ComposeResult:
        """Create layout."""
        yield Header()
        yield RichLog(id="history", markup=True)
        yield VimTextArea(id="input", language="markdown")
        yield Footer()

    def on_mount(self):
        """Initialize on mount."""
        self.title = "AI Chat"
        self.query_one("#input").focus()

        # Welcome message
        history = self.query_one("#history")
        history.write("[bold cyan]Welcome to AI Chat![/bold cyan]")
        history.write("Type your message and press Enter in insert mode.")

    async def on_vim_text_area_submitted(self, event: VimTextArea.Submitted):
        """Handle user message."""
        history = self.query_one("#history")

        # Display user message
        history.write(f"[bold]You:[/bold] {event.text}")

        # Get and display AI response
        response = await self.get_ai_response(event.text)
        history.write(f"[bold green]AI:[/bold green] {response}")

    async def get_ai_response(self, prompt: str) -> str:
        """Get AI response (placeholder - replace with actual API)."""
        # TODO: Integrate with your LLM API
        return f"Echo: {prompt}"

if __name__ == "__main__":
    app = SimpleChatApp()
    app.run()
```

### Pattern 2: Streaming Chat

**Use Case**: LLM with token-by-token streaming

```python
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, RichLog, LoadingIndicator
from textual.containers import Vertical, Horizontal
from textbox import VimTextArea
import asyncio

class StreamingChatApp(App):
    """Chat app with streaming responses."""

    CSS = """
    #history {
        height: 1fr;
        border: solid $primary;
        scrollbar-gutter: stable;
    }

    #input {
        height: auto;
        max-height: 10;
    }

    #status {
        height: 1;
        background: $panel;
        padding: 0 1;
    }

    .thinking {
        color: $warning;
        text-style: italic;
    }
    """

    BINDINGS = [
        ("ctrl+l", "clear_history", "Clear"),
        ("ctrl+s", "save_conversation", "Save"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield RichLog(id="history", markup=True, auto_scroll=True)
            yield VimTextArea(id="input")
        yield Footer()

    def on_mount(self):
        """Initialize."""
        self.title = "Streaming Chat"
        self.query_one("#input").focus()
        self.is_streaming = False

    async def on_vim_text_area_submitted(self, event: VimTextArea.Submitted):
        """Handle user message with streaming."""
        if self.is_streaming:
            self.notify("Please wait for current response to complete")
            return

        history = self.query_one("#history")

        # User message
        history.write(f"[bold cyan]You:[/bold cyan] {event.text}")

        # Show thinking indicator
        self.is_streaming = True
        history.write("[dim italic]AI is thinking...[/dim italic]")

        # Stream response
        history.write("[bold green]AI:[/bold green] ", end="")

        try:
            async for token in self.stream_ai_response(event.text):
                history.write(token, end="")
                await asyncio.sleep(0)  # Yield control

            history.write("")  # New line after response

        finally:
            self.is_streaming = False

    async def stream_ai_response(self, prompt: str):
        """Stream AI response token by token."""
        # TODO: Replace with actual LLM streaming
        # Example with OpenAI:
        # async for chunk in openai.ChatCompletion.acreate(..., stream=True):
        #     yield chunk["choices"][0]["delta"].get("content", "")

        # Placeholder: word-by-word
        words = f"This is a streaming response to: {prompt}".split()
        for word in words:
            yield word + " "
            await asyncio.sleep(0.05)

    def action_clear_history(self):
        """Clear chat history."""
        history = self.query_one("#history")
        history.clear()
        self.notify("History cleared")

    async def action_save_conversation(self):
        """Save conversation to file."""
        history = self.query_one("#history")
        # Get text from RichLog (would need API support)
        self.notify("Save feature coming soon")

if __name__ == "__main__":
    app = StreamingChatApp()
    app.run()
```

### Pattern 3: Multi-Agent Chat

**Use Case**: Multiple AI agents with different roles

```python
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, RichLog, Static
from textual.containers import Vertical, Horizontal
from textbox import VimTextArea
import asyncio

class MultiAgentChatApp(App):
    """Chat with multiple AI agents."""

    CSS = """
    .agent-panel {
        height: 1fr;
        border: solid $primary;
        padding: 1;
    }

    #code-agent {
        border: solid green;
    }

    #research-agent {
        border: solid blue;
    }

    #writing-agent {
        border: solid yellow;
    }

    #input {
        height: auto;
        max-height: 8;
    }

    .agent-title {
        background: $panel;
        text-align: center;
        text-style: bold;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal():
            # Code Agent Panel
            with Vertical():
                yield Static("🤖 Code Agent", classes="agent-title")
                yield RichLog(id="code-agent", classes="agent-panel", markup=True)

            # Research Agent Panel
            with Vertical():
                yield Static("🔍 Research Agent", classes="agent-title")
                yield RichLog(id="research-agent", classes="agent-panel", markup=True)

            # Writing Agent Panel
            with Vertical():
                yield Static("✍️ Writing Agent", classes="agent-title")
                yield RichLog(id="writing-agent", classes="agent-panel", markup=True)

        yield VimTextArea(id="input")
        yield Footer()

    def on_mount(self):
        """Initialize."""
        self.title = "Multi-Agent Chat"
        self.query_one("#input").focus()

    async def on_vim_text_area_submitted(self, event: VimTextArea.Submitted):
        """Route message to all agents."""
        prompt = event.text

        # Get agent outputs
        code_agent = self.query_one("#code-agent")
        research_agent = self.query_one("#research-agent")
        writing_agent = self.query_one("#writing-agent")

        # Display prompt in all panels
        for agent in [code_agent, research_agent, writing_agent]:
            agent.write(f"[dim]User: {prompt}[/dim]")

        # Run agents concurrently
        await asyncio.gather(
            self.run_code_agent(prompt, code_agent),
            self.run_research_agent(prompt, research_agent),
            self.run_writing_agent(prompt, writing_agent),
        )

    async def run_code_agent(self, prompt: str, output: RichLog):
        """Code-focused agent."""
        output.write("[bold green]Code Agent:[/bold green] ", end="")

        # TODO: Call specialized LLM for code
        async for token in self.stream_response(f"Code: {prompt}"):
            output.write(token, end="")

        output.write("")

    async def run_research_agent(self, prompt: str, output: RichLog):
        """Research-focused agent."""
        output.write("[bold blue]Research Agent:[/bold blue] ", end="")

        # TODO: Call specialized LLM for research
        async for token in self.stream_response(f"Research: {prompt}"):
            output.write(token, end="")

        output.write("")

    async def run_writing_agent(self, prompt: str, output: RichLog):
        """Writing-focused agent."""
        output.write("[bold yellow]Writing Agent:[/bold yellow] ", end="")

        # TODO: Call specialized LLM for writing
        async for token in self.stream_response(f"Writing: {prompt}"):
            output.write(token, end="")

        output.write("")

    async def stream_response(self, text: str):
        """Stream tokens."""
        for word in text.split():
            yield word + " "
            await asyncio.sleep(0.05)

if __name__ == "__main__":
    app = MultiAgentChatApp()
    app.run()
```

---

## Command Palette Integration

### Custom Commands

```python
from textual.command import Provider, Hit
from textual.app import App

class ChatCommands(Provider):
    """Custom commands for chat app."""

    async def search(self, query: str) -> list[Hit]:
        """Search for commands."""
        matcher = self.matcher(query)

        commands = [
            ("clear", "Clear chat history", "🗑️"),
            ("save", "Save conversation", "💾"),
            ("export-markdown", "Export as Markdown", "📝"),
            ("export-html", "Export as HTML", "🌐"),
            ("theme-dark", "Dark theme", "🌙"),
            ("theme-light", "Light theme", "☀️"),
            ("theme-monokai", "Monokai theme", "🎨"),
            ("new-conversation", "Start new conversation", "✨"),
            ("settings", "Open settings", "⚙️"),
        ]

        for command_id, text, icon in commands:
            score = matcher.match(text)
            if score > 0:
                yield Hit(
                    score,
                    matcher.highlight(text),
                    lambda c=command_id: self.execute_command(c),
                    help=f"{icon} {text}",
                )

    async def execute_command(self, command_id: str):
        """Execute command."""
        app = self.app

        if command_id == "clear":
            app.query_one("#history").clear()
            app.notify("History cleared")

        elif command_id == "save":
            # Save logic
            app.notify("Conversation saved")

        elif command_id == "export-markdown":
            # Export logic
            app.notify("Exported as Markdown")

        elif command_id == "export-html":
            # Export logic
            app.notify("Exported as HTML")

        elif command_id.startswith("theme-"):
            theme_name = command_id.replace("theme-", "")
            app.theme = f"textual-{theme_name}" if theme_name in ["dark", "light"] else theme_name
            app.notify(f"Theme changed to {theme_name}")

        elif command_id == "new-conversation":
            app.query_one("#history").clear()
            app.query_one("#input").clear()
            app.notify("Started new conversation")

        elif command_id == "settings":
            # Open settings modal
            app.notify("Settings coming soon")

class ChatApp(App):
    """Chat app with command palette."""

    COMMANDS = {ChatCommands}

    # ... rest of app
```

**Usage**: Press Ctrl+\\ (Textual's default) or Ctrl+P to open command palette

---

## Rich Text Features

### Syntax Highlighting

```python
from rich.syntax import Syntax

async def on_vim_text_area_submitted(self, event):
    """Handle code input."""
    code = event.text
    history = self.query_one("#history")

    # Detect language (simple heuristic)
    if code.startswith("def ") or "import " in code:
        language = "python"
    elif code.startswith("function ") or "const " in code:
        language = "javascript"
    else:
        language = "python"  # Default

    # Syntax highlight
    syntax = Syntax(code, language, theme="monokai", line_numbers=True)
    history.write(syntax)
```

### Tables

```python
from rich.table import Table

async def show_results(self, data: list[dict]):
    """Display results as table."""
    history = self.query_one("#history")

    table = Table(title="Results", show_header=True, header_style="bold magenta")

    # Add columns
    if data:
        for key in data[0].keys():
            table.add_column(key.title())

        # Add rows
        for row in data:
            table.add_row(*[str(v) for v in row.values()])

    history.write(table)
```

### Markdown

```python
from rich.markdown import Markdown

async def on_vim_text_area_submitted(self, event):
    """Handle markdown input."""
    history = self.query_one("#history")

    # Render markdown
    markdown = Markdown(event.text)
    history.write(markdown)
```

---

## Theming

### Built-in Themes

```python
class ChatApp(App):
    """Chat with theme support."""

    def on_mount(self):
        """Set initial theme."""
        self.theme = "textual-dark"  # or "textual-light"

    def action_toggle_theme(self):
        """Toggle between dark and light."""
        current = self.theme
        self.theme = "textual-light" if current == "textual-dark" else "textual-dark"
```

### Custom Theme

```python
from textual.theme import Theme

# Define custom theme
custom_theme = Theme(
    name="custom",
    primary="#3b82f6",
    secondary="#8b5cf6",
    accent="#f59e0b",
    foreground="#f9fafb",
    background="#0f172a",
    success="#10b981",
    warning="#f59e0b",
    error="#ef4444",
    surface="#1e293b",
    panel="#334155",
)

class ChatApp(App):
    def on_mount(self):
        """Register and use custom theme."""
        self.register_theme(custom_theme)
        self.theme = "custom"
```

### CSS Styling

```python
class ChatApp(App):
    CSS = """
    Screen {
        background: $background;
    }

    #history {
        background: $surface;
        border: solid $primary;
        scrollbar-color: $primary;
        scrollbar-color-hover: $accent;
    }

    #input {
        border: solid $secondary;
    }

    #input.insert-mode {
        border: solid $success;
    }

    #input.command-mode {
        border: solid $primary;
    }

    .user-message {
        color: $accent;
        text-style: bold;
    }

    .ai-message {
        color: $success;
    }

    .error-message {
        color: $error;
        background: $surface;
        padding: 1;
        border: solid $error;
    }
    """
```

---

## State Management

### Conversation State

```python
from dataclasses import dataclass
from typing import List

@dataclass
class Message:
    """Single message in conversation."""
    role: str  # "user" or "assistant"
    content: str
    timestamp: float

class ChatApp(App):
    """Chat with conversation state."""

    def __init__(self):
        super().__init__()
        self.conversation: List[Message] = []
        self.current_agent = "default"

    async def on_vim_text_area_submitted(self, event):
        """Store and process message."""
        import time

        # Store user message
        user_msg = Message(
            role="user",
            content=event.text,
            timestamp=time.time()
        )
        self.conversation.append(user_msg)

        # Get AI response
        response = await self.get_ai_response(event.text)

        # Store AI message
        ai_msg = Message(
            role="assistant",
            content=response,
            timestamp=time.time()
        )
        self.conversation.append(ai_msg)

        # Display
        self.display_message(user_msg)
        self.display_message(ai_msg)

    def display_message(self, msg: Message):
        """Display message in history."""
        history = self.query_one("#history")

        if msg.role == "user":
            history.write(f"[bold cyan]You:[/bold cyan] {msg.content}")
        else:
            history.write(f"[bold green]AI:[/bold green] {msg.content}")

    def export_conversation(self, format: str = "markdown"):
        """Export conversation."""
        if format == "markdown":
            lines = ["# Conversation\n"]
            for msg in self.conversation:
                role = "**You**" if msg.role == "user" else "**AI**"
                lines.append(f"{role}: {msg.content}\n")
            return "\n".join(lines)
```

---

## LLM Integration Examples

### OpenAI

```python
import openai
import os

class OpenAIChatApp(App):
    """Chat with OpenAI integration."""

    def on_mount(self):
        """Initialize OpenAI."""
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.conversation_history = []

    async def get_ai_response(self, prompt: str) -> str:
        """Get response from OpenAI."""
        self.conversation_history.append({"role": "user", "content": prompt})

        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=self.conversation_history,
        )

        reply = response.choices[0].message.content
        self.conversation_history.append({"role": "assistant", "content": reply})

        return reply

    async def stream_ai_response(self, prompt: str):
        """Stream response from OpenAI."""
        self.conversation_history.append({"role": "user", "content": prompt})

        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=self.conversation_history,
            stream=True,
        )

        full_response = ""
        async for chunk in response:
            delta = chunk.choices[0].delta
            if "content" in delta:
                token = delta.content
                full_response += token
                yield token

        self.conversation_history.append({"role": "assistant", "content": full_response})
```

### Anthropic Claude

```python
import anthropic
import os

class ClaudeChatApp(App):
    """Chat with Anthropic Claude."""

    def on_mount(self):
        """Initialize Anthropic client."""
        self.client = anthropic.AsyncAnthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        self.conversation_history = []

    async def stream_ai_response(self, prompt: str):
        """Stream response from Claude."""
        self.conversation_history.append({"role": "user", "content": prompt})

        async with self.client.messages.stream(
            model="claude-3-5-sonnet-20241022",
            messages=self.conversation_history,
            max_tokens=4096,
        ) as stream:
            full_response = ""
            async for text in stream.text_stream:
                full_response += text
                yield text

            self.conversation_history.append({
                "role": "assistant",
                "content": full_response
            })
```

---

## Error Handling

### Graceful Degradation

```python
class ChatApp(App):
    """Chat with error handling."""

    async def on_vim_text_area_submitted(self, event):
        """Handle message with error handling."""
        history = self.query_one("#history")

        history.write(f"[bold]You:[/bold] {event.text}")

        try:
            # Show thinking
            history.write("[dim]Thinking...[/dim]")

            # Get response
            response = await self.get_ai_response(event.text)
            history.write(f"[bold green]AI:[/bold green] {response}")

        except Exception as e:
            # Show error
            history.write(
                f"[bold red]Error:[/bold red] {str(e)}",
                classes="error-message"
            )
            self.notify(f"Error: {str(e)}", severity="error", timeout=5)

    async def get_ai_response(self, prompt: str) -> str:
        """Get AI response with retries."""
        max_retries = 3

        for attempt in range(max_retries):
            try:
                return await self._call_ai_api(prompt)

            except TimeoutError:
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise

            except Exception as e:
                # Log error
                self.log.error(f"AI API error: {e}")
                raise
```

---

## Testing

### Widget Testing

```python
import pytest
from textual.pilot import Pilot

@pytest.fixture
async def chat_app():
    """Create chat app for testing."""
    app = SimpleChatApp()
    async with app.run_test() as pilot:
        yield app, pilot

async def test_user_message(chat_app):
    """Test sending user message."""
    app, pilot = chat_app

    # Get input widget
    input_widget = app.query_one("#input")

    # Type message
    input_widget.text = "Hello"

    # Submit (trigger enter in insert mode)
    await pilot.press("enter")

    # Check history
    history = app.query_one("#history")
    # Assert message appears (would need RichLog API)

async def test_vim_mode_switching(chat_app):
    """Test vim modes work."""
    app, pilot = chat_app

    input_widget = app.query_one("#input")

    # Should start in insert mode
    assert input_widget.vim_mode == VimMode.INSERT

    # ESC to command mode
    await pilot.press("escape")
    assert input_widget.vim_mode == VimMode.COMMAND

    # i to insert mode
    await pilot.press("i")
    assert input_widget.vim_mode == VimMode.INSERT
```

---

## Performance Optimization

### Large Conversations

```python
class ChatApp(App):
    """Chat with conversation limits."""

    MAX_MESSAGES = 100

    async def on_vim_text_area_submitted(self, event):
        """Handle message with limits."""
        history = self.query_one("#history")

        # Trim if too many messages
        if len(self.conversation) > self.MAX_MESSAGES:
            self.conversation = self.conversation[-self.MAX_MESSAGES:]

        # ... rest of logic
```

### Streaming Optimization

```python
async def stream_ai_response(self, prompt: str):
    """Stream with batching for performance."""
    buffer = ""
    batch_size = 5  # Buffer 5 tokens before rendering

    async for token in self.get_tokens(prompt):
        buffer += token

        if len(buffer) >= batch_size:
            yield buffer
            buffer = ""

    # Yield remaining
    if buffer:
        yield buffer
```

---

## Deployment

### Standalone Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --name chat-app app.py
```

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

---

## Next Steps

1. **Choose a pattern** - Simple, Streaming, or Multi-Agent
2. **Implement VimTextArea** - Follow VIM_TEXTAREA.md
3. **Build chat app** - Using patterns from this document
4. **Add LLM integration** - OpenAI, Anthropic, or other
5. **Customize** - Themes, commands, features

See [IMPLEMENTATION.md](IMPLEMENTATION.md) for detailed timeline.
