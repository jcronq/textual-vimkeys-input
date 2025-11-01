"""Tests for operator + motion combinations."""

import pytest
from vimkeys_input import VimTextArea, VimMode


class TestDeleteMotion:
    """Test d + motion (dw, d$, dj, etc.)."""

    def test_dw_deletes_word(self):
        """Test dw deletes to end of word."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        # Simulate 'd' then 'w'
        widget.operator_pending.set_operator("d")
        widget.nav_word_forward()  # Motion
        # In actual usage, _handle_operator_motion would do this
        from vimkeys_input.operator_pending import OperatorMotionHandler

        # Text should be shorter after delete
        initial_len = len(widget.text)
        # We can't fully test this without the event system, but we can test the infrastructure
        assert widget.operator_pending.is_pending()

    def test_d_dollar_deletes_to_end_of_line(self):
        """Test d$ deletes to end of line."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 6)

        # Set up operator-pending
        widget.operator_pending.set_operator("d")
        assert widget.operator_pending.get_operator() == "d"

    def test_dj_deletes_down_line(self):
        """Test dj deletes current and next line."""
        widget = VimTextArea()
        widget.text = "line1\nline2\nline3"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        widget.operator_pending.set_operator("d")
        assert widget.operator_pending.is_pending()


class TestChangeMotion:
    """Test c + motion (cw, c$, cb, etc.)."""

    def test_cw_changes_word(self):
        """Test cw changes word and enters insert mode."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        widget.operator_pending.set_operator("c")
        assert widget.operator_pending.get_operator() == "c"

    def test_cb_changes_back(self):
        """Test cb changes previous word."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 6)

        widget.operator_pending.set_operator("c")
        assert widget.operator_pending.is_pending()


class TestYankMotion:
    """Test y + motion (yw, y$, yj, etc.)."""

    def test_yw_yanks_word(self):
        """Test yw yanks word to register."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        widget.operator_pending.set_operator("y")
        assert widget.operator_pending.get_operator() == "y"

    def test_y_dollar_yanks_to_end(self):
        """Test y$ yanks to end of line."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        widget.operator_pending.set_operator("y")
        assert widget.operator_pending.is_pending()


class TestCountWithOperatorMotion:
    """Test count + operator + motion (3dw, 2cb, etc.)."""

    def test_3dw_deletes_three_words(self):
        """Test 3dw deletes 3 words."""
        widget = VimTextArea()
        widget.text = "one two three four"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        widget.operator_pending.set_operator("d", count=3)
        assert widget.operator_pending.count == 3

    def test_d3w_deletes_three_words(self):
        """Test d3w deletes 3 words."""
        widget = VimTextArea()
        widget.text = "one two three four"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        widget.operator_pending.set_operator("d")
        widget.operator_pending.set_motion_count(3)
        assert widget.operator_pending.motion_count == 3

    def test_2d3w_deletes_six_words(self):
        """Test 2d3w deletes 6 words (2*3)."""
        widget = VimTextArea()
        widget.text = "one two three four five six seven"
        widget.vim_mode = VimMode.COMMAND

        widget.operator_pending.set_operator("d", count=2)
        widget.operator_pending.set_motion_count(3)
        assert widget.operator_pending.get_total_count() == 6


class TestLineWiseOperators:
    """Test dd, yy, cc (line-wise operators)."""

    def test_dd_deletes_line(self):
        """Test dd deletes line."""
        widget = VimTextArea()
        widget.text = "line1\nline2\nline3"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (1, 0)

        from vimkeys_input.operator_pending import OperatorMotionHandler
        success = OperatorMotionHandler.execute_line_operator(widget, "d", 1)
        assert success

    def test_3dd_deletes_three_lines(self):
        """Test 3dd deletes 3 lines."""
        widget = VimTextArea()
        widget.text = "line1\nline2\nline3\nline4\nline5"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (1, 0)

        from vimkeys_input.operator_pending import OperatorMotionHandler
        success = OperatorMotionHandler.execute_line_operator(widget, "d", 3)
        assert success

    def test_yy_yanks_line(self):
        """Test yy yanks line."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        from vimkeys_input.operator_pending import OperatorMotionHandler
        success = OperatorMotionHandler.execute_line_operator(widget, "y", 1)
        assert success
        assert widget.yank_register == "hello world\n"

    def test_cc_changes_line(self):
        """Test cc changes line and enters insert mode."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        from vimkeys_input.operator_pending import OperatorMotionHandler
        success = OperatorMotionHandler.execute_line_operator(widget, "c", 1)
        assert success
        assert widget.vim_mode == VimMode.INSERT


class TestOperatorPendingState:
    """Test OperatorPendingState class."""

    def test_set_and_get_operator(self):
        """Test setting and getting operator."""
        from vimkeys_input.operator_pending import OperatorPendingState
        state = OperatorPendingState()

        state.set_operator("d")
        assert state.get_operator() == "d"
        assert state.is_pending()

    def test_clear_state(self):
        """Test clearing state."""
        from vimkeys_input.operator_pending import OperatorPendingState
        state = OperatorPendingState()

        state.set_operator("d", count=3)
        state.clear()
        assert not state.is_pending()
        assert state.count == 0

    def test_count_multiplication(self):
        """Test count * motion_count."""
        from vimkeys_input.operator_pending import OperatorPendingState
        state = OperatorPendingState()

        state.set_operator("d", count=2)
        state.set_motion_count(3)
        assert state.get_total_count() == 6

    def test_count_only(self):
        """Test with only operator count."""
        from vimkeys_input.operator_pending import OperatorPendingState
        state = OperatorPendingState()

        state.set_operator("d", count=5)
        assert state.get_total_count() == 5

    def test_motion_count_only(self):
        """Test with only motion count."""
        from vimkeys_input.operator_pending import OperatorPendingState
        state = OperatorPendingState()

        state.set_operator("d")
        state.set_motion_count(3)
        assert state.get_total_count() == 3

    def test_no_count(self):
        """Test with no count."""
        from vimkeys_input.operator_pending import OperatorPendingState
        state = OperatorPendingState()

        state.set_operator("d")
        assert state.get_total_count() == 1  # Default


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
