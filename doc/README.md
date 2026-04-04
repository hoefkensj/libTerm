# libTerm

Lightweight Python library for direct terminal control on POSIX systems (Linux/macOS). Works with raw ANSI escape codes, terminal modes, cursor positioning, input handling, and color management — without heavy abstractions.

## Quick Start

```bash
git clone https://github.com/hoefkensj/libTerm
cd libTerm
python -m venv .venv && source .venv/bin/activate
pip install -e .
python -m libTerm.examples.ex_arrowkeys
```

Or install directly into your project:
```bash
pip install libTerm
```

## What is libTerm?

A direct interface to terminal I/O and ANSI control codes. Useful for:

- **Terminal games** (snake, roguelikes, real-time animations)
- **Interactive CLI tools** with custom key handling
- **Live dashboards** that update without clearing the screen
- **Learning ANSI sequences** and POSIX terminal control

## Features

- **Terminal modes**: Switch between NORMAL (echo, canonical) and CONTROL (raw input, no echo, cursor hidden)
- **Cursor control**: Position, move, show/hide, save/restore positions on a stack
- **Raw keyboard input**: Non-blocking event polling, read all available input at once
- **Color detection**: Query current foreground/background colors from terminal
- **Terminal size**: Track terminal width and height, detect resize events
- **Direct ANSI access**: Use raw escape codes alongside the API

## Basic Usage

```python
from libTerm import Term, Mode, Coord

term = Term()

# Query terminal state
print(f"Size: {term.size.xy}")          # (width, height)
print(f"Cursor at: {term.cursor.xy}")   # (x, y)
print(f"BG color: {term.color.bg}")     # Current background color
```

## Terminal Modes

Switch between normal line-editing and raw control input:

```python
from libTerm import Term, Mode

term = Term()

# Enter raw input mode (no echo, no line buffering, cursor hidden)
term.mode = Mode.CONTROL

# Poll for keyboard events without blocking
if term.stdin.event:
    key = term.stdin.read()
    if key == 'q':
        break

# Restore normal mode (echo on, canonical input, cursor visible)
term.mode = Mode.NORMAL
```

## Keyboard Input (Non-Blocking)

Read raw input one event at a time:

```python
# Check if input is available (non-blocking)
if term.stdin.event:
    key_bytes = term.stdin.read()
    
    # Arrow keys come as ANSI sequences
    if key_bytes == '\x1b[A':  # Up
        print("UP")
    elif key_bytes == '\x1b[B':  # Down
        print("DOWN")
    elif key_bytes == '\x1b[C':  # Right
        print("RIGHT")
    elif key_bytes == '\x1b[D':  # Left
        print("LEFT")
```

vs. using `input()`:
- `input()` blocks and echoes, waits for Enter
- `term.stdin.event + term.stdin.read()` is non-blocking, captures individual bytes, allows arrow keys and Ctrl sequences

## Cursor Control

Position the cursor, move it, or hide it:

```python
from libTerm import Coord

# Set cursor position (1-indexed)
term.cursor.xy = Coord(10, 5)
print("*")

# Move relative to current position
term.cursor.move.down(3)
term.cursor.move.right(5)
print("*")

# Show / hide cursor
term.cursor.hide()
term.cursor.show()
```

vs. raw ANSI:
```python
# Without libTerm (raw ANSI):
print("\x1b[5;10H*")  # Move to (10, 5), print *
print("\x1b[3B\x1b[5C*")  # Move down 3, right 5, print *
print("\x1b[?25l")  # Hide cursor
print("\x1b[?25h")  # Show cursor
```

libTerm makes this discoverable and less error-prone.

## Cursor Position Stack

Save and restore cursor positions easily:

```python
term.cursor.store.save()   # Push current position
print("Hello at position 1")

term.cursor.xy = Coord(1, 10)
print("Hello at position 2")

term.cursor.store.undo()   # Pop back to saved position
print("Back to position 1")
```

## Coordinates (`Coord`)

Immutable coordinate type:

```python
c = Coord(5, 10)
print(c.x, c.y)           # 5, 10
print(c[0], c[1])         # 5, 10 (indexing)
print(c + Coord(2, 3))    # Coord(7, 13)
```

## Terminal Size & Resize Detection

Query size and detect when terminal is resized:

```python
width, height = term.size.xy
print(f"{width} x {height}")

# Detect resize events
if term.size.changed:
    print("Terminal was resized!")
```

vs. `os.get_terminal_size()`:
- libTerm tracks resize events
- Provides a convenient object interface
- Integrates with the terminal state system

## Colors

Query the current foreground and background colors:

```python
fg = term.color.fg
bg = term.color.bg

# Color has R, G, B components (0-255 per channel)
print(f"Background: RGB({bg.R}, {bg.G}, {bg.B})")
```

## Direct ANSI Access

libTerm doesn't hide ANSI. Mix raw codes with the API:

```python
# Use Ansi enum for common sequences
from libTerm import Ansi

print(Ansi.hide)     # Hide cursor
print(Ansi.show)     # Show cursor
print("\x1b[31mRED text\x1b[m")  # Raw ANSI still works
```

## Why Use libTerm?

### vs. Curses / ncurses
- **libTerm**: Direct, close to ANSI, minimal setup, no system package dependency
- **Curses**: Heavier abstraction, window-based model, more complex for simple tasks

**Choose libTerm if** you want raw terminal access without heavy abstractions.

### vs. Manual ANSI Codes
- **Raw ANSI**: Error-prone escape sequences, hard to remember, no structure
- **libTerm**: Named enums, methods with clear intent, still lets you write raw ANSI

**Choose libTerm if** you want safety and discoverability alongside low-level control.

### vs. Rich / Textual
- **Rich/Textual**: High-level TUI framework, great for dashboards, lots of abstraction
- **libTerm**: Low-level, minimal, close to the terminal

**Choose libTerm if** you want to build your own abstractions or learn terminal internals.

## Examples

Located in `src/libTerm/examples/`:

| File                    | Shows                      |
| ----------------------- | -------------------------- |
| `ex_basic.py`           | Terminal state inspection  |
| `ex_arrowkeys.py`       | Raw arrow key polling      |
| `ex_snake_manual.py`    | Keyboard-controlled game  |
| `ex_snake_automatic.py` | Animation without input    |
| `ex_colors.py`          | Color detection            |
| `ex_buffers.py`         | Alternate screen buffer    |
| `ex_printkeys.py`       | Debug: see all key codes   |

Run an example:
```bash
python -m libTerm.examples.ex_arrowkeys
```

## Platform Support

- Linux: Full support
- macOS: Full support
- Windows: Partial (alternate implementations in progress)

## Philosophy

libTerm is intentionally low-level:

- Stay close to ANSI and POSIX
- Avoid heavy abstractions
- Let you control the terminal directly
- Make common tasks simple, complex tasks possible

If you need a full TUI framework, use Rich or Textual.
If you want control and simplicity, use libTerm.

## Contributing

Pull requests welcome. Report bugs and experimental ideas.

---

Happy terminal hacking!
