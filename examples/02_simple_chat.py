"""Simple chat application using VimTextArea.

A basic chat interface demonstrating:
- Message input with vim keybindings
- Message history display
- Simple echo bot responses
"""

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, RichLog
from textual.containers import Vertical
import sys
import os

# Add parent directory to path so we can import vimkeys_input
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from vimkeys_input import VimTextArea


class SimpleChatApp(App):
    """Simple chat application."""

    CSS = """
    Screen {
        background: $surface;
    }

    #history {
        height: 1fr;
        border: solid $primary;
        padding: 1;
        background: $surface;
    }

    #input {
        height: auto;
        max-height: 10;
        margin: 1;
    }

    #mode-indicator {
        height: 1;
        background: $panel;
        padding: 0 2;
        text-align: center;
    }

    .user-message {
        color: $text;
    }

    .ai-message {
        color: $success;
    }
    """

    BINDINGS = [
        ("ctrl+l", "clear_history", "Clear"),
        ("ctrl+c", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        """Create layout."""
        yield Header()
        with Vertical():
            yield RichLog(id="history", markup=True, highlight=True, auto_scroll=True)
            yield VimTextArea(id="input", language="markdown")
        yield Footer()

    def on_mount(self):
        """Initialize on mount."""
        self.title = "Simple Chat with VimTextArea"
        self.query_one("#input").focus()
        self.message_count = 0

        # Welcome message
        history = self.query_one("#history")
        history.write("[bold cyan]Welcome to Simple Chat![/bold cyan]")
        history.write("Type your message and press Enter in insert mode to send.")
        history.write("Use vim keybindings for editing (ESC for command mode, i for insert).")
        history.write("")

    def on_vim_text_area_submitted(self, event: VimTextArea.Submitted):
        """Handle user message."""
        history = self.query_one("#history")

        # Don't process empty messages
        if not event.text.strip():
            return

        self.message_count += 1

        # Display user message
        history.write(f"[bold cyan]You:[/bold cyan] {event.text}")

        # Simple echo bot response
        response = self.get_bot_response(event.text)
        history.write(f"[bold green]Bot:[/bold green] {response}")
        history.write("")  # Add spacing

    def get_bot_response(self, prompt: str) -> str:
        """Get bot response (simple echo bot for now)."""
        # Simple responses based on content
        prompt_lower = prompt.lower()

        if "hello" in prompt_lower or "hi" in prompt_lower:
            return "Hello! How can I help you today?"
        elif "how are you" in prompt_lower:
            return "I'm doing great! Thanks for asking. How are you?"
        elif "bye" in prompt_lower or "goodbye" in prompt_lower:
            return "Goodbye! Have a great day!"
        elif "?" in prompt:
            return f"That's a great question about: '{prompt}'. Let me think about that..."
        else:
            return f"You said: {prompt}. Interesting!"

    def action_clear_history(self):
        """Clear chat history."""
        history = self.query_one("#history")
        history.clear()
        self.message_count = 0
        history.write("[dim]History cleared[/dim]")


def main():
    """Run the chat app."""
    app = SimpleChatApp()
    app.run()


if __name__ == "__main__":
    main()
