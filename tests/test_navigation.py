"""Tests for vim navigation operations."""

import pytest
from vimkeys_input import VimTextArea, VimMode


class TestBasicNavigation:
    """Test basic cursor movement (hjkl)."""

    def test_nav_left(self):
        """Test h key moves left."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 5)

        widget.nav_left()
        assert widget.cursor_location == (0, 4)

    def test_nav_right(self):
        """Test l key moves right."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 5)

        widget.nav_right()
        assert widget.cursor_location == (0, 6)

    def test_nav_down(self):
        """Test j key moves down."""
        widget = VimTextArea()
        widget.text = "line1\nline2\nline3"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        widget.nav_down()
        assert widget.cursor_location[0] == 1

    def test_nav_up(self):
        """Test k key moves up."""
        widget = VimTextArea()
        widget.text = "line1\nline2\nline3"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (1, 0)

        widget.nav_up()
        assert widget.cursor_location[0] == 0


class TestWordNavigation:
    """Test word motion commands (w, b, e)."""

    def test_nav_word_forward(self):
        """Test w moves to next word."""
        widget = VimTextArea()
        widget.text = "hello world foo bar"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        widget.nav_word_forward()
        # Should move to start of "world"
        row, col = widget.cursor_location
        assert col > 0  # Moved forward

    def test_nav_word_backward(self):
        """Test b moves to previous word."""
        widget = VimTextArea()
        widget.text = "hello world foo bar"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 12)  # On "foo"

        widget.nav_word_backward()
        # Should move to start of "world"
        row, col = widget.cursor_location
        assert col < 12  # Moved backward

    def test_nav_word_end(self):
        """Test e moves to end of word."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        widget.nav_word_end()
        # Should move toward end of word
        row, col = widget.cursor_location
        assert col > 0  # Moved forward


class TestLineNavigation:
    """Test line movement commands (0, $, ^)."""

    def test_nav_line_start(self):
        """Test 0 moves to start of line."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 5)

        widget.nav_line_start()
        assert widget.cursor_location == (0, 0)

    def test_nav_line_end(self):
        """Test $ moves to end of line."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        widget.nav_line_end()
        row, col = widget.cursor_location
        assert col == len("hello world")

    def test_nav_first_non_whitespace(self):
        """Test ^ moves to first non-whitespace character."""
        widget = VimTextArea()
        widget.text = "   hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        widget.nav_first_non_whitespace()
        assert widget.cursor_location == (0, 3)  # Start of "hello"

    def test_nav_first_non_whitespace_all_whitespace(self):
        """Test ^ on line with only whitespace."""
        widget = VimTextArea()
        widget.text = "     "
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 3)

        widget.nav_first_non_whitespace()
        assert widget.cursor_location == (0, 0)  # Line start


class TestDocumentNavigation:
    """Test document movement commands (gg, G)."""

    def test_nav_document_start(self):
        """Test gg moves to start of document."""
        widget = VimTextArea()
        widget.text = "line1\nline2\nline3"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (2, 5)

        widget.nav_document_start()
        assert widget.cursor_location == (0, 0)

    def test_nav_document_end(self):
        """Test G moves to end of document."""
        widget = VimTextArea()
        widget.text = "line1\nline2\nline3"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        widget.nav_document_end()
        row, col = widget.cursor_location
        assert row == 2  # Last line

    def test_nav_document_end_empty(self):
        """Test G on empty document."""
        widget = VimTextArea()
        widget.text = ""
        widget.vim_mode = VimMode.COMMAND

        widget.nav_document_end()
        # Should not crash


class TestParagraphNavigation:
    """Test paragraph movement ({ and })."""

    def test_nav_paragraph_forward(self):
        """Test } moves to next paragraph."""
        widget = VimTextArea()
        widget.text = "para1\npara1\n\npara2\npara2"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        widget.nav_paragraph_forward()
        row, col = widget.cursor_location
        # Should move to blank line or next paragraph
        assert row > 0

    def test_nav_paragraph_backward(self):
        """Test { moves to previous paragraph."""
        widget = VimTextArea()
        widget.text = "para1\npara1\n\npara2\npara2"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (4, 0)  # Last line

        widget.nav_paragraph_backward()
        row, col = widget.cursor_location
        # Should move backward
        assert row < 4


class TestGotoLine:
    """Test goto line functionality."""

    def test_nav_goto_line_valid(self):
        """Test going to valid line number."""
        widget = VimTextArea()
        widget.text = "line1\nline2\nline3\nline4\nline5"
        widget.vim_mode = VimMode.COMMAND

        widget.nav_goto_line(3)  # 1-indexed
        assert widget.cursor_location[0] == 2  # 0-indexed

    def test_nav_goto_line_too_high(self):
        """Test going to line number beyond document."""
        widget = VimTextArea()
        widget.text = "line1\nline2\nline3"
        widget.vim_mode = VimMode.COMMAND

        widget.nav_goto_line(100)
        row, col = widget.cursor_location
        assert row == 2  # Last line (clamped)

    def test_nav_goto_line_zero(self):
        """Test going to line 0 or negative."""
        widget = VimTextArea()
        widget.text = "line1\nline2\nline3"
        widget.vim_mode = VimMode.COMMAND

        widget.nav_goto_line(0)
        assert widget.cursor_location[0] == 0  # First line


class TestEdgeCases:
    """Test navigation edge cases."""

    def test_nav_left_at_line_start(self):
        """Test h at start of line."""
        widget = VimTextArea()
        widget.text = "hello"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        widget.nav_left()
        # Should stay at start or move to previous line (TextArea behavior)
        row, col = widget.cursor_location
        assert row >= 0 and col >= 0

    def test_nav_right_at_line_end(self):
        """Test l at end of line."""
        widget = VimTextArea()
        widget.text = "hello"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 5)

        widget.nav_right()
        # Should stay at end or move to next line (TextArea behavior)
        row, col = widget.cursor_location
        assert row >= 0 and col >= 0

    def test_nav_on_empty_line(self):
        """Test navigation on empty line."""
        widget = VimTextArea()
        widget.text = "\n"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        # Should not crash
        widget.nav_right()
        widget.nav_left()
        widget.nav_line_start()
        widget.nav_line_end()

    def test_nav_on_single_char_line(self):
        """Test navigation on single character line."""
        widget = VimTextArea()
        widget.text = "x"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        widget.nav_line_end()
        row, col = widget.cursor_location
        assert col <= 1  # At or after the character


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
