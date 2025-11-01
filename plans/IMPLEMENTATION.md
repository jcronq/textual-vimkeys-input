# Implementation Plan - Detailed Timeline

**Total Estimated Effort**: 20-28 days (4-5.5 weeks)
**Approach**: Iterative development with TDD
**Phases**: 5 phases from spike to production

---

## Phase Overview

| Phase | Duration | Goal | Status |
|-------|----------|------|--------|
| **Phase 0: Spike** | 2-3 days | Validate VimTextArea feasibility | ⏳ Next |
| **Phase 1: Basic Vim** | 5-7 days | Core modes and navigation | ⏳ Pending |
| **Phase 2: Advanced Vim** | 5-7 days | Full vim feature set | ⏳ Pending |
| **Phase 3: Chat App** | 5-7 days | Complete chat application | ⏳ Pending |
| **Phase 4: Polish** | 3-4 days | Production ready | ⏳ Pending |

---

## Phase 0: Spike / Validation (2-3 days)

**Goal**: Prove that extending TextArea for vim modes is feasible and feels right

**Key Questions to Answer**:
1. Can we intercept keys in TextArea effectively?
2. Do mode transitions feel responsive?
3. Does hjkl navigation work smoothly?
4. Can we style based on mode?
5. Does it feel like vim?

### Day 1: Setup & Basic Structure

**Morning (4 hours)**:
- [ ] Install Textual and dependencies
  ```bash
  pip install textual textual-dev rich
  ```
- [ ] Create project structure
  ```
  textbox/
  ├── textbox/
  │   ├── __init__.py
  │   └── vim_textarea.py
  ├── tests/
  │   └── test_vim_textarea.py
  └── examples/
      └── spike.py
  ```
- [ ] Create minimal VimTextArea class extending TextArea
- [ ] Add mode tracking (INSERT, COMMAND)
- [ ] Verify widget renders

**Afternoon (4 hours)**:
- [ ] Implement ESC key handling (INSERT → COMMAND)
- [ ] Implement 'i' key handling (COMMAND → INSERT)
- [ ] Add CSS for mode-based borders
- [ ] Test mode switching feels instant
- [ ] Create simple example app

**Deliverable**: Widget that switches modes with visual feedback

### Day 2: Navigation & Editing

**Morning (4 hours)**:
- [ ] Implement hjkl navigation in command mode
- [ ] Test navigation feels natural
- [ ] Implement 0 and $ (line start/end)
- [ ] Test with different text lengths

**Afternoon (4 hours)**:
- [ ] Implement 'a' (append after cursor)
- [ ] Implement 'x' (delete character)
- [ ] Test editing operations
- [ ] Create test suite for basic features
- [ ] Document any TextArea limitations found

**Deliverable**: Basic vim navigation and editing works

### Day 3: Validation & Decision

**Morning (3 hours)**:
- [ ] Test with real usage patterns
- [ ] Type several messages with mode switching
- [ ] Evaluate responsiveness
- [ ] Check for any blocking issues
- [ ] Measure key latency

**Afternoon (3 hours)**:
- [ ] Write spike report
- [ ] List what works well
- [ ] List any concerns or blockers
- [ ] Decide: proceed or pivot?
- [ ] If proceed: plan Phase 1 details
- [ ] If pivot: design alternative approach

**Decision Point**: GO / NO-GO for full implementation

**Success Criteria**:
- ✅ Mode switching feels instant (<50ms)
- ✅ hjkl navigation works smoothly
- ✅ No major TextArea API blockers
- ✅ Feels like vim (subjective but important)
- ✅ Team consensus to proceed

**If GO**: Continue to Phase 1
**If NO-GO**: Evaluate alternatives (see fallback section)

---

## Phase 1: Basic Vim (5-7 days)

**Goal**: Core vim editing experience

**Prerequisites**: Phase 0 spike succeeded

### Day 4-5: Core Navigation (2 days)

**Tasks**:
- [ ] **hjkl** - Refine from spike
- [ ] **0, $** - Line start/end
- [ ] **gg, G** - Document start/end
- [ ] **w, b** - Word navigation
- [ ] **e** - End of word

**Tests**:
```python
def test_h_moves_left():
    widget.text = "hello"
    widget.cursor = (0, 3)
    widget.vim_mode = COMMAND
    widget.press("h")
    assert widget.cursor == (0, 2)

def test_gg_moves_to_start():
    widget.text = "line1\nline2\nline3"
    widget.cursor = (2, 0)
    widget.press("g")
    widget.press("g")
    assert widget.cursor == (0, 0)
```

**Deliverable**: All basic navigation works

### Day 6-7: Mode Transitions (2 days)

**Tasks**:
- [ ] **i** - Insert at cursor
- [ ] **a** - Append after cursor
- [ ] **I** - Insert at line start
- [ ] **A** - Append at line end
- [ ] **o** - Open line below
- [ ] **O** - Open line above
- [ ] **ESC** - Back to command mode (already done)

**Tests**:
```python
def test_i_enters_insert_mode():
    widget.vim_mode = COMMAND
    widget.press("i")
    assert widget.vim_mode == INSERT

def test_o_opens_line_below():
    widget.text = "line1"
    widget.cursor = (0, 0)
    widget.press("o")
    assert widget.vim_mode == INSERT
    assert widget.text == "line1\n"
    assert widget.cursor == (1, 0)
```

**Deliverable**: Can enter insert mode from any command

### Day 8: Basic Editing (1 day)

**Tasks**:
- [ ] **x** - Delete character
- [ ] **X** - Delete left
- [ ] **u** - Undo
- [ ] **Ctrl+r** - Redo

**Tests**:
```python
def test_x_deletes_char():
    widget.text = "hello"
    widget.cursor = (0, 1)  # On 'e'
    widget.press("x")
    assert widget.text == "hllo"

def test_u_undoes():
    widget.text = "hello"
    widget.press("x")  # Delete 'h'
    assert widget.text == "ello"
    widget.press("u")
    assert widget.text == "hello"
```

**Deliverable**: Basic editing operations work

### Day 9-10: Polish & Integration (2 days)

**Tasks**:
- [ ] Mode indicator in footer/status
- [ ] Border styling based on mode
- [ ] Pending command indicator (for dd, yy)
- [ ] Fix any edge cases found
- [ ] Complete test coverage for Phase 1
- [ ] Documentation for basic features

**Tests**:
- [ ] Test all combinations
- [ ] Test edge cases (empty buffer, single character, etc.)
- [ ] Test rapid mode switching
- [ ] Test undo/redo chains

**Deliverable**: Solid basic vim implementation

**Milestone**: Can use for basic text input with vim feel

---

## Phase 2: Advanced Vim (5-7 days)

**Goal**: Complete vim feature set for text editing

### Day 11-12: Line Operations (2 days)

**Tasks**:
- [ ] **dd** - Delete line
- [ ] **yy** - Yank (copy) line
- [ ] **p** - Paste after cursor
- [ ] **P** - Paste before cursor
- [ ] Yank register management

**Implementation**:
```python
def _handle_command_mode(self, event):
    if key == "d":
        self.pending_command = "d"
    elif self.pending_command == "d" and key == "d":
        self._delete_line()
        self.pending_command = None
```

**Tests**:
```python
def test_dd_deletes_line():
    widget.text = "line1\nline2\nline3"
    widget.cursor = (1, 0)
    widget.press("d")
    widget.press("d")
    assert widget.text == "line1\nline3"

def test_yy_p_copy_paste():
    widget.text = "hello"
    widget.press("y")
    widget.press("y")  # Yank line
    widget.press("p")  # Paste
    assert "hello" in widget.text  # Appears twice
```

**Deliverable**: Line operations work

### Day 13-15: Visual Mode (3 days)

**Tasks**:
- [ ] **v** - Enter visual mode
- [ ] **hjkl** - Extend selection
- [ ] **w, b** - Select words
- [ ] **y** - Yank selection
- [ ] **d** - Delete selection
- [ ] **ESC** - Exit visual mode
- [ ] Visual feedback (highlighted selection)

**Implementation**:
```python
def _enter_visual_mode(self):
    self.vim_mode = VISUAL
    self.visual_start = self.cursor_location
    # TextArea selection API

def _handle_visual_mode(self, event):
    if key == "h":
        self.action_cursor_left_select()
    elif key == "y":
        self._yank_selection()
        self._enter_command_mode()
```

**Tests**:
```python
def test_visual_mode_selection():
    widget.text = "hello world"
    widget.cursor = (0, 0)
    widget.press("v")  # Visual mode
    for _ in range(5):
        widget.press("l")  # Select 5 chars
    widget.press("d")  # Delete
    assert widget.text == " world"
```

**Deliverable**: Visual selection works

### Day 16-17: Advanced Features (2 days)

**Tasks**:
- [ ] **r** - Replace character
- [ ] **f/F** - Find character forward/backward
- [ ] **t/T** - Till character forward/backward
- [ ] **;** - Repeat find
- [ ] **^** - First non-whitespace
- [ ] **Ctrl+d/u** - Page down/up (if useful)

**Tests**: Cover each new feature

**Deliverable**: Advanced vim motions work

**Milestone**: Feature-complete vim editing

---

## Phase 3: Chat Application (5-7 days)

**Goal**: Production-ready chat application using VimTextArea

### Day 18-19: Basic Chat App (2 days)

**Tasks**:
- [ ] Create ChatApp class
- [ ] Layout: Header, RichLog (output), VimTextArea (input), Footer
- [ ] Submit on Enter in insert mode
- [ ] Display user messages
- [ ] Basic AI response (echo or placeholder)
- [ ] Clear input after submit

**Code**:
```python
class ChatApp(App):
    def compose(self):
        yield Header()
        yield RichLog(id="history")
        yield VimTextArea(id="input")
        yield Footer()

    async def on_vim_text_area_submitted(self, event):
        history = self.query_one("#history")
        history.write(f"You: {event.text}")
        response = await self.get_ai_response(event.text)
        history.write(f"AI: {response}")
```

**Tests**:
- [ ] App launches
- [ ] Can type and submit
- [ ] Messages appear in history
- [ ] Input clears after submit

**Deliverable**: Working chat interface

### Day 20-21: Streaming Responses (2 days)

**Tasks**:
- [ ] Implement streaming response handler
- [ ] Token-by-token output to RichLog
- [ ] Thinking indicator while waiting
- [ ] Handle streaming errors gracefully
- [ ] Test with actual LLM API

**Code**:
```python
async def on_vim_text_area_submitted(self, event):
    history = self.query_one("#history")
    history.write(f"You: {event.text}")
    history.write("AI: ", end="")

    async for token in self.stream_llm(event.text):
        history.write(token, end="")

    history.write("")  # New line
```

**Tests**:
- [ ] Streaming works smoothly
- [ ] No UI blocking during stream
- [ ] Can interrupt stream
- [ ] Error handling works

**Deliverable**: Streaming chat works

### Day 22-23: Command Palette (1-2 days)

**Tasks**:
- [ ] Create custom command provider
- [ ] Commands: clear, save, export, theme change
- [ ] Implement each command
- [ ] Test command palette (Ctrl+\\)
- [ ] Help text for commands

**Code**:
```python
class ChatCommands(Provider):
    async def search(self, query):
        yield Hit("clear", "Clear history")
        yield Hit("save", "Save conversation")
        yield Hit("theme-dark", "Dark theme")

class ChatApp(App):
    COMMANDS = {ChatCommands}
```

**Deliverable**: Command palette works

### Day 24: Themes & Polish (1 day)

**Tasks**:
- [ ] Create CSS styling
- [ ] Implement theme switching
- [ ] Add status bar with mode indicator
- [ ] Polish borders and colors
- [ ] Add welcome message

**Deliverable**: Beautiful, polished UI

**Milestone**: Production-ready chat app

---

## Phase 4: Polish & Production (3-4 days)

**Goal**: Release-ready package with docs and examples

### Day 25-26: Documentation (2 days)

**Tasks**:
- [ ] Write comprehensive README
- [ ] API documentation for VimTextArea
- [ ] Usage guide for chat app
- [ ] Architecture documentation
- [ ] Contributing guide
- [ ] License file

**Deliverable**: Complete documentation

### Day 27: Examples (1 day)

**Tasks**:
- [ ] Example 1: Basic VimTextArea demo
- [ ] Example 2: Simple chat
- [ ] Example 3: Streaming chat
- [ ] Example 4: Multi-agent chat
- [ ] Example 5: Custom commands

**Deliverable**: 5 working examples

### Day 28: Package & Release (1 day)

**Tasks**:
- [ ] Set up pyproject.toml
- [ ] Configure build system
- [ ] Run all tests (100+ tests)
- [ ] Verify coverage (>80%)
- [ ] Create release notes
- [ ] Tag v2.0.0
- [ ] Publish to PyPI (optional)

**Deliverable**: Release package

---

## Testing Strategy

### Test Pyramid

```
        E2E Tests (5%)
       /            \
      /   Integration  \
     /      Tests (15%)  \
    /________________________\
          Unit Tests (80%)
```

### Unit Tests (Target: 100+ tests)

**VimTextArea**:
- Mode switching (10 tests)
- Navigation (20 tests)
- Editing (15 tests)
- Visual mode (10 tests)
- Edge cases (15 tests)

**Example**:
```python
# tests/test_vim_textarea.py

@pytest.mark.asyncio
async def test_hjkl_navigation():
    async with VimTextAreaApp().run_test() as pilot:
        widget = pilot.app.query_one(VimTextArea)
        widget.text = "hello\nworld"

        # Start in command mode
        await pilot.press("escape")

        # Test h (left)
        widget.cursor = (0, 3)
        await pilot.press("h")
        assert widget.cursor[1] == 2

        # Test l (right)
        await pilot.press("l")
        assert widget.cursor[1] == 3

        # Test j (down)
        await pilot.press("j")
        assert widget.cursor[0] == 1

        # Test k (up)
        await pilot.press("k")
        assert widget.cursor[0] == 0
```

### Integration Tests (Target: 15-20 tests)

**Chat App**:
- Message submission (5 tests)
- Streaming (3 tests)
- Commands (5 tests)
- Theming (2 tests)

**Example**:
```python
# tests/test_chat_app.py

@pytest.mark.asyncio
async def test_submit_message():
    async with ChatApp().run_test() as pilot:
        input_widget = pilot.app.query_one(VimTextArea)
        history = pilot.app.query_one("#history")

        # Type message
        input_widget.text = "Hello"

        # Submit (Enter in insert mode)
        await pilot.press("enter")

        # Check history updated
        # (Would need RichLog test API)
```

### E2E Tests (Target: 5 tests)

**Full workflows**:
- Complete conversation (type, submit, response, repeat)
- Mode switching during conversation
- Command palette usage
- Theme switching
- Error recovery

---

## Risk Mitigation

### Risk 1: Phase 0 Spike Fails

**If TextArea too limited**:

**Fallback A**: Build custom widget from scratch
- Effort: +2-3 weeks
- Use TextArea code as reference
- Implement own text buffer

**Fallback B**: Use textual-vim approach (PTY wrapper)
- Effort: +1 week for integration
- Accept file-based limitation
- Build adapter layer

**Fallback C**: Abandon vim, use standard TextArea
- Effort: 0 (existing Textual feature)
- Lose vim editing
- Simplest but least desirable

### Risk 2: Timeline Overruns

**Mitigation**:
- Ship incrementally (basic vim first)
- Phase 1 + Phase 3 = minimal viable product
- Phase 2 + Phase 4 = polish and advanced features
- Can release v2.0 with basic vim, v2.1 with advanced

### Risk 3: Performance Issues

**If VimTextArea slow**:
- Profile with cProfile
- Optimize hot paths (key handling)
- Add debouncing if needed
- Textual has built-in profiling: `textual run --dev`

### Risk 4: Vim Feel Not Right

**If doesn't feel like vim**:
- Iterate on key latency
- Adjust mode transition timing
- Get user feedback early
- Consider animation/feedback improvements

---

## Success Metrics

### Phase 0 Success
- [ ] Mode switching <50ms
- [ ] hjkl navigation smooth
- [ ] Feels vim-like
- [ ] No blocking issues

### Phase 1 Success
- [ ] All basic vim features work
- [ ] 30+ unit tests passing
- [ ] Can write simple messages comfortably

### Phase 2 Success
- [ ] All advanced vim features work
- [ ] 60+ unit tests passing
- [ ] Feels like real vim for text editing

### Phase 3 Success
- [ ] Can have full conversations
- [ ] Streaming works smoothly
- [ ] Commands functional
- [ ] Pleasant to use

### Phase 4 Success
- [ ] 100+ tests passing
- [ ] Documentation complete
- [ ] 5+ examples working
- [ ] Ready to ship

---

## Daily Workflow

### Development Cycle

**Morning**:
1. Review previous day's work
2. Run all tests
3. Pick task from phase plan
4. Write tests first (TDD)

**Afternoon**:
5. Implement features
6. Make tests pass
7. Refactor if needed
8. Document changes
9. Commit with good messages

**Evening**:
10. Run full test suite
11. Manual testing
12. Update progress
13. Plan next day

### Tools

```bash
# Hot reload during development
textual run --dev examples/spike.py

# Run tests with coverage
pytest tests/ --cov=textbox --cov-report=html

# Type checking
mypy textbox/

# Formatting
black textbox/ tests/
```

---

## Progress Tracking

### Weekly Checkpoints

**End of Week 1** (Phase 0 + 1):
- [ ] Spike complete and approved
- [ ] Basic vim implemented
- [ ] 30+ tests passing
- [ ] Demo working

**End of Week 2** (Phase 2):
- [ ] Advanced vim complete
- [ ] 60+ tests passing
- [ ] Visual mode working
- [ ] Feature complete vim

**End of Week 3** (Phase 3):
- [ ] Chat app working
- [ ] Streaming implemented
- [ ] Commands functional
- [ ] 80+ tests passing

**End of Week 4** (Phase 4):
- [ ] Documentation done
- [ ] Examples complete
- [ ] 100+ tests passing
- [ ] Ready to release

---

## Next Steps

**Immediate**:
1. ✅ Review this implementation plan
2. ⏳ Set up development environment
3. ⏳ Start Phase 0: Spike (2-3 days)

**After Spike**:
4. Review spike results
5. Make GO/NO-GO decision
6. If GO: Continue to Phase 1
7. If NO-GO: Evaluate fallbacks

---

See [SPIKE_GUIDE.md](SPIKE_GUIDE.md) for detailed spike instructions.
