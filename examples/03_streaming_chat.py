"""Streaming chat application with simulated AI responses.

Demonstrates:
- Token-by-token streaming responses
- Thinking indicator
- Prevents multiple simultaneous requests
- Command palette integration
"""

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, RichLog
from textual.containers import Vertical
from textual.command import Provider, Hit
import asyncio
import sys
import os

# Add parent directory to path so we can import vimkeys_input
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from vimkeys_input import VimTextArea, VimMode


class ChatCommands(Provider):
    """Custom commands for chat app."""

    async def search(self, query: str):
        """Search for commands."""
        matcher = self.matcher(query)

        commands = [
            ("clear", "Clear chat history"),
            ("save", "Save conversation"),
            ("new", "Start new conversation"),
        ]

        for command_id, text in commands:
            score = matcher.match(text)
            if score > 0:
                yield Hit(
                    score,
                    matcher.highlight(text),
                    lambda c=command_id: self.app.run_command(c),
                    help=text,
                )


class StreamingChatApp(App):
    """Chat app with streaming responses."""

    CSS = """
    Screen {
        background: $surface;
    }

    #history {
        height: 1fr;
        border: solid $primary;
        scrollbar-gutter: stable;
        background: $surface;
        padding: 1;
    }

    #input {
        height: auto;
        max-height: 10;
        margin: 1;
    }

    .thinking {
        color: $warning;
        text-style: italic;
    }
    """

    BINDINGS = [
        ("ctrl+l", "clear_history", "Clear"),
        ("ctrl+s", "save_conversation", "Save"),
        ("ctrl+n", "new_conversation", "New"),
        ("ctrl+c", "quit", "Quit"),
    ]

    COMMANDS = {ChatCommands}

    def __init__(self):
        super().__init__()
        self.is_streaming = False
        self.conversation = []

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield RichLog(id="history", markup=True, auto_scroll=True, highlight=True)
            yield VimTextArea(id="input")
        yield Footer()

    def on_mount(self):
        """Initialize."""
        self.title = "Streaming Chat"
        self.query_one("#input").focus()

        history = self.query_one("#history")
        history.write("[bold cyan]Streaming Chat Application[/bold cyan]")
        history.write("Watch responses stream in token-by-token!")
        history.write("")

    async def on_vim_text_area_submitted(self, event: VimTextArea.Submitted):
        """Handle user message with streaming."""
        if self.is_streaming:
            self.notify("Please wait for current response to complete", severity="warning")
            return

        if not event.text.strip():
            return

        history = self.query_one("#history")

        # Store user message
        self.conversation.append({"role": "user", "content": event.text})

        # User message
        history.write(f"[bold cyan]You:[/bold cyan] {event.text}")

        # Show thinking indicator
        self.is_streaming = True
        thinking_msg = history.write("[dim italic]AI is thinking...[/dim italic]")

        # Stream response
        history.write("[bold green]AI:[/bold green] ", end="")

        try:
            full_response = ""
            async for token in self.stream_ai_response(event.text):
                history.write(token, end="")
                full_response += token
                await asyncio.sleep(0)  # Yield control

            history.write("")  # New line after response
            history.write("")  # Spacing

            # Store AI response
            self.conversation.append({"role": "assistant", "content": full_response})

        finally:
            self.is_streaming = False

    async def stream_ai_response(self, prompt: str):
        """Stream AI response token by token (simulated)."""
        # Simulated streaming response
        responses = [
            "I understand you're asking about: ",
            f'"{prompt}". ',
            "This is a simulated streaming response ",
            "that demonstrates how tokens would appear ",
            "one by one in a real AI conversation. ",
            "Each word appears with a small delay ",
            "to simulate the streaming behavior ",
            "of large language models. ",
            "Pretty cool, right?",
        ]

        for chunk in responses:
            # Split into words for more granular streaming
            words = chunk.split()
            for word in words:
                yield word + " "
                await asyncio.sleep(0.08)  # Simulate network delay

    def action_clear_history(self):
        """Clear chat history."""
        history = self.query_one("#history")
        history.clear()
        self.conversation = []
        self.notify("History cleared")

    def action_save_conversation(self):
        """Save conversation to file."""
        if not self.conversation:
            self.notify("No conversation to save", severity="warning")
            return

        # Create markdown export
        lines = ["# Conversation Export\n\n"]
        for msg in self.conversation:
            role = "**You**" if msg["role"] == "user" else "**AI**"
            lines.append(f"{role}: {msg['content']}\n\n")

        content = "".join(lines)

        # Save to file
        import datetime
        filename = f"conversation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        try:
            with open(filename, "w") as f:
                f.write(content)
            self.notify(f"Saved to {filename}")
        except Exception as e:
            self.notify(f"Error saving: {e}", severity="error")

    def action_new_conversation(self):
        """Start new conversation."""
        self.action_clear_history()
        self.query_one("#input").clear()

    def run_command(self, command_id: str):
        """Execute command from command palette."""
        if command_id == "clear":
            self.action_clear_history()
        elif command_id == "save":
            self.action_save_conversation()
        elif command_id == "new":
            self.action_new_conversation()


def main():
    """Run the streaming chat app."""
    app = StreamingChatApp()
    app.run()


if __name__ == "__main__":
    main()
