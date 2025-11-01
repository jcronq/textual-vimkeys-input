# Complete Plan: Textbox with Textual Framework

**Status**: ✅ Planning Complete - Ready to Start
**Date**: 2025-11-01
**Estimated Effort**: 20-28 days (4-5.5 weeks)

---

## Quick Start

**New here?** Read in this order:

1. 📋 **[README.md](README.md)** - Overview, decision rationale, and timeline
2. 🚀 **[SPIKE_GUIDE.md](SPIKE_GUIDE.md)** - Start here! 2-3 day validation prototype
3. 🏗️ **[VIM_TEXTAREA.md](VIM_TEXTAREA.md)** - VimTextArea widget implementation
4. 💬 **[CHAT_APP.md](CHAT_APP.md)** - Chat application patterns and examples
5. 📝 **[IMPLEMENTATION.md](IMPLEMENTATION.md)** - Detailed 28-day timeline

**Supporting Docs**:
6. 🔍 **[TEXTUAL_VIM_ANALYSIS.md](TEXTUAL_VIM_ANALYSIS.md)** - Analysis of existing textual-vim library

---

## The Decision

**Build textbox v2.0 using Textual framework + custom VimTextArea widget**

### Why This Approach Won

| What We Need | Textual Provides | We Build |
|--------------|------------------|----------|
| Vim editing | ❌ | ✅ **VimTextArea widget** |
| Beautiful output | ✅ RichLog widget | |
| Streaming | ✅ Built-in | |
| Commands | ✅ Command palette (Ctrl+P) | |
| Themes | ✅ CSS + built-in themes | |
| Layouts | ✅ Grid, HSplit, VSplit | |
| Docs | ✅ Excellent | |
| Community | ✅ Large, active | |

**Effort**: 20-28 days
**Payoff**: Production-ready chat framework with vim editing

---

## Document Guide

### Core Documents (Read These)

#### [README.md](README.md) - Project Overview
**Purpose**: High-level overview and decision summary
**Key Sections**:
- Executive summary
- Technology stack (Textual + Rich)
- Timeline: 4-5.5 weeks
- Success criteria
- Architecture decisions
- Risk assessment

#### [SPIKE_GUIDE.md](SPIKE_GUIDE.md) - 2-3 Day Validation
**Purpose**: Validate approach before full commitment
**Key Sections**:
- Day 1: Basic structure & mode switching
- Day 2: Navigation & editing
- Day 3: Validation & GO/NO-GO decision
- Success criteria
- Fallback plans

#### [VIM_TEXTAREA.md](VIM_TEXTAREA.md) - Widget Implementation
**Purpose**: Technical design for VimTextArea widget
**Key Sections**:
- Architecture (extends TextArea)
- VimMode enum
- Key handling by mode
- All vim operations (hjkl, dd, yy, p, visual)
- Testing strategy
- Implementation phases

#### [CHAT_APP.md](CHAT_APP.md) - Application Patterns
**Purpose**: How to build chat apps with VimTextArea
**Key Sections**:
- Simple chat pattern
- Streaming chat pattern
- Multi-agent chat pattern
- Command palette integration
- LLM integration examples (OpenAI, Anthropic)
- Themes and styling

#### [IMPLEMENTATION.md](IMPLEMENTATION.md) - Detailed Timeline
**Purpose**: Phase-by-phase, day-by-day implementation guide
**Key Sections**:
- Phase 0: Spike (2-3 days)
- Phase 1: Basic Vim (5-7 days)
- Phase 2: Advanced Vim (5-7 days)
- Phase 3: Chat App (5-7 days)
- Phase 4: Polish (3-4 days)
- Testing strategy
- Risk mitigation

### Supporting Documents

#### [TEXTUAL_VIM_ANALYSIS.md](TEXTUAL_VIM_ANALYSIS.md) - Existing Library Analysis
**Purpose**: Analysis of davidbrochart/textual-vim library
**Key Findings**:
- It's a PTY wrapper around real vim
- Not suitable for chat input widgets
- Good for file editing use cases
- Validates that vim-in-Textual is possible
- Confirms our architecture choice is correct

---

## Timeline Summary

### Phase 0: Spike (2-3 days) ← **START HERE**

**Goal**: Validate VimTextArea approach

**Deliverables**:
- Working prototype with mode switching
- hjkl navigation
- Basic editing
- GO/NO-GO decision

**Success**: Mode switching feels instant, navigation smooth, feels vim-like

### Phase 1: Basic Vim (5-7 days)

**Goal**: Core vim editing

**Deliverables**:
- All basic navigation (hjkl, 0, $, gg, G, w, b, e)
- Mode transitions (i, a, I, A, o, O)
- Basic editing (x, u, Ctrl+r)
- 30+ unit tests

**Success**: Can write messages comfortably with vim

### Phase 2: Advanced Vim (5-7 days)

**Goal**: Complete vim feature set

**Deliverables**:
- Line operations (dd, yy, p, P)
- Visual mode (v, hjkl selection, y, d)
- Advanced features (r, f/F/t/T)
- 60+ unit tests

**Success**: Feels like real vim for text editing

### Phase 3: Chat Application (5-7 days)

**Goal**: Production-ready chat app

**Deliverables**:
- Complete chat interface
- Streaming LLM responses
- Command palette with custom commands
- Themes
- 80+ unit tests

**Success**: Can have full conversations naturally

### Phase 4: Polish (3-4 days)

**Goal**: Release-ready package

**Deliverables**:
- Complete documentation
- 5+ examples
- 100+ tests passing
- PyPI package ready

**Success**: Production quality, ready to ship

---

## What You Get

### From Textual (Built-in)

✅ **RichLog widget**
- Perfect for streaming chat output
- Auto-scroll
- Rich text support (bold, colors, syntax highlighting)

✅ **Command Palette**
- Ctrl+P (or Ctrl+\\)
- Fuzzy search
- Custom commands
- Help text

✅ **CSS Theming**
- Dark/light themes
- Custom themes
- Per-widget styling
- Responsive layouts

✅ **Layout System**
- Grid, HSplit, VSplit
- Responsive resizing
- Flexbox-style
- Container widgets

✅ **Framework Features**
- Hot reload (`textual run --dev`)
- Debugging console
- Event system
- Widget tree
- Excellent docs

### From VimTextArea (We Build)

✅ **Vim Editing Modes**
- Insert mode
- Command mode
- Visual mode

✅ **Vim Navigation**
- hjkl (cursor movement)
- w, b, e (word motion)
- 0, $, gg, G (line/document navigation)
- f, t (character search)

✅ **Vim Editing**
- x (delete character)
- dd (delete line)
- yy, p (yank/paste)
- u, Ctrl+r (undo/redo)
- Visual selection

✅ **Integration**
- Submit on Enter in insert mode
- Mode indicators
- CSS styling
- Textual events
- Clean API

---

## Success Criteria

### Spike Success (Phase 0)
- [ ] Mode switching <50ms
- [ ] hjkl navigation smooth
- [ ] Feels vim-like
- [ ] No blocking issues

### MVP Success (Phase 1 + 3)
- [ ] Can write and send messages with vim
- [ ] Streaming responses work
- [ ] Basic commands functional
- [ ] Pleasant to use

### Production Success (All Phases)
- [ ] 100+ tests passing (>80% coverage)
- [ ] Documentation complete
- [ ] 5+ working examples
- [ ] No critical bugs
- [ ] Performance excellent

---

## Technology Stack

```toml
[project]
name = "textbox"
version = "2.0.0"
dependencies = [
    "textual>=0.47.0",    # TUI framework
    "rich>=13.7.0",        # Rich text (used by Textual)
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "textual-dev>=1.0.0",  # Hot reload
]
```

**What each provides**:
- **Textual**: Framework, widgets, layouts, CSS, events
- **Rich**: Text rendering, colors, syntax highlighting (used by Textual)
- **pytest**: Testing framework
- **textual-dev**: Development tools (hot reload, console)

---

## Project Structure

```
textbox/
├── textbox/
│   ├── __init__.py
│   ├── vim_textarea.py       # VimTextArea widget (our custom component)
│   ├── vim_modes.py          # VimMode enum
│   └── chat_app.py           # Example chat application
├── examples/
│   ├── 01_basic_vim.py       # VimTextArea demo
│   ├── 02_simple_chat.py     # Simple chat
│   ├── 03_streaming_chat.py  # Streaming responses
│   ├── 04_multi_agent.py     # Multi-agent chat
│   └── 05_custom_commands.py # Command palette
├── tests/
│   ├── test_vim_textarea.py  # Widget tests
│   ├── test_vim_modes.py     # Mode switching tests
│   └── test_chat_app.py      # Integration tests
├── docs/
│   ├── getting_started.md
│   ├── vim_textarea.md
│   └── chat_app.md
├── claude-output/
│   └── textual-plan/         # This planning documentation
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Key Decisions

### Decision 1: Textual Framework (Not Pure Refactor)
**Rationale**: Textual provides 90% of features we need. We only build VimTextArea (10%).
**Trade-off**: Framework constraints vs. feature completeness

### Decision 2: Extend TextArea (Not Build from Scratch)
**Rationale**: TextArea has multi-line editing, undo/redo, selection, cursor actions.
**Trade-off**: API limitations vs. development speed
**Validation**: Phase 0 spike proves this works

### Decision 3: Ctrl+P Commands (Not : Syntax)
**Rationale**: Textual's command palette is powerful, reduces scope.
**Trade-off**: Less vim-like vs. modern UX pattern

### Decision 4: ~80% Vim Coverage (Not 100%)
**Rationale**: Focus on most-used features for text editing.
**Trade-off**: Some advanced vim features missing vs. faster development

---

## Risks & Mitigation

### Risk 1: Spike Fails (20% probability)
**Impact**: High - need different approach
**Mitigation**: Phase 0 validates early
**Fallback**: Build custom widget from scratch (+2-3 weeks)

### Risk 2: Doesn't Feel Like Vim (30% probability)
**Impact**: Medium - need UX iteration
**Mitigation**: Early testing, rapid iteration
**Fallback**: Refine key handling, add feedback

### Risk 3: Timeline Overruns (40% probability)
**Impact**: Low - can ship incrementally
**Mitigation**: MVP is Phase 1 + Phase 3
**Fallback**: Ship basic vim first, advanced features in v2.1

### Risk 4: Performance Issues (10% probability)
**Impact**: Medium - affects UX
**Mitigation**: Profile early, optimize hot paths
**Fallback**: Textual has built-in profiling tools

---

## Why Not Other Approaches?

### Why Not textual-vim Library?
- ❌ PTY wrapper around real vim binary
- ❌ File-based editing (not suitable for chat input)
- ❌ Hard to integrate with chat patterns
- ❌ Process overhead
- ✅ Good for: File editors, code editors
- ❌ Bad for: Chat input, REPL input

See [TEXTUAL_VIM_ANALYSIS.md](TEXTUAL_VIM_ANALYSIS.md) for full analysis.

### Why Not Pure Refactor (Original Plan)?
- ⚠️ Similar effort (19-27 days vs 20-28 days)
- ⚠️ Would need to build output widgets, layouts, themes
- ⚠️ No community support
- ✅ Full control and flexibility
- ❌ More maintenance burden

Textual gives us: RichLog, CSS, layouts, themes, docs, community for similar effort.

### Why Not Keep Current textbox?
- ❌ 8 identified architectural bugs
- ❌ Tight coupling (model-view)
- ❌ Manual redraw spam (72 call sites)
- ❌ Hard to extend
- ❌ Technical debt accumulating

v2.0 is needed regardless of approach chosen.

---

## Next Steps

### Immediate (This Week)

**1. Review & Approve** (1-2 hours)
- [ ] Read README.md
- [ ] Review timeline
- [ ] Approve approach

**2. Set Up Environment** (30 minutes)
- [ ] Install Textual
  ```bash
  pip install textual textual-dev rich
  ```
- [ ] Verify installation
- [ ] Create project structure

**3. Start Spike** (2-3 days)
- [ ] Follow [SPIKE_GUIDE.md](SPIKE_GUIDE.md)
- [ ] Build minimal VimTextArea
- [ ] Test mode switching and navigation
- [ ] Make GO/NO-GO decision

### Short-term (Weeks 1-2)

**4. Phase 1: Basic Vim** (if spike succeeds)
- [ ] Implement core navigation
- [ ] Mode transitions
- [ ] Basic editing
- [ ] Unit tests

**5. Phase 2: Advanced Vim**
- [ ] Line operations
- [ ] Visual mode
- [ ] Advanced features
- [ ] Complete test suite

### Medium-term (Weeks 3-4)

**6. Phase 3: Chat App**
- [ ] Build chat interface
- [ ] Streaming support
- [ ] Command palette
- [ ] Themes

**7. Phase 4: Polish**
- [ ] Documentation
- [ ] Examples
- [ ] Package for release

---

## Questions?

### "Is 20-28 days realistic?"
Yes. Breakdown:
- Spike: 2-3 days (validate)
- Basic Vim: 5-7 days (MVP)
- Advanced Vim: 5-7 days (feature complete)
- Chat App: 5-7 days (production app)
- Polish: 3-4 days (release ready)

Can ship MVP (Phase 1+3) in ~10-14 days if needed.

### "What if spike fails?"
Fallback options:
1. Build custom widget from scratch (+2-3 weeks)
2. Use different approach (textual-vim + adapter)
3. Abandon vim, use standard TextArea
4. Return to original plan (Rich + custom MVC)

Spike validates early (2-3 days) before major commitment.

### "Why Textual over pure refactor?"
Similar effort, but Textual gives:
- RichLog widget (perfect for streaming)
- CSS theming (powerful)
- Layouts (Grid, Split)
- Widget library
- Documentation
- Community
- Maintained framework

vs. building all of this ourselves.

### "What about compatibility with v1.x?"
v2.0 is breaking change (new architecture).
Plan:
- v2.0: New Textual-based API
- v1.x: Keep in separate branch
- v2.1: Add compatibility layer (optional)

Users can stay on v1.x or migrate to v2.0.

---

## Resources

### Textual
- Main docs: https://textual.textualize.io/
- Tutorial: https://textual.textualize.io/tutorial/
- Widgets: https://textual.textualize.io/widgets/
- CSS: https://textual.textualize.io/guide/CSS/
- Discord: https://discord.gg/Enf6Z3qhVr

### Development
- Hot reload: `textual run --dev app.py`
- Debug console: `textual console`
- Testing: https://textual.textualize.io/guide/testing/

### Examples
- Official: https://github.com/Textualize/textual/tree/main/examples
- Showcase: https://github.com/Textualize/awesome-textual

---

## Document Status

| Document | Size | Status | Purpose |
|----------|------|--------|---------|
| INDEX.md | This file | ✅ Complete | Navigation hub |
| README.md | 15KB | ✅ Complete | Overview |
| SPIKE_GUIDE.md | 18KB | ✅ Complete | 2-3 day validation |
| VIM_TEXTAREA.md | 22KB | ✅ Complete | Widget implementation |
| CHAT_APP.md | 25KB | ✅ Complete | Application patterns |
| IMPLEMENTATION.md | 20KB | ✅ Complete | Detailed timeline |
| TEXTUAL_VIM_ANALYSIS.md | 12KB | ✅ Complete | Library analysis |

**Total**: ~112KB of comprehensive planning

---

## Plan Version

- **v1**: Initial exploration (archived)
- **v2**: Rich + custom MVC (discarded)
- **v3**: Textual + VimTextArea ← **Current plan**

---

**Ready to start?** → Begin with [SPIKE_GUIDE.md](SPIKE_GUIDE.md)

**Questions?** → Read [README.md](README.md) for overview

**Technical details?** → See [VIM_TEXTAREA.md](VIM_TEXTAREA.md)

**Implementation?** → Follow [IMPLEMENTATION.md](IMPLEMENTATION.md)
