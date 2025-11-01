# Textbox Reimagined: Textual Framework + VimTextArea

**Date**: 2025-11-01
**Decision**: Migrate from custom curses implementation to Textual framework
**Target**: textbox v2.0 (or new project name?)
**Estimated Effort**: 20-25 days (4-5 weeks)

---

## Executive Summary

### The Decision

**Rebuild textbox using Textual framework with a custom VimTextArea widget.**

### Why This Approach

Your requirements:
1. ✅ **Chat interface** - Textual's RichLog widget is perfect
2. ✅ **Vim-like editing** - Custom VimTextArea widget (our only custom component)
3. ✅ **Custom commands** - Textual's command palette (Ctrl+P) is acceptable
4. ✅ **Beautiful output** - Textual excels at this (Rich integration, CSS, themes)

### What Changes

| Old (textbox + curses) | New (Textual) |
|------------------------|---------------|
| Custom curses rendering | Textual's rendering engine |
| Custom Text/TextLine classes | Textual's TextArea |
| Custom color system | CSS theming |
| Fixed layout (3 boxes) | Flexible layouts (Grid, HSplit, VSplit) |
| Manual window management | Textual's widget tree |
| Custom command system (`:cmd`) | Textual command palette (Ctrl+P) |
| **Keep: Vim editing** | **Custom VimTextArea widget** |

### What We Get

From **Textual (built-in)**:
- ✅ RichLog widget for streaming chat output
- ✅ CSS-based theming (dark/light/custom)
- ✅ Layout system (Grid, HSplit, VSplit, responsive)
- ✅ Command palette (Ctrl+P, fuzzy search)
- ✅ Rich text support (bold, italic, colors, syntax highlighting)
- ✅ Widget library (buttons, tabs, trees, tables)
- ✅ Hot reload during development
- ✅ Excellent documentation and community

From **custom VimTextArea**:
- ✅ Vim modes (insert, command, visual)
- ✅ Vim navigation (hjkl, w, b, e, 0, $, gg, G)
- ✅ Vim editing (x, dd, yy, p, u, Ctrl+r)
- ✅ Visual selection
- ✅ Mode indicators

### Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| **Phase 0: Spike** | 2-3 days | Validate VimTextArea approach |
| **Phase 1: Basic Vim** | 5-7 days | Insert/command modes, hjkl |
| **Phase 2: Advanced Vim** | 5-7 days | Word motions, dd/yy/p, visual mode |
| **Phase 3: Chat App** | 5-7 days | Full chat interface with streaming |
| **Phase 4: Polish** | 3-4 days | Themes, docs, examples |
| **Total** | **20-28 days** | **Production-ready v2.0** |

---

## Quick Links

### Planning Documents

1. 📋 **[README.md](README.md)** (this file) - Overview and decision summary
2. 🏗️ **[VIM_TEXTAREA.md](VIM_TEXTAREA.md)** - VimTextArea widget implementation guide
3. 💬 **[CHAT_APP.md](CHAT_APP.md)** - Chat application architecture and examples
4. 📝 **[IMPLEMENTATION.md](IMPLEMENTATION.md)** - Phase-by-phase implementation guide
5. 🚀 **[SPIKE_GUIDE.md](SPIKE_GUIDE.md)** - 2-3 day spike/prototype instructions

### Reference

6. 📚 **[TEXTUAL_FEATURES.md](TEXTUAL_FEATURES.md)** - What Textual provides out-of-box
7. 🔄 **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - Migrating from old textbox API

---

## Key Architectural Decisions

### Decision 1: Use Textual Framework

**Rationale**:
- Textual provides 90% of what we need (output, theming, layouts, commands)
- We only need to build 10% (VimTextArea)
- Maintained framework with active community
- Excellent documentation

**Trade-off**:
- Lose some flexibility (framework constraints)
- Class-based App model instead of callback-based
- Must follow Textual's patterns

**Verdict**: ✅ Benefits far outweigh trade-offs

### Decision 2: Ctrl+P for Commands (Not `:`)

**Rationale**:
- Textual's command palette is powerful (fuzzy search, help text)
- Reduces scope (no need to build `:` command parsing)
- Modern pattern (like VS Code Ctrl+Shift+P)

**Trade-off**:
- Less "vim-like" (vim uses `:w`, `:q`, etc.)
- Different muscle memory

**Verdict**: ✅ Acceptable for the benefits gained

### Decision 3: Extend TextArea (Not Build from Scratch)

**Rationale**:
- TextArea already has multi-line editing, undo/redo, selection
- Has cursor actions we can use (move left/right/up/down, word navigation)
- Solid foundation, just need to add vim modes

**Trade-off**:
- Constrained by TextArea's API
- May have limitations we don't know yet

**Verdict**: ✅ Spike will validate this (Phase 0)

### Decision 4: Separate Widget (Not Monolithic App)

**Rationale**:
- VimTextArea should be reusable component
- Can be used in other Textual apps
- Clean separation of concerns

**Deliverables**:
- `textbox/vim_textarea.py` - VimTextArea widget
- `textbox/chat_app.py` - Example chat application
- `textbox/` can become a library of Textual vim components

---

## Project Structure

```
textbox/
├── textbox/
│   ├── __init__.py
│   ├── vim_textarea.py          # VimTextArea widget
│   ├── vim_modes.py              # Vim mode enum and state
│   ├── chat_app.py               # Example chat app
│   └── commands.py               # Command palette providers
├── examples/
│   ├── 01_basic_vim_input.py    # VimTextArea demo
│   ├── 02_simple_chat.py        # Simple chat with LLM
│   ├── 03_multi_agent_chat.py   # Multi-agent chat
│   ├── 04_streaming_demo.py     # Streaming response demo
│   └── 05_custom_commands.py    # Custom command palette
├── tests/
│   ├── test_vim_textarea.py     # VimTextArea tests
│   ├── test_vim_modes.py        # Mode switching tests
│   └── test_chat_app.py         # Chat app tests
├── docs/
│   ├── vim_textarea.md          # VimTextArea docs
│   ├── chat_app.md              # Chat app guide
│   └── commands.md              # Command system docs
├── pyproject.toml               # Dependencies (textual, rich, etc.)
├── requirements.txt
└── README.md
```

---

## Technology Stack

### Core Dependencies

```toml
[project]
name = "textbox"
version = "2.0.0"
dependencies = [
    "textual>=0.47.0",      # TUI framework
    "rich>=13.7.0",          # Rich text (used by Textual)
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "textual-dev>=1.0.0",    # Hot reload, debugging
]
```

### What Each Provides

**Textual**:
- TUI framework
- Widget library (RichLog, Header, Footer, etc.)
- Layout system
- Event system
- CSS theming
- Command palette

**Rich** (used by Textual):
- Text rendering
- Syntax highlighting
- Tables, panels
- Colors and styles

---

## Comparison: Old vs New

### Code Comparison

**Old textbox (callback-based)**:
```python
from textbox import App

app = App()

@app.on_submit
def handle(text: str):
    app.print("Response")

@app.command("greet", help="Say hello")
def greet(name: str):
    app.print(f"Hello, {name}!")

app.start()
```

**New textbox (Textual-based)**:
```python
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, RichLog
from textbox import VimTextArea

class ChatApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield RichLog(id="output")
        yield VimTextArea(id="input")
        yield Footer()

    async def on_vim_text_area_submitted(self, event):
        output = self.query_one("#output")
        output.write(f"You said: {event.text}")

if __name__ == "__main__":
    app = ChatApp()
    app.run()
```

**Observations**:
- More verbose (class-based vs callback-based)
- More explicit (compose() method)
- More structured (Textual patterns)
- More powerful (access to full Textual API)

### Feature Comparison

| Feature | Old textbox | New textbox | Status |
|---------|-------------|-------------|--------|
| **Vim editing** | ✅ Full | ✅ Full (VimTextArea) | Keep |
| **Input modes** | ✅ INSERT, COMMAND, VISUAL | ✅ Same | Keep |
| **Navigation** | ✅ hjkl, w, b, e, etc. | ✅ Same | Keep |
| **Commands** | ✅ `:cmd` syntax | ✅ Ctrl+P palette | Change |
| **Output** | ⚠️ Basic colors | ✅ Rich text, syntax highlighting | Better |
| **Theming** | ⚠️ Basic | ✅ CSS, themes | Better |
| **Layouts** | ❌ Fixed (3 boxes) | ✅ Flexible (Grid, Split) | Better |
| **Widgets** | ❌ Only TextBox, InputBox | ✅ Buttons, tabs, trees, tables | Better |
| **Docs** | ⚠️ README | ✅ Full docs + Textual docs | Better |
| **Examples** | ⚠️ Few | ✅ Many + Textual examples | Better |
| **Hot reload** | ❌ No | ✅ Yes (textual dev) | Better |
| **Mouse support** | ❌ No | ✅ Yes | Better |

---

## Success Criteria

### Phase 0: Spike (2-3 days)

**Goal**: Validate that extending TextArea for vim is feasible

**Success**:
- [ ] VimTextArea widget exists
- [ ] Can switch between insert/command modes
- [ ] hjkl navigation works in command mode
- [ ] ESC switches modes
- [ ] Border color changes by mode
- [ ] Feels responsive and natural

**Failure**: If TextArea is too limiting, reconsider approach

### Phase 1: Basic Vim (5-7 days)

**Goal**: Core vim editing works

**Success**:
- [ ] All basic navigation (hjkl, 0, $, gg, G)
- [ ] Mode switching (i, a, I, A, ESC)
- [ ] Basic editing (x, dd, u, Ctrl+r)
- [ ] Mode indicator in footer
- [ ] All unit tests pass

### Phase 2: Advanced Vim (5-7 days)

**Goal**: Complete vim feature set

**Success**:
- [ ] Word motions (w, b, e, ge)
- [ ] yy, p (yank/paste)
- [ ] Visual mode (v, hjkl selection, y, d)
- [ ] Character search (f, t)
- [ ] All advanced tests pass

### Phase 3: Chat App (5-7 days)

**Goal**: Full chat application

**Success**:
- [ ] Chat interface with VimTextArea input
- [ ] Streaming LLM responses
- [ ] Command palette with custom commands
- [ ] Multiple themes
- [ ] Example with multiple agents/panels

### Phase 4: Polish (3-4 days)

**Goal**: Production-ready

**Success**:
- [ ] Documentation complete
- [ ] 5+ examples
- [ ] Tests passing (>80% coverage)
- [ ] README with quick start
- [ ] PyPI package published

---

## Risk Assessment

### Risk 1: TextArea Too Limited

**Probability**: 20%
**Impact**: High (need different approach)
**Mitigation**: Phase 0 spike validates feasibility
**Fallback**: Build custom widget from scratch (+2-3 weeks)

### Risk 2: Vim Behavior Doesn't Feel Right

**Probability**: 30%
**Impact**: Medium (refinement needed)
**Mitigation**: Early testing with real usage
**Fallback**: Iterate on key handling

### Risk 3: Timeline Overrun

**Probability**: 40%
**Impact**: Low (can ship incrementally)
**Mitigation**:
- Phase 0 validates approach
- Can ship with basic vim first
- Advanced features in v2.1

### Risk 4: Textual API Changes

**Probability**: 10%
**Impact**: Medium
**Mitigation**:
- Pin Textual version
- Textual has stable API (v0.47+)
- Active maintenance

---

## Migration Path

### For Existing textbox Users

We'll provide migration guide and compatibility layer:

```python
# Old API (textbox v1)
from textbox import App

app = App()

@app.on_submit
def handle(text: str):
    app.print("Response")

# New API (textbox v2 - compatibility mode)
from textbox.compat import App

app = App()  # Wraps Textual app

@app.on_submit
async def handle(text: str):  # Now async
    app.print("Response")  # Still works

# New API (textbox v2 - native)
from textbox import ChatApp
from textual.app import ComposeResult

class MyApp(ChatApp):
    async def on_message_submitted(self, event):
        self.output.write(f"You: {event.text}")
```

**Strategy**:
1. v2.0 ships with new Textual-based API
2. v2.1 adds compatibility layer for old API
3. v1.x stays available for those who need it

---

## Next Steps

### Immediate (This Week)

1. **Review this plan** ✋
   - Approve overall approach
   - Identify any concerns
   - Decide on project name (keep "textbox" or rename?)

2. **Set up environment** 🔧
   ```bash
   pip install textual textual-dev rich
   ```

3. **Start Phase 0: Spike** 🚀
   - Follow [SPIKE_GUIDE.md](SPIKE_GUIDE.md)
   - Build minimal VimTextArea
   - Validate approach (2-3 days)

### Short-term (Next 2 Weeks)

4. **Phase 1: Basic Vim** (if spike succeeds)
   - Implement core vim modes
   - Basic navigation and editing
   - Unit tests

5. **Phase 2: Advanced Vim**
   - Complete vim feature set
   - Visual mode
   - All tests passing

### Medium-term (Weeks 3-4)

6. **Phase 3: Chat App**
   - Build example chat application
   - Streaming support
   - Command palette

7. **Phase 4: Polish**
   - Documentation
   - Examples
   - PyPI package

---

## Questions & Decisions Needed

### 1. Project Name

**Options**:
- Keep "textbox" (v2.0 is major rewrite)
- Rename to something new (vim-textual? textual-vim? vim-chat?)

**Recommendation**: Keep "textbox" - it's a major version bump (v2.0)

### 2. API Compatibility

**Options**:
- v2.0 is completely new API (breaking change)
- v2.0 has compatibility layer for v1.x API
- Maintain v1.x separately

**Recommendation**: v2.0 is new API, add compat layer in v2.1

### 3. Repository

**Options**:
- Same repo, new branch (main becomes v2.0)
- New repo (textbox-v2)
- Same repo, v1.x branch for old version

**Recommendation**: Same repo, new main branch (v2.0), v1.x branch frozen

---

## Resources

### Textual Documentation
- Main docs: https://textual.textualize.io/
- Tutorial: https://textual.textualize.io/tutorial/
- Widget guide: https://textual.textualize.io/widgets/
- Styling guide: https://textual.textualize.io/guide/CSS/

### Textual Examples
- Official examples: https://github.com/Textualize/textual/tree/main/examples
- Showcase: https://github.com/Textualize/awesome-textual

### Development Tools
- Textual dev mode: `textual run --dev app.py` (hot reload)
- Textual console: `textual console` (debug logging)
- Textual keys: https://textual.textualize.io/guide/input/#key

---

## Document Status

| Document | Status | Purpose |
|----------|--------|---------|
| README.md | ✅ Complete | Overview and entry point |
| VIM_TEXTAREA.md | 🚧 In Progress | VimTextArea implementation |
| CHAT_APP.md | 🚧 In Progress | Chat app architecture |
| IMPLEMENTATION.md | 🚧 In Progress | Phase-by-phase guide |
| SPIKE_GUIDE.md | 🚧 In Progress | Spike instructions |
| TEXTUAL_FEATURES.md | ⏳ Pending | Textual reference |
| MIGRATION_GUIDE.md | ⏳ Pending | Migration from v1.x |

---

**Ready to start?** → Review this plan, then proceed to [SPIKE_GUIDE.md](SPIKE_GUIDE.md) for the 2-3 day validation phase.
