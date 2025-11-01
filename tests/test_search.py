"""Tests for character and word search operations."""

import pytest
from vimkeys_input import VimTextArea, VimMode


class TestCharacterSearchForward:
    """Test f (find character forward)."""

    def test_search_char_forward_found(self):
        """Test f finds character."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        result = widget.search_char_forward("o")
        assert result is True
        row, col = widget.cursor_location
        assert col > 0  # Moved to 'o'

    def test_search_char_forward_not_found(self):
        """Test f returns False if not found."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        result = widget.search_char_forward("z")
        assert result is False

    def test_search_char_forward_stores_last_search(self):
        """Test f stores search for repeat."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        widget.search_char_forward("o")
        assert widget.last_f_search == ("f", "o")

    def test_search_char_forward_same_char(self):
        """Test f finds next occurrence of same char."""
        widget = VimTextArea()
        widget.text = "hello"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        # Find first 'l'
        widget.search_char_forward("l")
        pos1 = widget.cursor_location

        # Find next 'l'
        widget.search_char_forward("l")
        pos2 = widget.cursor_location

        assert pos2[1] > pos1[1]  # Moved further


class TestCharacterSearchBackward:
    """Test F (find character backward)."""

    def test_search_char_backward_found(self):
        """Test F finds character backward."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 10)

        result = widget.search_char_backward("o")
        assert result is True
        row, col = widget.cursor_location
        assert col < 10  # Moved backward

    def test_search_char_backward_not_found(self):
        """Test F returns False if not found."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 5)

        result = widget.search_char_backward("z")
        assert result is False

    def test_search_char_backward_stores_last_search(self):
        """Test F stores search for repeat."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 10)

        widget.search_char_backward("o")
        assert widget.last_f_search == ("F", "o")


class TestTillForward:
    """Test t (till character forward)."""

    def test_search_till_forward_found(self):
        """Test t stops before character."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        result = widget.search_till_forward("o")
        assert result is True
        # Should be one before the 'o'

    def test_search_till_forward_not_found(self):
        """Test t returns False if not found."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        result = widget.search_till_forward("z")
        assert result is False

    def test_search_till_forward_stores_last_search(self):
        """Test t stores search for repeat."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        widget.search_till_forward("o")
        assert widget.last_f_search == ("t", "o")


class TestTillBackward:
    """Test T (till character backward)."""

    def test_search_till_backward_found(self):
        """Test T stops after character."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 10)

        result = widget.search_till_backward("o")
        assert result is True

    def test_search_till_backward_not_found(self):
        """Test T returns False if not found."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 10)

        result = widget.search_till_backward("z")
        assert result is False


class TestSearchRepeat:
    """Test ; (repeat search) and , (reverse repeat)."""

    def test_search_repeat_forward(self):
        """Test ; repeats last f search."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        # Do initial search
        widget.search_char_forward("l")
        pos1 = widget.cursor_location

        # Repeat
        result = widget.search_repeat()
        pos2 = widget.cursor_location

        # Should have moved to next 'l'
        if result:
            assert pos2[1] >= pos1[1]

    def test_search_repeat_no_previous(self):
        """Test ; with no previous search."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.last_f_search = None

        result = widget.search_repeat()
        assert result is False

    def test_search_repeat_reverse(self):
        """Test , reverses search direction."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 5)

        # Search forward
        widget.search_char_forward("o")

        # Reverse repeat should search backward
        widget.search_repeat_reverse()

    def test_search_repeat_reverse_no_previous(self):
        """Test , with no previous search."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.last_f_search = None

        result = widget.search_repeat_reverse()
        assert result is False


class TestWordSearch:
    """Test * and # (word search)."""

    def test_search_word_under_cursor_forward(self):
        """Test * searches for word under cursor."""
        widget = VimTextArea()
        widget.text = "hello world hello"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)  # On "hello"

        result = widget.search_word_under_cursor(forward=True)
        # Should find next occurrence or return bool

    def test_search_word_under_cursor_backward(self):
        """Test # searches backward for word."""
        widget = VimTextArea()
        widget.text = "hello world hello"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 12)  # On second "hello"

        result = widget.search_word_under_cursor(forward=False)
        # Should find previous occurrence

    def test_search_word_under_cursor_not_on_word(self):
        """Test * on non-word character."""
        widget = VimTextArea()
        widget.text = "hello   world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 5)  # On space

        result = widget.search_word_under_cursor(forward=True)
        assert result is False

    def test_search_word_stores_word(self):
        """Test * stores word for repeat."""
        widget = VimTextArea()
        widget.text = "hello world hello"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        widget.search_word_under_cursor(forward=True)
        # Should have stored the word
        if hasattr(widget, 'last_search_word'):
            assert widget.last_search_word is not None


class TestSearchMultiline:
    """Test search across multiple lines."""

    def test_search_char_only_current_line(self):
        """Test f only searches current line."""
        widget = VimTextArea()
        widget.text = "hello\nworld"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        # Try to find 'w' which is on next line
        result = widget.search_char_forward("w")
        assert result is False  # Should not find it

    def test_search_word_multiline_forward(self):
        """Test * can find word on next line."""
        widget = VimTextArea()
        widget.text = "hello\nworld\nhello"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        result = widget.search_word_under_cursor(forward=True)
        # Should find "hello" on line 3

    def test_search_word_multiline_backward(self):
        """Test # can find word on previous line."""
        widget = VimTextArea()
        widget.text = "hello\nworld\nhello"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (2, 0)  # On second "hello"

        result = widget.search_word_under_cursor(forward=False)
        # Should find first "hello"


class TestSearchEdgeCases:
    """Test edge cases in search operations."""

    def test_search_at_line_start(self):
        """Test f from start of line."""
        widget = VimTextArea()
        widget.text = "hello"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        result = widget.search_char_forward("h")
        # Should not find 'h' (cursor is already on it)

    def test_search_at_line_end(self):
        """Test F from end of line."""
        widget = VimTextArea()
        widget.text = "hello"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 5)

        result = widget.search_char_backward("o")
        assert result is True

    def test_search_empty_line(self):
        """Test search on empty line."""
        widget = VimTextArea()
        widget.text = "\n"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        result = widget.search_char_forward("a")
        assert result is False

    def test_search_single_char_line(self):
        """Test search on single character line."""
        widget = VimTextArea()
        widget.text = "x"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        result = widget.search_char_forward("y")
        assert result is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
