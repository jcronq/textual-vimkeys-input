"""Marks system for vim.

Marks allow saving and jumping to positions in the document.
Examples:
    - ma: set mark 'a' at current position
    - 'a: jump to line of mark 'a'
    - `a: jump to exact position of mark 'a'
"""

from typing import Dict, Tuple, Optional


class MarksManager:
    """Manages vim marks (bookmarks in the document)."""

    def __init__(self):
        # Dict of mark_name -> (row, col)
        self.marks: Dict[str, Tuple[int, int]] = {}

    def set_mark(self, name: str, position: Tuple[int, int]) -> None:
        """Set a mark at the given position.

        Args:
            name: Single character mark name (a-z, A-Z)
            position: (row, col) tuple
        """
        if len(name) != 1:
            return

        # Only allow letter marks
        if not name.isalpha():
            return

        self.marks[name] = position

    def get_mark(self, name: str) -> Optional[Tuple[int, int]]:
        """Get the position of a mark.

        Args:
            name: Single character mark name

        Returns:
            (row, col) tuple or None if mark doesn't exist
        """
        return self.marks.get(name)

    def has_mark(self, name: str) -> bool:
        """Check if a mark exists.

        Args:
            name: Single character mark name

        Returns:
            True if mark exists
        """
        return name in self.marks

    def delete_mark(self, name: str) -> None:
        """Delete a mark.

        Args:
            name: Single character mark name
        """
        if name in self.marks:
            del self.marks[name]

    def clear_all(self) -> None:
        """Clear all marks."""
        self.marks.clear()

    def list_marks(self) -> Dict[str, Tuple[int, int]]:
        """Get all marks.

        Returns:
            Dictionary of mark_name -> position
        """
        return self.marks.copy()
