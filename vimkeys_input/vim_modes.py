"""Vim editing modes and mode indicators."""

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
