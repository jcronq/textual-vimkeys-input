"""Count/number handling for vim commands.

Vim allows counts before commands: 5j, 3dd, 2w, etc.
This module provides the CountHandler to manage count state.
"""


class CountHandler:
    """Handles count/number input for vim commands.

    Examples:
        5j - move down 5 lines
        3dd - delete 3 lines
        2w - move 2 words forward
        10G - go to line 10
    """

    def __init__(self):
        self.count = 0
        self.count_str = ""

    def add_digit(self, digit: str) -> None:
        """Add a digit to the current count.

        Args:
            digit: Single digit character ('0'-'9')
        """
        if not digit.isdigit():
            return

        # Special case: leading 0 is not allowed (would be line start command)
        if digit == "0" and self.count_str == "":
            return

        self.count_str += digit
        self.count = int(self.count_str)

    def get_count(self, default: int = 1) -> int:
        """Get the current count, or default if no count entered.

        Args:
            default: Value to return if no count (usually 1)

        Returns:
            The count value, or default if none entered
        """
        if self.count == 0:
            return default
        return self.count

    def has_count(self) -> bool:
        """Check if a count has been entered.

        Returns:
            True if count > 0
        """
        return self.count > 0

    def clear(self) -> None:
        """Clear the current count."""
        self.count = 0
        self.count_str = ""

    def __str__(self) -> str:
        """String representation for display.

        Returns:
            Count string or empty string
        """
        return self.count_str

    def __repr__(self) -> str:
        """Debug representation.

        Returns:
            Debug string
        """
        return f"CountHandler(count={self.count})"
