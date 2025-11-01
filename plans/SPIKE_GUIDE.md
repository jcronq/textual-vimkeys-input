# Spike Guide - VimTextArea Validation (2-3 Days)

**Purpose**: Validate that extending TextArea for vim modes is feasible before committing to full implementation
**Timeline**: 2-3 days
**Outcome**: GO/NO-GO decision

---

## Goals

### Primary Goals

1. ✅ **Prove feasibility** - Can we extend TextArea successfully?
2. ✅ **Feel right** - Does it feel like vim?
3. ✅ **Identify blockers** - Any showstoppers?

### Questions to Answer

- Can we intercept key events effectively?
- Do mode transitions feel instant?
- Does navigation feel natural?
- Can we style based on mode?
- Are there any TextArea API limitations?
- Does it feel good to use?

---

## Setup (30 minutes)

### Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install Textual
pip install textual textual-dev rich

# Verify installation
textual --version
python3 -c "from textual.widgets import TextArea; print('OK')"
```

### Create Project Structure

```bash
mkdir -p textbox-spike
cd textbox-spike

# Create files
touch spike_vim.py
touch test_spike.py
mkdir -p textbox
touch textbox/__init__.py
touch textbox/vim_textarea.py
```

---

## Day 1: Basic Structure & Mode Switching

### Step 1: Minimal VimTextArea (1 hour)

Create `textbox/vim_textarea.py`:

```python
"""Minimal VimTextArea for spike."""

from textual.widgets import TextArea
from textual.message import Message
from enum import Enum

class VimMode(Enum):
    """Vim editing modes."""
    INSERT = "INSERT"
    COMMAND = "COMMAND"

class VimTextArea(TextArea):
    """TextArea with vim keybindings (spike version)."""

    DEFAULT_CSS = """
    VimTextArea {
        border: solid green;
    }

    VimTextArea.command-mode {
        border: solid blue;
    }
    """

    class ModeChanged(Message):
        """Posted when vim mode changes."""
        def __init__(self, mode: VimMode):
            super().__init__()
            self.mode = mode

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vim_mode = VimMode.INSERT
        self.log(f"VimTextArea initialized in {self.vim_mode}")

    def on_key(self, event):
        """Handle key events based on vim mode."""
        self.log(f"Key pressed: {event.key} in mode {self.vim_mode}")

        # ESC always goes to command mode
        if event.key == "escape":
            self.vim_mode = VimMode.COMMAND
            self.remove_class("insert-mode")
            self.add_class("command-mode")
            self.post_message(self.ModeChanged(VimMode.COMMAND))
            event.prevent_default()
            self.log("Switched to COMMAND mode")
            return

        # Route to mode handler
        if self.vim_mode == VimMode.INSERT:
            self._handle_insert_mode(event)
        elif self.vim_mode == VimMode.COMMAND:
            self._handle_command_mode(event)

    def _handle_insert_mode(self, event):
        """Insert mode - default TextArea behavior."""
        # Let TextArea handle typing
        pass

    def _handle_command_mode(self, event):
        """Command mode - vim navigation."""
        key = event.key

        # Enter insert mode with 'i'
        if key == "i":
            self.vim_mode = VimMode.INSERT
            self.remove_class("command-mode")
            self.add_class("insert-mode")
            self.post_message(self.ModeChanged(VimMode.INSERT))
            event.prevent_default()
            self.log("Switched to INSERT mode")
```

**Test**: Does mode tracking work?

```bash
# Run with logging
textual console &
python3 test_spike.py
# Watch console for log messages
```

### Step 2: Simple Test App (1 hour)

Create `spike_vim.py`:

```python
"""Spike test app for VimTextArea."""

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Vertical
from textbox.vim_textarea import VimTextArea, VimMode

class SpikeApp(App):
    """Test app for VimTextArea spike."""

    CSS = """
    #status {
        height: 1;
        background: $panel;
        color: $text;
        padding: 0 1;
    }

    #input {
        height: 10;
        margin: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Type text, press ESC for command mode, 'i' for insert mode", id="status")
        yield VimTextArea(id="input")
        yield Footer()

    def on_mount(self):
        """Initialize."""
        self.title = "VimTextArea Spike"
        self.query_one("#input").focus()

    def on_vim_text_area_mode_changed(self, event):
        """Update status when mode changes."""
        status = self.query_one("#status")
        mode_text = f"Mode: {event.mode.value}"
        status.update(mode_text)

if __name__ == "__main__":
    app = SpikeApp()
    app.run()
```

**Test**: Run and verify:
- [ ] App launches
- [ ] Can type text
- [ ] ESC changes border color
- [ ] Status line updates
- [ ] 'i' returns to insert mode
- [ ] Border changes back

```bash
textual run --dev spike_vim.py
```

### Step 3: Test Mode Switching Feel (1 hour)

**Manual Testing**:

1. Launch app
2. Type: "hello world"
3. Press ESC (should feel instant)
4. Press 'i' (should feel instant)
5. Type more text
6. Repeat 10 times rapidly

**Questions**:
- Does mode switching feel instant (<50ms)?
- Is there any lag or delay?
- Does the border change immediately?
- Do you feel the mode change?

**Record Results**:
```
Mode Switching Test:
✅ / ❌  Feels instant
✅ / ❌  Border changes immediately
✅ / ❌  Can switch rapidly
✅ / ❌  No visual glitches
Notes: _______________________
```

### Step 4: Add hjkl Navigation (2 hours)

Update `_handle_command_mode` in `vim_textarea.py`:

```python
def _handle_command_mode(self, event):
    """Command mode - vim navigation."""
    key = event.key

    # Navigation
    if key == "h":
        self.action_cursor_left()
        event.prevent_default()
        self.log("Moved left")
    elif key == "j":
        self.action_cursor_down()
        event.prevent_default()
        self.log("Moved down")
    elif key == "k":
        self.action_cursor_up()
        event.prevent_default()
        self.log("Moved up")
    elif key == "l":
        self.action_cursor_right()
        event.prevent_default()
        self.log("Moved right")

    # Enter insert mode
    elif key == "i":
        self.vim_mode = VimMode.INSERT
        self.remove_class("command-mode")
        self.add_class("insert-mode")
        self.post_message(self.ModeChanged(VimMode.INSERT))
        event.prevent_default()
        self.log("Switched to INSERT mode")
```

**Test**: Run and verify:
- [ ] Type text in insert mode
- [ ] ESC to command mode
- [ ] hjkl moves cursor
- [ ] Movement feels natural
- [ ] No lag or stutter
- [ ] 'i' returns to insert mode at correct position

**Manual Testing**:
1. Type: "line1\nline2\nline3"
2. ESC
3. Press 'k' twice (should go to line1)
4. Press 'j' (should go to line2)
5. Press 'h' and 'l' (should move left/right)
6. Does it feel like vim?

**Record Results**:
```
Navigation Test:
✅ / ❌  hjkl works correctly
✅ / ❌  Movement feels smooth
✅ / ❌  No unexpected behavior
✅ / ❌  Cursor position correct
Notes: _______________________
```

---

## Day 2: More Navigation & Basic Editing

### Step 5: Add 0, $, and 'a' (2 hours)

Add to `_handle_command_mode`:

```python
# Line navigation
elif key == "0":
    self.action_cursor_line_start()
    event.prevent_default()
elif key == "dollar":  # $
    self.action_cursor_line_end()
    event.prevent_default()

# Append after cursor
elif key == "a":
    self.action_cursor_right()
    self.vim_mode = VimMode.INSERT
    self.remove_class("command-mode")
    self.add_class("insert-mode")
    self.post_message(self.ModeChanged(VimMode.INSERT))
    event.prevent_default()
```

**Test**:
- [ ] 0 goes to line start
- [ ] $ goes to line end
- [ ] 'a' enters insert mode after cursor

### Step 6: Add 'x' (Delete Character) (1 hour)

```python
# Delete character
elif key == "x":
    self.action_delete_right()
    event.prevent_default()
```

**Test**:
- [ ] 'x' deletes character under cursor
- [ ] Works at line start
- [ ] Works at line end
- [ ] Stays in command mode

### Step 7: Test Real Usage (2 hours)

**Scenario**: Write 3 messages with vim editing

**Task**:
1. Launch app
2. Type message: "Hello, I am testing vim mode."
3. ESC → 'h' back to "vim" → 'x' delete 'v' → 'i' insert "V" → ESC
4. Review message, submit (we'll add submit later, for now just check editing)
5. Clear and repeat 2 more times

**Questions**:
- Does it feel productive?
- Any frustrating limitations?
- Does it feel like vim?
- Would you want to use this?

**Record Observations**:
```
Real Usage Test:
✅ / ❌  Productive to use
✅ / ❌  Feels like vim
✅ / ❌  No major frustrations
✅ / ❌  Would use in real app
Issues found: _________________
Missing features needed: ______
```

### Step 8: Identify TextArea Limitations (1 hour)

**Test Edge Cases**:

1. **Multi-line behavior**:
   - Type 10+ lines
   - Navigate with hjkl
   - Does scrolling work?
   - Can reach all lines?

2. **Selection**:
   - Try Shift+arrow keys
   - Does selection work in command mode?
   - Can we hook into this for visual mode?

3. **Undo/redo**:
   - Type text, press 'u' in command mode
   - Does TextArea's undo work?
   - Can we intercept it?

4. **Word boundaries**:
   - Call `action_cursor_word_right()`
   - Does it move correctly?
   - What about punctuation?

**Document Findings**:
```
TextArea API Findings:
✅ / ❌  Multi-line works
✅ / ❌  Scrolling works
✅ / ❌  Selection accessible
✅ / ❌  Undo/redo works
✅ / ❌  Word motions work
✅ / ❌  Can build visual mode
Blockers found: _______________
Workarounds needed: ___________
```

---

## Day 3: Validation & Decision

### Step 9: Performance Testing (1 hour)

**Test Key Latency**:

```python
# Add to spike_vim.py

import time

class SpikeApp(App):
    def __init__(self):
        super().__init__()
        self.key_times = []

    def on_key(self, event):
        """Measure key latency."""
        t = time.time()
        super().on_key(event)
        latency = time.time() - t
        self.key_times.append(latency)

        if len(self.key_times) >= 100:
            avg = sum(self.key_times) / len(self.key_times)
            self.log(f"Average key latency: {avg*1000:.2f}ms")
            self.key_times = []
```

**Test**:
- Type rapidly for 30 seconds
- Check average latency
- Should be <10ms

**Record**:
```
Performance Test:
Average latency: _____ ms
✅ / ❌  <10ms (excellent)
✅ / ❌  <50ms (acceptable)
❌       >50ms (too slow)
```

### Step 10: Write Spike Report (2 hours)

Create `SPIKE_REPORT.md`:

```markdown
# VimTextArea Spike Report

**Date**: [Date]
**Duration**: [X] days
**Conclusion**: GO / NO-GO

## What We Built

- Basic VimTextArea extending TextArea
- Insert/Command modes
- hjkl navigation
- 0, $, 'a', 'x' commands
- Mode-based styling

## What Worked Well

✅ [List what worked]
- Mode switching feels instant
- hjkl navigation smooth
- TextArea API sufficient
- etc.

## What Didn't Work

❌ [List issues]
- [Issue if any]

## TextArea Limitations Found

[List any API limitations]

## Performance

- Average key latency: ___ms
- Mode switch latency: ___ms
- Verdict: Acceptable / Too Slow

## User Experience

[Subjective assessment]
- Does it feel like vim? Yes/No
- Would you use this? Yes/No
- What's missing for MVP?

## Technical Risks

[Any risks identified]

## Recommendation

GO / NO-GO

Justification:
[Explain decision]

## Next Steps if GO

1. Implement Phase 1: Basic Vim
2. Add tests
3. [etc.]

## Next Steps if NO-GO

[Alternative approaches]
```

### Step 11: Demo & Decision (1 hour)

**Present Spike**:
1. Show the working prototype
2. Demonstrate mode switching
3. Demonstrate navigation
4. Show code (how simple it is)
5. Discuss findings

**Make Decision**:
- Review spike report
- Consider effort vs value
- Check team consensus
- Decide: GO or NO-GO

**If GO**:
→ Continue to Phase 1 (IMPLEMENTATION.md)

**If NO-GO**:
→ Review alternatives (see below)

---

## Success Criteria

### Must Have (GO)

- ✅ Mode switching feels instant (<50ms)
- ✅ hjkl navigation works smoothly
- ✅ No critical TextArea API blockers
- ✅ Feels vim-like to use
- ✅ Team believes it's viable

### Nice to Have

- ✅ Performance excellent (<10ms latency)
- ✅ No edge case issues found
- ✅ Code is clean and simple
- ✅ Excited about building it

### Deal Breakers (NO-GO)

- ❌ Mode switching lags (>100ms)
- ❌ TextArea missing critical APIs
- ❌ Doesn't feel like vim at all
- ❌ Performance unacceptable (>50ms)
- ❌ Team not confident it will work

---

## Common Issues & Solutions

### Issue: Keys Not Intercepted

**Problem**: Command mode keys still type characters

**Solution**:
```python
def on_key(self, event):
    if self.vim_mode == VimMode.COMMAND:
        event.prevent_default()  # Add this
        self._handle_command_mode(event)
```

### Issue: Mode Doesn't Change

**Problem**: CSS class not updating

**Solution**:
```python
# Remove old class before adding new
self.remove_class("insert-mode", "command-mode")
self.add_class(f"{self.vim_mode.value.lower()}-mode")
```

### Issue: Lag When Typing

**Problem**: Key events slow

**Check**:
- Are you logging too much?
- Is TextArea action slow?
- Try removing logs and test again

### Issue: Border Not Changing

**Problem**: CSS not applied

**Solution**:
```python
# Check CSS is correct
DEFAULT_CSS = """
VimTextArea.command-mode {
    border: solid blue;
}
"""

# Make sure class is actually added
self.log(f"Classes: {self.classes}")
```

---

## Fallback Plans

### If Spike Fails

**Option A**: Build Custom Widget
- Don't extend TextArea
- Build from Widget base class
- Implement own text buffer
- Effort: +2-3 weeks

**Option B**: Use Different Approach
- Use textual-vim (PTY wrapper)
- Accept file-based limitation
- Build adapter layer
- Effort: +1 week

**Option C**: Abandon Vim
- Use standard TextArea
- No vim modes
- Simplest but lose main feature
- Effort: 0

**Option D**: Reconsider Original Plan
- Go back to extending current textbox
- Rich library + custom MVC
- Known quantity
- Effort: ~27 days (original estimate)

---

## Resources

### Textual Documentation
- TextArea: https://textual.textualize.io/widgets/text_area/
- Key events: https://textual.textualize.io/guide/events/#key
- CSS: https://textual.textualize.io/guide/CSS/
- Testing: https://textual.textualize.io/guide/testing/

### Debugging
```bash
# Run with console for logging
textual console &
textual run --dev spike_vim.py

# Check logs
tail -f textual.log
```

### Getting Help
- Textual Discord: https://discord.gg/Enf6Z3qhVr
- GitHub Issues: https://github.com/Textualize/textual/issues

---

## Checklist

### Day 1
- [ ] Environment set up
- [ ] VimTextArea class created
- [ ] Mode switching works
- [ ] Border changes by mode
- [ ] hjkl navigation implemented
- [ ] Manual testing completed

### Day 2
- [ ] 0, $ navigation added
- [ ] 'a' append mode works
- [ ] 'x' delete works
- [ ] Real usage testing done
- [ ] TextArea limitations documented
- [ ] Edge cases tested

### Day 3
- [ ] Performance measured
- [ ] Spike report written
- [ ] Demo prepared
- [ ] Decision made
- [ ] Next steps clear

---

**Ready to start?** Set up your environment and begin Day 1!

**Questions?** Refer to [VIM_TEXTAREA.md](VIM_TEXTAREA.md) for detailed design, or [IMPLEMENTATION.md](IMPLEMENTATION.md) for full timeline.
