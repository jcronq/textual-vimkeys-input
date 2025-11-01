# VimKeys Input User Guide

A comprehensive guide to using VimKeys Input for building Textual applications with vim-style modal editing.

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Basic Concepts](#basic-concepts)
4. [Getting Started](#getting-started)
5. [Modal Editing](#modal-editing)
6. [Navigation](#navigation)
7. [Editing Operations](#editing-operations)
8. [Operator + Motion System](#operator--motion-system)
9. [Text Objects](#text-objects)
10. [Visual Mode](#visual-mode)
11. [Search and Replace](#search-and-replace)
12. [Marks](#marks)
13. [Customization](#customization)
14. [Advanced Usage](#advanced-usage)
15. [Troubleshooting](#troubleshooting)

## Introduction

VimKeys Input brings the power and efficiency of Vim modal editing to Textual applications. If you're familiar with Vim, you'll feel right at home. If you're new to modal editing, this guide will teach you everything you need to know.

### Why Modal Editing?

Modal editing separates text input from text manipulation:
- **INSERT mode** - For typing text
- **COMMAND mode** - For navigating and manipulating text
- **VISUAL mode** - For selecting text

This separation allows for powerful, composable commands without modifier keys.

### Key Benefits

-  **Efficiency**: Navigate and edit text without leaving the keyboard
- **Composability**: Combine operators and motions for powerful commands
- **Muscle Memory**: Use familiar vim keybindings
- **Customizable**: Full CSS and event system for integration

## Installation

### Requirements

- Python 3.11 or higher
- Textual 0.47.0 or higher

### Install from PyPI

```bash
pip install vimkeys-input
```

### Install from Source

```bash
git clone https://github.com/yourusername/vimkeys-input.git
cd vimkeys-input
pip install -e ".[dev]"
```

## Basic Concepts

### The Widget

`VimTextArea` extends Textual's `TextArea` widget with vim keybindings:

```python
from vimkeys_input import VimTextArea

# Create a vim-enabled text input
text_input = VimTextArea(id="input")
```

### Modes

The widget operates in three modes:

| Mode | Purpose | How to Enter |
|------|---------|--------------|
| INSERT | Type text | `i`, `a`, `I`, `A`, `o`, `O` |
| COMMAND | Navigate and manipulate | `ESC` |
| VISUAL | Select text | `v` in COMMAND mode |

### Visual Feedback

The widget's border color changes based on mode:
- **Green** - INSERT mode (typing)
- **Blue** - COMMAND mode (navigating)
- **Yellow** - VISUAL mode (selecting)

## Getting Started

### Minimal Example

```python
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from vimkeys_input import VimTextArea

class MyApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield VimTextArea(id="input")
        yield Footer()

    def on_vim_text_area_submitted(self, event: VimTextArea.Submitted):
        self.notify(f"Submitted: {event.text}")

if __name__ == "__main__":
    MyApp().run()
```

### Try It Out

1. Run the app
2. Start typing (widget starts in INSERT mode)
3. Press `ESC` to enter COMMAND mode (border turns blue)
4. Press `h`, `j`, `k`, `l` to navigate
5. Press `i` to return to INSERT mode
6. Press `Enter` to submit

## Modal Editing

### Understanding Modes

#### INSERT Mode (Green Border)

This is where you type text. It works like a normal text input:

```
Type: "Hello world"
Press: ESC → Enter COMMAND mode
```

All standard keys work: letters, numbers, punctuation, backspace, delete, arrows.

#### COMMAND Mode (Blue Border)

This is where you navigate and manipulate text:

```
h → Move left
j → Move down
k → Move up
l → Move right
w → Next word
dd → Delete line
yy → Copy line
```

No text is inserted - every key is a command.

#### VISUAL Mode (Yellow Border)

This is where you select text:

```
v → Start visual mode
h/j/k/l → Extend selection
w/b → Select words
d → Delete selection
y → Copy selection
ESC → Back to COMMAND mode
```

### Mode Transitions

```
              ┌─────────────┐
              │   INSERT    │ (Green)
              │  (Typing)   │
              └──────┬──────┘
                     │
          i,a,I,A,o,O│ │ESC
                     │ ↓
              ┌─────────────┐
      ┌───────┤   COMMAND   │ (Blue)
      │ v     │ (Navigate)  │
      │       └──────┬──────┘
      │              │ ESC
      │              ↓
      │       ┌─────────────┐
      └──────→│   VISUAL    │ (Yellow)
              │  (Select)   │
              └─────────────┘
```

## Navigation

Navigation only works in COMMAND mode. Press `ESC` first if you're in INSERT mode.

### Basic Movement

| Key | Action | Example |
|-----|--------|---------|
| `h` | Move left | Moves cursor one character left |
| `j` | Move down | Moves cursor one line down |
| `k` | Move up | Moves cursor one line up |
| `l` | Move right | Moves cursor one character right |

**With counts:**
```
5j → Move down 5 lines
10l → Move right 10 characters
```

### Word Movement

| Key | Action | Behavior |
|-----|--------|----------|
| `w` | Next word | Move to start of next word |
| `b` | Previous word | Move to start of previous word |
| `e` | End of word | Move to end of current/next word |

**Example text:** `hello world test`

```
Cursor at 'h':
w → Cursor at 'w' (start of "world")
w → Cursor at 't' (start of "test")
b → Cursor at 'w' (back to "world")
e → Cursor at 'd' (end of "world")
```

**With counts:**
```
3w → Move forward 3 words
2b → Move back 2 words
```

### Line Movement

| Key | Action | Behavior |
|-----|--------|----------|
| `0` | Line start | Move to beginning of line |
| `$` | Line end | Move to end of line |
| `^` | First non-blank | Move to first non-whitespace character |

**Example line:** `    hello world`

```
0 → Column 0 (the first space)
$ → Column 15 (after "world")
^ → Column 4 (the 'h' in "hello")
```

### Document Movement

| Key | Action | Behavior |
|-----|--------|----------|
| `gg` | Document start | Move to first line |
| `G` | Document end | Move to last line |

## Editing Operations

All editing operations work in COMMAND mode.

### Delete Character

```
x → Delete character under cursor
3x → Delete 3 characters
```

### Delete Line

```
dd → Delete current line
3dd → Delete 3 lines (current + 2 below)
```

### Copy (Yank) Line

```
yy → Copy current line
3yy → Copy 3 lines
```

### Paste

```
p → Paste after cursor/line
P → Paste before cursor/line
3p → Paste 3 times
```

### Undo/Redo

```
u → Undo last change
Ctrl+r → Redo last undone change
```

### Replace Character

```
r → Wait for next key, replace character under cursor
rx → Replace with 'x'
r<space> → Replace with space
```

### Join Lines

```
J → Join current line with next line
```

Example:
```
Before:
hello
world

After 'J':
hello world
```

## Operator + Motion System

This is vim's most powerful feature: combining operators with motions.

### The Pattern

```
[count] operator [count] motion
```

### Operators

| Operator | Action |
|----------|--------|
| `d` | Delete |
| `c` | Change (delete + INSERT mode) |
| `y` | Yank (copy) |

### Common Combinations

```
dw → Delete word
d$ → Delete to end of line
d0 → Delete to start of line
d3w → Delete 3 words
d3j → Delete 3 lines down

cw → Change word (delete word, enter INSERT)
c$ → Change to end of line
cb → Change previous word

yw → Yank word
y$ → Yank to end of line
y3j → Yank 3 lines down
```

### Count Multiplication

```
2d3w → Delete 6 words (2 × 3)
3y2j → Yank 6 lines (3 × 2)
```

### Examples

**Delete from cursor to end of line:**
```
Text: "hello world test"
       ^cursor
Command: d$
Result: "hello "
```

**Change next 3 words:**
```
Text: "the quick brown fox jumps"
       ^cursor
Command: c3w
Result: " fox jumps"
(Now in INSERT mode to type replacement)
```

**Copy 2 words:**
```
Text: "hello world test"
       ^cursor
Command: y2w
Yank register: "hello world "
(Text unchanged, but now you can paste)
```

## Text Objects

Text objects let you operate on semantic units like words, quoted strings, or brackets.

### Word Text Objects

| Text Object | Meaning | Includes |
|-------------|---------|----------|
| `iw` | Inner word | The word only |
| `aw` | A word | Word + surrounding space |

**Example:** `hello world test`

```
Cursor anywhere in "world":
diw → Delete just "world" → "hello  test"
daw → Delete "world " → "hello test"
```

### Quote Text Objects

| Text Object | Description | Includes |
|-------------|-------------|----------|
| `i"` | Inside double quotes | Text only |
| `a"` | Around double quotes | Text + quotes |
| `i'` | Inside single quotes | Text only |
| `a'` | Around single quotes | Text + quotes |

**Example:** `say "hello world" to everyone`

```
Cursor anywhere in the quoted text:
di" → Delete "hello world" → say "" to everyone
da" → Delete whole thing → say  to everyone
ci" → Change text (delete + INSERT) → say "" to everyone
```

### Bracket Text Objects

Works with `()`, `{}`, `[]`:

| Text Object | Example | Description |
|-------------|---------|-------------|
| `i(` or `i)` | `(hello)` | Inside parens |
| `a(` or `a)` | `(hello)` | Around parens |
| `i{` or `i}` | `{hello}` | Inside braces |
| `a{` or `a}` | `{hello}` | Around braces |
| `i[` or `i]` | `[hello]` | Inside brackets |
| `a[` or `a]` | `[hello]` | Around brackets |

**Example:** `func(arg1, arg2)`

```
Cursor anywhere in parentheses:
di( → Delete "arg1, arg2" → func()
da( → Delete "(arg1, arg2)" → func
ci( → Change args → func()  (INSERT mode)
```

### Combining with Operators

```
diw → Delete inner word
daw → Delete a word (with space)
ci" → Change inside quotes
da( → Delete around parentheses
yi{ → Yank inside braces
```

## Visual Mode

Visual mode lets you select text before operating on it.

### Entering Visual Mode

```
v → Start character-wise visual mode
```

### Selecting Text

```
h/j/k/l → Extend selection by character/line
w → Extend to next word
b → Extend to previous word
e → Extend to end of word
$ → Extend to end of line
0 → Extend to start of line
```

### Operating on Selection

```
d → Delete selection
c → Change selection (delete + INSERT)
y → Yank (copy) selection
ESC → Cancel selection (back to COMMAND)
```

### Example Workflow

```
1. Place cursor at start of text to select
2. Press 'v' → Enter VISUAL mode (yellow border)
3. Press 'w' 'w' 'w' → Select 3 words
4. Press 'y' → Yank selection
5. Move cursor elsewhere
6. Press 'p' → Paste
```

## Search and Replace

### Search

```
/ → Enter search mode
  → Type search pattern
  → Press Enter
n → Next match
N → Previous match
```

**Example:**
```
Text: "hello world hello test hello"
Command: /hello
Result: Cursor jumps to first "hello"
Press 'n': Jump to second "hello"
Press 'n': Jump to third "hello"
Press 'N': Jump back to second "hello"
```

### Replace Character

```
r → Wait for next character
rx → Replace character under cursor with 'x'
```

## Marks

Marks are bookmarks for cursor positions.

### Setting Marks

```
m{a-z} → Set mark at cursor position
ma → Set mark 'a'
mb → Set mark 'b'
```

### Jumping to Marks

```
'{a-z} → Jump to line of mark
'a → Jump to line of mark 'a'

`{a-z} → Jump to exact position of mark
`a → Jump to exact position of mark 'a'
```

### Example Workflow

```
1. Navigate to important line
2. Press 'ma' → Set mark 'a'
3. Navigate elsewhere in document
4. Edit other text
5. Press 'a → Jump back to mark 'a'
```

## Customization

### Styling Modes

Customize colors for each mode:

```python
class MyApp(App):
    CSS = """
    VimTextArea.insert-mode {
        border: solid green;
        background: $surface;
    }

    VimTextArea.command-mode {
        border: solid blue;
        background: $surface;
    }

    VimTextArea.visual-mode {
        border: solid yellow;
        background: $boost;
    }
    """
```

### Handling Events

React to mode changes and submissions:

```python
def on_vim_text_area_mode_changed(self, event: VimTextArea.ModeChanged):
    """React to mode changes."""
    if event.mode == VimMode.INSERT:
        self.sub_title = "✎ Editing"
    elif event.mode == VimMode.COMMAND:
        self.sub_title = "⌘ Command"
    elif event.mode == VimMode.VISUAL:
        self.sub_title = "◆ Visual"

def on_vim_text_area_submitted(self, event: VimTextArea.Submitted):
    """Handle submission."""
    text = event.text
    self.process_input(text)
    event.text_area.clear()
```

### Sizing the Widget

```python
class MyApp(App):
    CSS = """
    VimTextArea {
        height: auto;
        max-height: 20;
        min-height: 3;
        width: 100%;
    }
    """
```

## Advanced Usage

### Building a Chat Application

See `examples/03_streaming_chat.py` for a complete example with:
- Message history display
- Input history navigation
- Streaming responses
- Command palette

### Extending VimTextArea

Add custom functionality by subclassing:

```python
class CustomVimTextArea(VimTextArea):
    """VimTextArea with custom features."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_data = []

    def on_key(self, event: events.Key) -> None:
        """Override to add custom key handling."""
        if event.key == "ctrl+k":
            # Custom behavior
            self.do_something_custom()
            return

        # Default behavior
        return super().on_key(event)

    def do_something_custom(self):
        """Custom functionality."""
        pass
```

### Integration with Other Widgets

VimTextArea works seamlessly with other Textual widgets:

```python
def compose(self) -> ComposeResult:
    with Vertical():
        yield RichLog(id="output")
        yield VimTextArea(id="input")
        yield Button("Submit")
```

## Troubleshooting

### Widget Doesn't Respond to Keys

**Problem:** Pressing vim keys does nothing

**Solution:** Make sure the widget has focus:
```python
def on_mount(self):
    self.query_one("#input").focus()
```

### Wrong Mode

**Problem:** Keys don't work as expected

**Solution:** Check current mode (border color) and press `ESC` to return to COMMAND mode

### Selection Not Working

**Problem:** Visual mode selection doesn't extend properly

**Solution:** Make sure you're in VISUAL mode (press `v` in COMMAND mode first)

### Events Not Firing

**Problem:** `on_vim_text_area_submitted` doesn't fire

**Solution:**
1. Make sure you're pressing Enter in INSERT mode
2. Check the handler name matches: `on_vim_text_area_submitted`
3. Verify the widget ID matches your query

### Custom CSS Not Applying

**Problem:** Mode colors don't change

**Solution:** Make sure CSS classes match exactly:
- `.insert-mode`
- `.command-mode`
- `.visual-mode`

## Next Steps

- Read the [API Reference](api-reference.md) for complete API documentation
- Check out [Examples](examples.md) for complete working applications
- See [Contributing Guide](../CONTRIBUTING.md) to contribute to the project

## Quick Reference Card

```
=== MODE SWITCHING ===
ESC     → COMMAND mode
i       → INSERT at cursor
a       → INSERT after cursor
I       → INSERT at line start
A       → INSERT at line end
o       → Open line below
O       → Open line above
v       → VISUAL mode

=== NAVIGATION ===
h/j/k/l → Left/down/up/right
w/b/e   → Word forward/back/end
0/$     → Line start/end
^       → First non-blank
gg/G    → Document start/end

=== EDITING ===
x       → Delete char
dd      → Delete line
yy      → Yank line
p/P     → Paste after/before
u       → Undo
Ctrl+r  → Redo
r       → Replace char
J       → Join lines

=== OPERATORS + MOTIONS ===
dw      → Delete word
d$      → Delete to end
d3w     → Delete 3 words
cw      → Change word
yw      → Yank word

=== TEXT OBJECTS ===
diw     → Delete inner word
ci"     → Change inside quotes
da(     → Delete around parens

=== VISUAL ===
v       → Start visual
hjkl/wb → Extend selection
d/c/y   → Delete/change/yank
ESC     → Exit visual

=== SEARCH ===
/       → Search
n/N     → Next/previous

=== MARKS ===
ma      → Set mark 'a'
'a      → Jump to mark line
`a      → Jump to mark position
```
