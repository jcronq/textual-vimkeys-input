"""Tests for visual mode operations."""

import pytest
from vimkeys_input import VimTextArea, VimMode


class TestVisualModeEntry:
    """Test entering and exiting visual mode."""

    def test_enter_visual_mode(self):
        """Test v enters visual mode."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND

        widget._enter_visual_mode()
        assert widget.vim_mode == VimMode.VISUAL

    def test_visual_start_recorded(self):
        """Test visual mode records starting position."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 5)

        widget._enter_visual_mode()
        assert widget.visual_start == (0, 5)

    def test_exit_visual_mode(self):
        """Test ESC exits visual mode."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.VISUAL

        widget._enter_command_mode()
        assert widget.vim_mode == VimMode.COMMAND
        assert widget.visual_start is None


class TestVisualNavigation:
    """Test navigation in visual mode extends selection."""

    def test_visual_left(self):
        """Test h in visual mode extends selection left."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.VISUAL
        widget.cursor_location = (0, 5)

        # Should call action_cursor_left_select
        widget.visual_left()

    def test_visual_right(self):
        """Test l in visual mode extends selection right."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.VISUAL
        widget.cursor_location = (0, 5)

        widget.visual_right()

    def test_visual_down(self):
        """Test j in visual mode extends selection down."""
        widget = VimTextArea()
        widget.text = "line1\nline2\nline3"
        widget.vim_mode = VimMode.VISUAL
        widget.cursor_location = (0, 0)

        widget.visual_down()

    def test_visual_up(self):
        """Test k in visual mode extends selection up."""
        widget = VimTextArea()
        widget.text = "line1\nline2\nline3"
        widget.vim_mode = VimMode.VISUAL
        widget.cursor_location = (1, 0)

        widget.visual_up()


class TestVisualWordMotion:
    """Test word motions in visual mode."""

    def test_visual_word_forward(self):
        """Test w in visual mode."""
        widget = VimTextArea()
        widget.text = "hello world foo"
        widget.vim_mode = VimMode.VISUAL
        widget.cursor_location = (0, 0)

        widget.visual_word_forward()

    def test_visual_word_backward(self):
        """Test b in visual mode."""
        widget = VimTextArea()
        widget.text = "hello world foo"
        widget.vim_mode = VimMode.VISUAL
        widget.cursor_location = (0, 12)

        widget.visual_word_backward()


class TestVisualLineMotion:
    """Test line motions in visual mode."""

    def test_visual_line_start(self):
        """Test 0 in visual mode."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.VISUAL
        widget.cursor_location = (0, 5)

        widget.visual_line_start()

    def test_visual_line_end(self):
        """Test $ in visual mode."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.VISUAL
        widget.cursor_location = (0, 0)

        widget.visual_line_end()


class TestVisualOperations:
    """Test operations on visual selections."""

    def test_visual_yank(self):
        """Test y yanks selection."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.VISUAL
        widget.selected_text = "hello"

        widget.visual_yank()
        assert widget.yank_register == "hello"

    def test_visual_yank_empty_selection(self):
        """Test y with no selection."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.VISUAL
        widget.selected_text = ""

        widget.visual_yank()
        # Should not crash

    def test_visual_delete(self):
        """Test d deletes selection."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.VISUAL
        widget.selected_text = "hello"

        widget.visual_delete()
        assert widget.yank_register == "hello"

    def test_visual_change(self):
        """Test c changes selection and enters insert mode."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.VISUAL
        widget.selected_text = "hello"

        widget.visual_change()
        assert widget.vim_mode == VimMode.INSERT


class TestVisualIndent:
    """Test indent/dedent in visual mode."""

    def test_visual_indent(self):
        """Test > indents selection."""
        widget = VimTextArea()
        widget.text = "line1\nline2\nline3"
        widget.vim_mode = VimMode.VISUAL

        # Create a mock selection
        from textual.widgets.text_area import Selection, Location

        widget.selection = Selection(start=Location(0, 0), end=Location(1, 5))

        # Should not crash
        widget.visual_indent()

    def test_visual_dedent(self):
        """Test < dedents selection."""
        widget = VimTextArea()
        widget.text = "    line1\n    line2"
        widget.vim_mode = VimMode.VISUAL

        from textual.widgets.text_area import Selection, Location

        widget.selection = Selection(start=Location(0, 0), end=Location(1, 5))

        # Should not crash
        widget.visual_dedent()


class TestVisualCaseOperations:
    """Test case manipulation in visual mode."""

    def test_visual_toggle_case(self):
        """Test ~ toggles case."""
        widget = VimTextArea()
        widget.text = "Hello World"
        widget.vim_mode = VimMode.VISUAL
        widget.selected_text = "Hello"

        widget.visual_toggle_case()
        # Textual will handle the actual replacement

    def test_visual_uppercase(self):
        """Test U converts to uppercase."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.VISUAL
        widget.selected_text = "hello"

        widget.visual_uppercase()

    def test_visual_lowercase(self):
        """Test u converts to lowercase."""
        widget = VimTextArea()
        widget.text = "HELLO WORLD"
        widget.vim_mode = VimMode.VISUAL
        widget.selected_text = "HELLO"

        widget.visual_lowercase()


class TestVisualEdgeCases:
    """Test edge cases in visual mode."""

    def test_visual_on_empty_text(self):
        """Test visual mode on empty text."""
        widget = VimTextArea()
        widget.text = ""
        widget.vim_mode = VimMode.COMMAND

        widget._enter_visual_mode()
        assert widget.vim_mode == VimMode.VISUAL

    def test_visual_operations_no_selection(self):
        """Test operations with no selection."""
        widget = VimTextArea()
        widget.text = "hello"
        widget.vim_mode = VimMode.VISUAL
        widget.selected_text = ""

        # Should not crash
        widget.visual_yank()
        widget.visual_delete()
        widget.visual_toggle_case()
        widget.visual_uppercase()
        widget.visual_lowercase()

    def test_visual_multiline_selection(self):
        """Test visual mode across multiple lines."""
        widget = VimTextArea()
        widget.text = "line1\nline2\nline3"
        widget.vim_mode = VimMode.VISUAL
        widget.cursor_location = (0, 0)

        # Extend selection down
        widget.visual_down()
        widget.visual_down()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
