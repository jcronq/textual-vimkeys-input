"""Operator-pending mode for vim operator + motion combinations.

Vim allows combining operators with motions:
- Operators: d (delete), c (change), y (yank), > (indent), < (dedent)
- Motions: w, b, e, $, 0, j, k, h, l, f, t, etc.

Examples:
    - dw: delete word
    - d$: delete to end of line
    - cb: change back (delete previous word + insert)
    - c3w: change 3 words
    - y$: yank to end of line
    - >j: indent current and next line
"""

from typing import Optional, Tuple, Callable


class OperatorPendingState:
    """Manages operator-pending mode state.

    When an operator is pressed (d, c, y), we enter operator-pending mode
    and wait for a motion to complete the command.
    """

    def __init__(self):
        self.operator: Optional[str] = None  # Current operator (d, c, y, >, <)
        self.count: int = 0  # Count before operator (3d)
        self.motion_count: int = 0  # Count after operator (d3w)

    def set_operator(self, operator: str, count: int = 0) -> None:
        """Set the pending operator.

        Args:
            operator: The operator character (d, c, y, >, <)
            count: Optional count before operator (3d)
        """
        self.operator = operator
        self.count = count

    def is_pending(self) -> bool:
        """Check if we're waiting for a motion.

        Returns:
            True if operator is set
        """
        return self.operator is not None

    def clear(self) -> None:
        """Clear operator-pending state."""
        self.operator = None
        self.count = 0
        self.motion_count = 0

    def get_operator(self) -> Optional[str]:
        """Get the current operator.

        Returns:
            The operator character or None
        """
        return self.operator

    def get_total_count(self) -> int:
        """Get the total count (operator count * motion count).

        If 3d2w, returns 6 (delete 6 words).
        If just 3d, returns 3.
        If just d2w, returns 2.

        Returns:
            Total count, minimum 1
        """
        if self.count > 0 and self.motion_count > 0:
            return self.count * self.motion_count
        elif self.count > 0:
            return self.count
        elif self.motion_count > 0:
            return self.motion_count
        else:
            return 1

    def set_motion_count(self, count: int) -> None:
        """Set the count entered after the operator.

        Args:
            count: Count after operator (d3w)
        """
        self.motion_count = count


class OperatorMotionHandler:
    """Handles execution of operator + motion combinations."""

    @staticmethod
    def execute_operator_motion(widget, operator: str, motion_func: Callable, count: int = 1) -> bool:
        """Execute an operator + motion combination.

        Args:
            widget: The VimTextArea widget
            operator: The operator (d, c, y, >, <)
            motion_func: The motion function to execute
            count: How many times to repeat the motion

        Returns:
            True if operation succeeded
        """
        # Save starting position
        start_pos = widget.cursor_location

        # Execute the motion to find the end position
        for _ in range(count):
            motion_func()

        end_pos = widget.cursor_location

        # If no movement, do nothing
        if start_pos == end_pos:
            return False

        # Now perform the operator on the range
        return OperatorMotionHandler._apply_operator(
            widget, operator, start_pos, end_pos
        )

    @staticmethod
    def _apply_operator(widget, operator: str, start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> bool:
        """Apply an operator to a range.

        Args:
            widget: The VimTextArea widget
            operator: The operator character
            start_pos: Starting (row, col)
            end_pos: Ending (row, col)

        Returns:
            True if operation succeeded
        """
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Handle same-line operations
        if start_row == end_row:
            # Make sure start is before end
            if start_col > end_col:
                start_col, end_col = end_col, start_col

            line = str(widget.get_line(start_row))
            affected_text = line[start_col:end_col]

            if operator == 'd':  # Delete
                widget.yank_register = affected_text
                widget.cursor_location = (start_row, start_col)
                for _ in range(end_col - start_col):
                    widget.action_delete_right()
                return True

            elif operator == 'c':  # Change (delete + insert mode)
                widget.yank_register = affected_text
                widget.cursor_location = (start_row, start_col)
                for _ in range(end_col - start_col):
                    widget.action_delete_right()
                widget._enter_insert_mode()
                return True

            elif operator == 'y':  # Yank (copy)
                widget.yank_register = affected_text
                widget.cursor_location = start_pos  # Stay at start
                return True

        # TODO: Multi-line operator + motion
        # For now, handle simple case
        return False

    @staticmethod
    def execute_line_operator(widget, operator: str, count: int = 1) -> bool:
        """Execute a line-wise operator (dd, yy, cc).

        Args:
            widget: The VimTextArea widget
            operator: The operator character
            count: Number of lines

        Returns:
            True if operation succeeded
        """
        if operator == 'd':
            for _ in range(count):
                widget.edit_delete_line()
            return True
        elif operator == 'y':
            # For multiple lines, yank them all
            row, col = widget.cursor_location
            lines = []
            for i in range(count):
                if row + i < widget.document.line_count:
                    lines.append(str(widget.get_line(row + i)))
            widget.yank_register = '\n'.join(lines) + '\n'
            return True
        elif operator == 'c':
            for _ in range(count):
                widget.edit_delete_line()
            widget._enter_insert_mode()
            return True
        return False
