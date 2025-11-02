"""Spike example - basic VimTextArea demonstration.

This is a minimal example to validate the VimTextArea widget works correctly.
- Test mode switching (ESC to command, i to insert)
- Test hjkl navigation
- Test basic editing
"""

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Vertical
import sys
import os

# Add parent directory to path so we can import vimkeys_input
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from vimkeys_input import VimTextArea, VimMode


class SpikeApp(App):
    """Minimal spike test app for VimTextArea."""

    CSS = """
    Screen {
        background: $surface;
    }

    #mode-display {
        height: 1;
        background: $panel;
        padding: 0 2;
        text-align: center;
        text-style: bold;
    }

    #instructions {
        height: auto;
        background: $panel;
        padding: 1 2;
        margin: 1;
        border: solid $primary;
    }

    #input {
        height: auto;
        min-height: 10;
        max-height: 20;
        margin: 1 2;
    }

    #output {
        height: auto;
        background: $panel;
        padding: 1 2;
        margin: 1 2;
        border: solid $accent;
    }
    """

    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        """Create layout."""
        yield Header()
        yield Static("-- INSERT --", id="mode-display")
        yield Static(
            "[bold cyan]VimTextArea Spike Test[/bold cyan]\n\n"
            "Commands:\n"
            "  ESC - Enter command mode\n"
            "  i/a/o - Enter insert mode\n"
            "  hjkl - Navigate (command mode)\n"
            "  0/$ - Line start/end (command mode)\n"
            "  gg/G - Document start/end (command mode)\n"
            "  dd - Delete line\n"
            "  yy/p - Copy/paste line\n"
            "  v - Visual mode\n"
            "  Enter - Submit (insert mode)\n",
            id="instructions",
            markup=True,
        )
        with Vertical():
            yield VimTextArea(id="input", language="markdown")
            yield Static(
                "Output will appear here after you press Enter in insert mode.", id="output"
            )
        yield Footer()

    def on_mount(self):
        """Initialize on mount."""
        self.title = "VimTextArea Spike"
        self.query_one("#input").focus()

    def on_vim_text_area_mode_changed(self, event: VimTextArea.ModeChanged):
        """Update mode display when mode changes."""
        mode_display = self.query_one("#mode-display")

        mode_text = {
            VimMode.INSERT: "[green]-- INSERT --[/green]",
            VimMode.COMMAND: "[blue]-- COMMAND --[/blue]",
            VimMode.VISUAL: "[yellow]-- VISUAL --[/yellow]",
        }.get(event.mode, "-- UNKNOWN --")

        mode_display.update(mode_text)

    def on_vim_text_area_submitted(self, event: VimTextArea.Submitted):
        """Handle text submission."""
        output = self.query_one("#output")
        output.update(
            f"[bold cyan]Submitted:[/bold cyan]\n{event.text}\n\n"
            f"[dim]Text has {len(event.text)} characters, "
            f"{len(event.text.splitlines())} lines[/dim]"
        )


def main():
    """Run the spike app."""
    app = SpikeApp()
    app.run()


if __name__ == "__main__":
    main()
