# Contributing to VimKeys Input

Thank you for considering contributing to VimKeys Input! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Code Style](#code-style)
- [Commit Messages](#commit-messages)
- [Pull Requests](#pull-requests)
- [Documentation](#documentation)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)

## Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors:

- Be respectful and inclusive
- Be patient with new contributors
- Focus on constructive feedback
- Assume good intentions
- Help create a positive community

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- Basic understanding of [Textual](https://textual.textualize.io/)
- Familiarity with Vim keybindings (helpful but not required)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:

```bash
git clone https://github.com/YOUR_USERNAME/vimkeys-input.git
cd vimkeys-input
```

3. Add the upstream repository:

```bash
git remote add upstream https://github.com/ORIGINAL_OWNER/vimkeys-input.git
```

## Development Setup

### Using uv (Recommended)

```bash
# Create virtual environment
uv venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in editable mode with dev dependencies
uv pip install -e ".[dev]"
```

### Using pip

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### Verify Installation

```bash
# Run tests to verify setup
pytest tests/

# Try running an example
uv run python examples/01_spike.py
```

## Project Structure

```
vimkeys-input/
├── vimkeys_input/           # Main package
│   ├── __init__.py         # Public API exports
│   ├── vim_modes.py        # VimMode enum definition
│   ├── vim_textarea.py     # Main VimTextArea widget
│   ├── count_handler.py    # Count/number support
│   ├── operator_pending.py # Operator+motion system
│   ├── marks.py            # Position bookmark system
│   └── operations/         # Modular operation mixins
│       ├── __init__.py
│       ├── navigation.py   # Movement commands (h, j, k, l, w, b, e, etc.)
│       ├── editing.py      # Edit commands (x, r, p, P, u, J)
│       ├── visual.py       # Visual mode operations
│       ├── search.py       # Search functionality (/, n, N)
│       └── text_objects.py # Text object support (iw, i", i(, etc.)
├── examples/               # Example applications
│   ├── 01_spike.py        # Basic functionality demo
│   ├── 02_simple_chat.py  # Simple chat bot
│   └── 03_streaming_chat.py # Advanced streaming chat
├── tests/                  # Test suite
│   ├── test_navigation.py
│   ├── test_editing.py
│   ├── test_visual.py
│   ├── test_search.py
│   ├── test_operator_motion.py
│   └── ...
├── docs/                   # Additional documentation
├── plans/                  # Development planning documents
├── pyproject.toml         # Package configuration
├── README.md              # Main documentation
├── CONTRIBUTING.md        # This file
├── LICENSE                # MIT License
└── CHANGELOG.md           # Version history
```

## Development Workflow

### 1. Create a Feature Branch

Always create a new branch for your work:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation only
- `refactor/` - Code refactoring
- `test/` - Test improvements

### 2. Make Your Changes

- Follow the existing code style (see [Code Style](#code-style))
- Add tests for new functionality
- Update documentation as needed
- Keep commits focused and atomic

### 3. Test Your Changes

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_navigation.py

# Run with coverage
pytest --cov=vimkeys_input tests/

# Run with verbose output
pytest -v tests/
```

### 4. Test with Examples

Run the example applications to verify your changes work in practice:

```bash
uv run python examples/01_spike.py
uv run python examples/02_simple_chat.py
uv run python examples/03_streaming_chat.py

# Or use Textual dev mode for live reload
textual run --dev examples/01_spike.py
```

### 5. Commit Your Changes

```bash
git add .
git commit -m "feat: add support for visual line mode"
```

See [Commit Messages](#commit-messages) for conventions.

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Testing

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_navigation.py

# Specific test function
pytest tests/test_navigation.py::test_nav_left

# With coverage report
pytest --cov=vimkeys_input --cov-report=html tests/

# Watch mode (requires pytest-watch)
ptw tests/
```

### Writing Tests

We use pytest for testing. Tests should:

1. **Test one thing** - Each test should verify a single behavior
2. **Be independent** - Tests should not depend on other tests
3. **Have clear names** - Name tests descriptively: `test_nav_word_forward_moves_to_next_word()`
4. **Use fixtures** - Reuse common setup with pytest fixtures

Example test:

```python
import pytest
from vimkeys_input import VimTextArea, VimMode

@pytest.fixture
def widget():
    """Create a VimTextArea for testing."""
    return VimTextArea()

def test_nav_word_forward_moves_cursor(widget):
    """Test that 'w' moves cursor to start of next word."""
    widget.text = "hello world test"
    widget.cursor_location = (0, 0)
    widget.mode = VimMode.COMMAND

    widget.nav_word_forward()

    assert widget.cursor_location == (0, 6)  # Start of "world"
```

### Test Coverage

We aim for high test coverage. When adding new features:

- Add tests for the happy path
- Add tests for edge cases
- Add tests for error conditions
- Test integration with existing features

Current coverage: ~82% (124 tests)

## Code Style

### Python Style

We follow PEP 8 with some project-specific conventions:

- **Line length**: 100 characters (not 79)
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Prefer double quotes for strings
- **Imports**: Group in order: stdlib, third-party, local

### Formatting

We use `ruff` for formatting and linting:

```bash
# Format code
ruff format vimkeys_input/

# Check for issues
ruff check vimkeys_input/

# Auto-fix issues
ruff check --fix vimkeys_input/
```

### Type Hints

Use type hints for all public APIs:

```python
def nav_word_forward(self, count: int = 1) -> None:
    """Move cursor to start of next word."""
    ...

@property
def mode(self) -> VimMode:
    """Get current vim mode."""
    return self._mode
```

### Docstrings

Use Google-style docstrings:

```python
def execute_operator_motion(
    widget: "VimTextArea",
    operator: str,
    motion_func: Callable,
    count: int = 1
) -> bool:
    """Execute an operator combined with a motion.

    Args:
        widget: The VimTextArea widget to operate on.
        operator: The operator key ('d', 'c', 'y').
        motion_func: The motion function to execute.
        count: Number of times to repeat the motion.

    Returns:
        True if the operation succeeded, False otherwise.

    Example:
        >>> execute_operator_motion(widget, 'd', widget.nav_word_forward, 3)
        True  # Deletes 3 words forward
    """
    ...
```

### Comments

- Write self-documenting code when possible
- Add comments for complex logic or non-obvious decisions
- Explain *why*, not *what* (the code shows what)

```python
# Good
# Use str() because get_line() returns a Text object, not a string
line = str(self.get_line(row))

# Bad
# Get the line as a string
line = str(self.get_line(row))
```

## Commit Messages

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `style:` - Code style (formatting, missing semicolons, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

### Examples

```bash
feat(visual): add visual line mode support

fix(navigation): correct word boundary detection for punctuation

docs(readme): add examples for text object operations

refactor(operations): extract text object logic into separate mixin

test(operator-motion): add tests for count multiplication (2d3w)

chore(deps): update textual to 0.50.0
```

### Commit Message Tips

- Use imperative mood ("add feature" not "added feature")
- First line should be 50 characters or less
- Separate subject from body with blank line
- Explain *what* and *why*, not *how*

## Pull Requests

### Before Submitting

- [ ] Tests pass locally (`pytest tests/`)
- [ ] Code is formatted (`ruff format vimkeys_input/`)
- [ ] No linting errors (`ruff check vimkeys_input/`)
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated (if applicable)
- [ ] Commit messages follow conventions

### PR Description Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe how you tested your changes.

## Screenshots (if applicable)
Add screenshots for UI changes.

## Checklist
- [ ] Tests pass
- [ ] Code formatted
- [ ] Documentation updated
- [ ] CHANGELOG updated
```

### Review Process

1. **Automated checks** - CI runs tests and linting
2. **Code review** - Maintainers review your code
3. **Feedback** - Address any requested changes
4. **Approval** - Once approved, we'll merge your PR
5. **Thanks!** - Your contribution is appreciated!

## Documentation

### README Updates

Update README.md when:
- Adding new features
- Changing public API
- Adding new examples
- Updating installation instructions

### Docstrings

All public functions, classes, and methods should have docstrings:

```python
class VimTextArea(TextArea):
    """A TextArea widget with vim-style modal editing.

    Extends Textual's TextArea with full vim modal editing support,
    including INSERT, COMMAND, and VISUAL modes with standard vim
    keybindings.

    Attributes:
        mode: Current vim mode (INSERT, COMMAND, or VISUAL).
        yank_register: Contents of the yank (copy) register.

    Events:
        Submitted: Posted when user presses Enter in INSERT mode.
        ModeChanged: Posted when vim mode changes.

    Example:
        >>> from vimkeys_input import VimTextArea
        >>> widget = VimTextArea(id="input")
        >>> widget.mode = VimMode.COMMAND
    """
```

### Examples

When adding features, consider adding an example:

1. Add example to `examples/` directory
2. Document the example in README.md
3. Keep examples simple and focused
4. Include comments explaining key concepts

## Reporting Bugs

### Before Reporting

1. Check existing issues
2. Try the latest version
3. Verify it's reproducible

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. Create VimTextArea with...
2. Press keys...
3. See error

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Environment:**
- OS: [e.g., macOS 14.0]
- Python version: [e.g., 3.11.5]
- Textual version: [e.g., 0.47.0]
- VimKeys Input version: [e.g., 0.1.0]

**Additional context**
Any other relevant information.
```

## Suggesting Features

We welcome feature suggestions! When suggesting a feature:

1. **Check existing issues** - Maybe it's already planned
2. **Describe the use case** - Why is this feature needed?
3. **Provide examples** - Show how it would work
4. **Consider scope** - Does it fit the project's goals?

### Feature Request Template

```markdown
**Feature Description**
Clear description of the proposed feature.

**Use Case**
Why is this feature needed? What problem does it solve?

**Proposed Solution**
How should this feature work?

**Alternatives Considered**
What other solutions have you considered?

**Vim Compatibility**
How does this relate to standard vim behavior?
```

## Development Tips

### Textual Dev Tools

```bash
# Run with dev console for debugging
textual console
textual run --dev examples/01_spike.py

# The console shows log output and allows inspection
```

### Debugging Tests

```python
# Add debugging to tests
def test_something(widget):
    import pdb; pdb.set_trace()  # Breakpoint
    widget.nav_word_forward()
    assert widget.cursor_location == (0, 6)
```

### Understanding the Architecture

1. **Start with VimTextArea** (`vim_textarea.py`) - Main widget class
2. **Check the mixins** (`operations/*.py`) - Specific functionality
3. **Read the tests** (`tests/`) - Usage examples
4. **Run examples** (`examples/`) - See it in action

### Common Tasks

**Adding a new vim command:**

1. Determine which mixin it belongs to
2. Add the method to the appropriate mixin
3. Wire it up in `vim_textarea.py` key handling
4. Add tests
5. Update README keybinding reference

**Adding a new mode:**

1. Add to `VimMode` enum in `vim_modes.py`
2. Add mode transition logic in `vim_textarea.py`
3. Add CSS class handling
4. Add tests
5. Update documentation

## Questions?

If you have questions:

- Check existing documentation
- Look at similar code in the project
- Ask in a GitHub issue or discussion
- Read Textual documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to VimKeys Input! 🎉
