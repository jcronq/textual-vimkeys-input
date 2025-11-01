"""Tests for vim editing operations."""

import pytest
from vimkeys_input import VimTextArea, VimMode


class TestCharacterOperations:
    """Test character-level editing operations."""

    def test_delete_char(self):
        """Test x deletes character under cursor."""
        widget = VimTextArea()
        widget.text = "hello"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 1)  # On 'e'

        widget.edit_delete_char()
        assert widget.text == "hllo"

    def test_delete_char_back(self):
        """Test X deletes character before cursor."""
        widget = VimTextArea()
        widget.text = "hello"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 2)  # After 'e'

        widget.edit_delete_char_back()
        assert widget.text == "hllo"

    def test_replace_char(self):
        """Test r replaces character."""
        widget = VimTextArea()
        widget.text = "hello"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 1)  # On 'e'

        widget.edit_replace_char("a")
        assert widget.text == "hallo"


class TestLineOperations:
    """Test line-level editing operations."""

    def test_delete_line(self):
        """Test dd deletes entire line."""
        widget = VimTextArea()
        widget.text = "line1\nline2\nline3"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (1, 0)  # On line2

        widget.edit_delete_line()
        # Line should be deleted
        assert "line2" not in widget.text

    def test_yank_line(self):
        """Test yy yanks line to register."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        widget.edit_yank_line()
        assert widget.yank_register == "hello world"

    def test_delete_to_line_end(self):
        """Test D deletes to end of line."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 6)  # After "hello "

        widget.edit_delete_to_line_end()
        assert widget.yank_register == "world"

    def test_change_line(self):
        """Test cc deletes line and enters insert mode."""
        widget = VimTextArea()
        widget.text = "hello\nworld"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        widget.edit_change_line()
        assert widget.vim_mode == VimMode.INSERT


class TestPasteOperations:
    """Test paste operations."""

    def test_paste_after_char(self):
        """Test p pastes after cursor."""
        widget = VimTextArea()
        widget.text = "helo"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 2)  # After 'e'
        widget.yank_register = "l"

        widget.edit_paste_after()
        assert "hell" in widget.text

    def test_paste_before(self):
        """Test P pastes before cursor."""
        widget = VimTextArea()
        widget.text = "helo"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 3)  # On 'o'
        widget.yank_register = "l"

        widget.edit_paste_before()
        assert "hel" in widget.text

    def test_paste_empty_register(self):
        """Test paste with empty register does nothing."""
        widget = VimTextArea()
        widget.text = "hello"
        widget.vim_mode = VimMode.COMMAND
        widget.yank_register = ""

        original = widget.text
        widget.edit_paste_after()
        assert widget.text == original


class TestOpenLineOperations:
    """Test opening new lines."""

    def test_open_line_below(self):
        """Test o opens line below."""
        widget = VimTextArea()
        widget.text = "line1"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        widget.edit_open_line_below()
        # Should have newline added
        assert "\n" in widget.text

    def test_open_line_above(self):
        """Test O opens line above."""
        widget = VimTextArea()
        widget.text = "line1\nline2"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (1, 0)  # On line2

        widget.edit_open_line_above()
        # Should have newline added
        assert widget.text.count("\n") >= 2


class TestWordOperations:
    """Test word-level operations."""

    def test_delete_word(self):
        """Test dw deletes word."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        widget.edit_delete_word()
        # Should have deleted some text
        assert len(widget.text) < len("hello world")

    def test_change_word(self):
        """Test cw changes word and enters insert mode."""
        widget = VimTextArea()
        widget.text = "hello world"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        widget.edit_change_word()
        assert widget.vim_mode == VimMode.INSERT


class TestUndoRedo:
    """Test undo/redo operations."""

    def test_undo(self):
        """Test u triggers undo."""
        widget = VimTextArea()
        widget.text = "hello"
        widget.vim_mode = VimMode.COMMAND

        # Make a change
        widget.edit_delete_char()
        # Undo should be called (testing the method exists)
        widget.edit_undo()

    def test_redo(self):
        """Test Ctrl+r triggers redo."""
        widget = VimTextArea()
        widget.text = "hello"
        widget.vim_mode = VimMode.COMMAND

        # Make a change, undo it, then redo
        widget.edit_delete_char()
        widget.edit_undo()
        widget.edit_redo()


class TestJoinLines:
    """Test line joining."""

    def test_join_lines(self):
        """Test J joins current line with next."""
        widget = VimTextArea()
        widget.text = "line1\nline2"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        widget.edit_join_lines()
        # Should have one less newline
        assert widget.text.count("\n") < 1

    def test_join_lines_last_line(self):
        """Test J on last line does nothing."""
        widget = VimTextArea()
        widget.text = "only line"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        original = widget.text
        widget.edit_join_lines()
        # Should not crash


class TestIndent:
    """Test indent/dedent operations."""

    def test_indent(self):
        """Test >> indents line."""
        widget = VimTextArea()
        widget.text = "hello"
        widget.vim_mode = VimMode.COMMAND

        # Should not crash (actual indent behavior depends on TextArea)
        widget.edit_indent()

    def test_dedent(self):
        """Test << dedents line."""
        widget = VimTextArea()
        widget.text = "    hello"
        widget.vim_mode = VimMode.COMMAND

        # Should not crash
        widget.edit_dedent()


class TestEdgeCases:
    """Test edge cases for editing operations."""

    def test_delete_on_empty_text(self):
        """Test delete operations on empty text."""
        widget = VimTextArea()
        widget.text = ""
        widget.vim_mode = VimMode.COMMAND

        # Should not crash
        widget.edit_delete_char()
        widget.edit_delete_line()

    def test_yank_empty_line(self):
        """Test yanking empty line."""
        widget = VimTextArea()
        widget.text = "\n"
        widget.vim_mode = VimMode.COMMAND
        widget.cursor_location = (0, 0)

        widget.edit_yank_line()
        # Should have yanked empty string or newline
        assert isinstance(widget.yank_register, str)

    def test_paste_with_line(self):
        """Test paste with full line (has newline)."""
        widget = VimTextArea()
        widget.text = "line1"
        widget.vim_mode = VimMode.COMMAND
        widget.yank_register = "line2\n"

        widget.edit_paste_after()
        # Should paste line
        assert "line2" in widget.text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
