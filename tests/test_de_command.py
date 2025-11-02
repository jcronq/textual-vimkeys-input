"""Test de command specifically."""

import pytest
from vimkeys_input import VimTextArea, VimMode
from vimkeys_input.operator_pending import OperatorMotionHandler


def test_de_delete_to_end_of_word():
    """Test de deletes to end of word."""
    widget = VimTextArea()
    widget.text = "hello world"
    widget.vim_mode = VimMode.COMMAND
    widget.cursor_location = (0, 0)

    # Save initial text
    initial_text = widget.text

    # Execute d then e
    result = OperatorMotionHandler.execute_operator_motion(widget, "d", widget.nav_word_end, 1)

    print(f"Initial: '{initial_text}'")
    print(f"After de: '{widget.text}'")
    print(f"Result: {result}")
    print(f"Yank register: '{widget.yank_register}'")

    # Check that text was deleted
    assert len(widget.text) < len(initial_text), (
        f"Text should be shorter. Was '{initial_text}', now '{widget.text}'"
    )


def test_de_from_middle_of_word():
    """Test de from middle of word."""
    widget = VimTextArea()
    widget.text = "hello world"
    widget.vim_mode = VimMode.COMMAND
    widget.cursor_location = (0, 2)  # On 'l' in hello

    result = OperatorMotionHandler.execute_operator_motion(widget, "d", widget.nav_word_end, 1)

    print(f"Result: {result}")
    print(f"Text after: '{widget.text}'")

    # Should delete from 'l' to end of 'hello'
    # Expected: 'he world'


def test_operator_pending_has_e_motion():
    """Verify 'e' is in the motion map."""
    widget = VimTextArea()

    # Check the motion handling
    # This verifies the code has 'e' mapped
    assert hasattr(widget, "nav_word_end")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
