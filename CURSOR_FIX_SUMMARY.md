# Cursor Position Query Fix

## Problem

When creating a `Term()` instance, the cursor position was being printed to the terminal as visible escape sequences (e.g., `^[[41;1R`), even though echo was supposed to be disabled.

### Root Cause

The `Cursor.__init__()` method was performing an immediate DSR (Device Status Report) query to get the current cursor position:

```python
# In src/libTerm/components/cursor.py, line 25
s.init = s.__sync__()  # This called s.update() which queries cursor position
```

This query was happening during `Term()` initialization, **before** the terminal mode and echo settings were properly configured. Here's the initialization order in `posix.py`:

```python
s.tty = TermTty(term=s)           # TTY initialized (echo=ON by default)
s.attr = TermAttrs(term=s)        # Attributes initialized (echo still ON)
s.buffers = TermBuffers(term=s)
s.colors = TermColors(term=s)
s.cursor = Cursor(term=s)         # ← DSR query happens HERE (echo still ON!)
s.modes = TermModes(term=s)       # Only NOW would mode be set to control
```

When the DSR query (`\x1b[6n`) was sent with echo enabled, the terminal's response (e.g., `\x1b[43;1R` meaning "cursor at row 43, col 1") became visible on the terminal instead of being consumed silently.

## Solution

Removed the automatic cursor position query during initialization by:

1. **Removed** `s.init = s.__sync__()` from `Cursor.__init__()` (line 25)
2. **Changed** initial coordinates from `Coord(0,0)` to `Coord(1,1)` (standard 1-indexed terminal position)
3. **Made cursor position query lazy**: The cursor position is now queried only when first accessed via the `.xy` property getter, which happens after terminal mode is properly configured

### Changes Made

**File: `src/libTerm/components/cursor.py`**

```diff
def __init__(s, term):
    s.term         = term
    s.move         = Move
    s._re      = re.compile(r"^.?\x1b\[(?P<Y>\d*);(?P<X>\d*)R", re.VERBOSE)
-   s._xy     = Coord(0,0)
+   s._xy     = Coord(1,1)
-   s._xyset  = Coord(0,0)
+   s._xyset  = Coord(1,1)
    s._coordstore   = Store(s.term)
    s.visible = True
    s.hidden  = False
    s.mock    = False
    s.slaves  = []
    #TODO:  s.stamp=time_ns()
    #TODO:  s.moved=False
    #TODO:  s._history = [*(None,) * 64]ASDF
-   s.init    = s.__sync__()  # ← REMOVED: This was causing the DSR response to be visible
```

## Impact

- ✅ **Fixes**: No more visible cursor position escape sequences during `Term()` initialization
- ✅ **Maintains**: All cursor functionality still works (`.xy` property still queries position when accessed)
- ✅ **Improves**: Terminal startup is cleaner with no unwanted escape sequences visible
- ⚠️ **Note**: The `s.init` attribute was never used in the codebase, so removing it has no side effects

## Testing

Before fix:
```
$ python -m libTerm.examples.ex_echo
^[[41;1R^[[41;1R   ← <- DSR responses visible!
bls
^[[43;1R^[[43;1R   ← <- More DSR responses visible!
```

After fix:
```
$ python -m libTerm.examples.ex_echo
bls
$ ← ← Clean output, no DSR artifacts!
```

