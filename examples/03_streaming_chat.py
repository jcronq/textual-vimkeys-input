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

from vimkeys_input import VimTextArea


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
        self.thinking_task = None
        self.display_lines = []  # Track what's shown in history

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield RichLog(id="history", markup=True, auto_scroll=True, highlight=True, wrap=True)
            yield VimTextArea(id="input")
        yield Footer()

    def on_mount(self):
        """Initialize."""
        self.title = "Streaming Chat"
        self.sub_title = ""
        self.query_one("#input").focus()

        # Add welcome messages
        self.display_lines = [
            "[bold cyan]Streaming Chat Application[/bold cyan]",
            "Watch responses stream in token-by-token!",
            "",
        ]
        self._refresh_history()

    def _refresh_history(self):
        """Refresh the history display."""
        history = self.query_one("#history")
        history.clear()
        for line in self.display_lines:
            history.write(line)

    async def animate_thinking_dots(self):
        """Animate the thinking indicator dots."""
        dots = 0
        messages = [
            "[dim italic]AI is thinking[/dim italic]",
            "[dim italic]AI is thinking.[/dim italic]",
            "[dim italic]AI is thinking..[/dim italic]",
            "[dim italic]AI is thinking...[/dim italic]",
        ]

        # Show initial message in display
        self.display_lines.append(messages[0])
        self._refresh_history()

        while self.is_streaming:
            await asyncio.sleep(0.5)  # Update every 500ms
            dots = (dots + 1) % 4

            # Update the last line with new animation frame
            self.display_lines[-1] = messages[dots]
            self._refresh_history()

    async def on_vim_text_area_submitted(self, event: VimTextArea.Submitted):
        """Handle user message with streaming."""
        if self.is_streaming:
            self.notify("Please wait for current response to complete", severity="warning")
            return

        if not event.text.strip():
            return

        # Store user message
        self.conversation.append({"role": "user", "content": event.text})

        # Add user message to display
        self.display_lines.append(f"[bold cyan]You:[/bold cyan] {event.text}")
        self._refresh_history()

        # Show animated thinking indicator
        self.is_streaming = True
        self.thinking_task = asyncio.create_task(self.animate_thinking_dots())

        try:
            full_response = ""
            async for token in self.stream_ai_response(event.text):
                # First token: stop thinking animation and start response line
                if not full_response:
                    # Stop thinking animation
                    if self.thinking_task:
                        self.thinking_task.cancel()
                        try:
                            await self.thinking_task
                        except asyncio.CancelledError:
                            pass

                    # Remove thinking line and add AI response line
                    self.display_lines = self.display_lines[:-1]  # Remove thinking line

                # Accumulate response
                full_response += token

                # Update the last line with accumulated response (or add if first token)
                if len(self.display_lines) == 0 or not self.display_lines[-1].startswith("[bold green]AI:"):
                    self.display_lines.append(f"[bold green]AI:[/bold green] {full_response}")
                else:
                    self.display_lines[-1] = f"[bold green]AI:[/bold green] {full_response}"

                # Refresh to show new token
                self._refresh_history()
                await asyncio.sleep(0)  # Yield control

            self.is_streaming = False

            # Add spacing after response
            self.display_lines.append("")
            self._refresh_history()

            # Store AI response
            self.conversation.append({"role": "assistant", "content": full_response})

        except Exception:
            self.is_streaming = False
            if self.thinking_task:
                self.thinking_task.cancel()
            # Remove thinking line on error
            if self.display_lines and "thinking" in self.display_lines[-1]:
                self.display_lines = self.display_lines[:-1]
            self._refresh_history()
            raise

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
        self.display_lines = []
        self.conversation = []
        self._refresh_history()
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
