"""Vim operations for VimTextArea.

This package contains modular implementations of vim operations:
- navigation.py: Cursor movement operations
- editing.py: Text editing operations (dd, yy, x, etc.)
- visual.py: Visual mode operations
- search.py: Character search operations (f, t, F, T)
- text_objects.py: Text object operations (iw, i", da(, etc.)
"""

from .navigation import NavigationMixin
from .editing import EditingMixin
from .visual import VisualMixin
from .search import SearchMixin
from .text_objects import TextObjectMixin

__all__ = [
    "NavigationMixin",
    "EditingMixin",
    "VisualMixin",
    "SearchMixin",
    "TextObjectMixin",
]
