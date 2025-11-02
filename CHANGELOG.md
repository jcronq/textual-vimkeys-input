# Changelog

All notable changes to VimKeys Input will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.1] - 2025-11-02

### Fixed
- Invalid PyPI classifier removed (`Framework :: Textual` is not recognized)
- CD workflow permissions - added `contents: write` for tag creation
- All linting errors resolved (unused imports and variables)
- Code formatting applied across all files with ruff

## [0.3.0] - 2025-11-01

### Added
- Visual mode word end motion (`e`)
- Visual mode document motions (`gg`, `G`)
- CI/CD workflows for automated testing and PyPI publishing
- Comprehensive documentation suite (README, CONTRIBUTING, user guide)
- Input history navigation in streaming chat example
- Animated thinking indicator in streaming chat example
- Text wrapping support in chat examples

### Fixed
- Visual mode delete operations (incorrect parameter order in `replace()` calls)
- Visual mode word motions (`w`, `b`) now properly maintain selection
- Visual mode selections are now inclusive (vim behavior) instead of exclusive
- Visual mode indent/dedent operations parameter order

### Changed
- Visual mode selections now use `_make_inclusive_end()` helper for vim-compliant behavior

## [0.2.0] - 2025-11-01

### Added
- Operator + motion system (`dw`, `c$`, `y3j`, etc.)
- Count support for all commands (`5j`, `3dd`, `2d3w`)
- Text object support (`iw`, `aw`, `i"`, `a"`, `i(`, `a(`, `i{`, `a{`, `i[`, `a[`)
- Marks system (`ma`, `'a`, `` `a ``)
- Search functionality (`/`, `n`, `N`)
- Replace character command (`r`)
- Join lines command (`J`)
- Complete operator-pending state management
- Modular mixin architecture for operations
- 124 comprehensive tests (82% passing)

### Changed
- Refactored monolithic vim_textarea.py into modular mixins
- Split operations into navigation.py, editing.py, visual.py, search.py, text_objects.py
- Improved test coverage and organization

### Fixed
- `get_line()` text object handling (wrap with `str()`)
- Operator + motion combinations now work correctly
- Count multiplication (e.g., `2d3w` deletes 6 words)

## [0.1.0] - 2025-10-31

### Added
- Initial VimTextArea widget implementation
- Modal editing (INSERT, COMMAND, VISUAL modes)
- Basic navigation (h, j, k, l, w, b, e, 0, $, ^, gg, G)
- Basic editing (x, dd, yy, cc, p, P)
- Visual character-wise selection
- Undo/redo support (u, Ctrl+r)
- Mode transition commands (i, a, I, A, o, O, v)
- Visual feedback (border colors by mode)
- CSS class support (.insert-mode, .command-mode, .visual-mode)
- Events (Submitted, ModeChanged)
- Three example applications:
  - 01_spike.py - Basic functionality demo
  - 02_simple_chat.py - Simple chat bot
  - 03_streaming_chat.py - Streaming chat with animations
- Initial test suite
- Project structure and build configuration

### Technical
- Built on Textual's TextArea widget
- Python 3.11+ support
- MIT License
- pyproject.toml configuration
- pytest test framework
- ruff linting and formatting

## Version History

### Phase 0: Spike (Complete)
Initial prototype with basic vim functionality

### Phase 1: Refactoring (Complete)
Modular architecture and comprehensive tests

### Phase 2: Advanced Features (Complete)
Operator+motion, counts, text objects, marks

### Phase 3: Polish (In Progress)
Documentation, optimization, PyPI preparation

---

## Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality in a backward compatible manner
- **PATCH** version for backward compatible bug fixes

## Links

- [Unreleased]: https://github.com/yourusername/vimkeys-input/compare/v0.3.1...HEAD
- [0.3.1]: https://github.com/yourusername/vimkeys-input/compare/v0.3.0...v0.3.1
- [0.3.0]: https://github.com/yourusername/vimkeys-input/compare/v0.2.0...v0.3.0
- [0.2.0]: https://github.com/yourusername/vimkeys-input/compare/v0.1.0...v0.2.0
- [0.1.0]: https://github.com/yourusername/vimkeys-input/releases/tag/v0.1.0
