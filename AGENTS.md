# libTerm Agent Guidelines

## Architecture Overview
libTerm provides direct terminal control via ANSI escape codes. Core is the `Term` class, platform-specific (POSIX in `src/libTerm/term/posix.py`, Windows in `winnt.py`). `Term` aggregates components like `cursor`, `stdin`, `size` for state management. Higher-level modules in `src/libTerm/modules/` build on components (e.g., menus, displays). Data flows from `Term` to components, outputting ANSI to stdout/stdin.

## Key Patterns
- **Instantiation**: `term = Term()` auto-detects platform; components accessible as `term.cursor`, `term.stdin`.
- **Modes**: Switch with `term.mode = Mode.CONTROL` for raw input (no echo, non-blocking). Use `Mode.NORMAL` for standard.
- **Coordinates**: Immutable `Coord(x, y)` (1-indexed); e.g., `term.cursor.xy = Coord(10, 5)`.
- **Input**: Non-blocking via `if term.stdin.event: key = term.stdin.read()`.
- **Cursor Stack**: `term.cursor.store.save()` pushes position; `term.cursor.store.undo()` pops.
- **Branchless Logic**: Prefer expressions like `((cond) * val1) + ((not cond) * val2)` over if/else for compactness.

## Coding Conventions
- **Indentation**: Tabs for structure, spaces for alignment only.
- **Methods**: First parameter `s` (not `self`); no type hints.
- **Functions**: Exactly one `return` at end; early returns forbidden.
- **Assertions**: Place `assert` in code for critical checks, not just tests.
- **Imports**: Minimal; no external deps beyond stdlib (termios, os).

## Testing & Examples
- **Tests**: Use unittest in `tests/`; no mocking—test via real `Term()` (falls back to mock). Focus on aggregated behaviors.
- **Examples**: Run with `python -m libTerm.examples.ex_basic`; modify for experimentation.
- **Build/Install**: `pip install -e .` for dev; `python -m build` for dist.

## File References
- Core Term: `src/libTerm/term/posix.py`
- Components: `src/libTerm/components/base.py` (Coord, Store)
- Tests: `tests/test_store.py`
- Usage: `src/libTerm/examples/ex_basic.py`
