"""Basic tests for VimTextArea widget."""

import pytest
from vimkeys_input import VimTextArea, VimMode


def test_vim_mode_enum():
    """Test VimMode enum exists and has expected values."""
    assert VimMode.INSERT
    assert VimMode.COMMAND
    assert VimMode.VISUAL
    assert VimMode.VISUAL_LINE


def test_vim_textarea_creation():
    """Test VimTextArea can be created."""
    widget = VimTextArea()
    assert widget is not None


def test_vim_textarea_initial_mode():
    """Test VimTextArea starts in INSERT mode."""
    widget = VimTextArea()
    assert widget.vim_mode == VimMode.INSERT


def test_vim_textarea_has_yank_register():
    """Test VimTextArea has yank register."""
    widget = VimTextArea()
    assert hasattr(widget, "yank_register")
    assert widget.yank_register == ""


def test_vim_textarea_has_pending_command():
    """Test VimTextArea has pending command tracking."""
    widget = VimTextArea()
    assert hasattr(widget, "pending_command")
    assert widget.pending_command is None


def test_vim_textarea_mode_methods():
    """Test VimTextArea has mode transition methods."""
    widget = VimTextArea()
    assert hasattr(widget, "_enter_insert_mode")
    assert hasattr(widget, "_enter_command_mode")
    assert hasattr(widget, "_enter_visual_mode")


def test_mode_transitions():
    """Test mode transitions work."""
    widget = VimTextArea()

    # Start in INSERT
    assert widget.vim_mode == VimMode.INSERT

    # Enter COMMAND
    widget._enter_command_mode()
    assert widget.vim_mode == VimMode.COMMAND

    # Enter VISUAL
    widget._enter_visual_mode()
    assert widget.vim_mode == VimMode.VISUAL

    # Back to INSERT
    widget._enter_insert_mode()
    assert widget.vim_mode == VimMode.INSERT


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
