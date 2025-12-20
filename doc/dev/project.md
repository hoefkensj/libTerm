# libTerm — Developer Guide

This document helps new contributors understand the repository layout, naming conventions, development practices, and where to put new code or tests.

Location: `doc/dev/project.md`

Quick start
- Clone the repo and open it in your editor.
- Create a virtualenv and install the package in editable mode for development:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

(If you use Poetry or other tooling, follow `pyproject.toml` instructions.)

Project overview
- Package root: `src/libTerm/`
- Main runtime code: `src/libTerm/term/` — platform-specific terminal helpers (modules include `cursor.py`, `posix.py`, `winnt.py`, `types.py`).
- Example / quick-run script: `src/test.py` (convenience).
- Build artifacts: `build/` and `libTerm.egg-info/` (do not commit these).
- Developer docs: `doc/dev/` (this file).

Design goals
- Small, focused utilities that provide a stable, small public API for terminal operations.
- Keep platform-specific code isolated under `term/`.
- Keep public API surface minimal and well-documented.

Where to put things (short map)
- Source code: `src/libTerm/`
- Platform-specific modules: `src/libTerm/term/`
- Public package exports: `src/libTerm/__init__.py` and `src/libTerm/term/__init__.py`
- Tests: `tests/` (create at repo root)
- Docs: `doc/` for user docs, `doc/dev/` for developer docs
- Examples / small scripts: `examples/` or `src/` (small runner scripts)

Naming conventions
- Packages & modules: lowercase, underscores as needed (e.g. `term_utils.py`).
- Classes: PascalCase (e.g. `CursorPosition`).
- Functions, variables, methods: snake_case (e.g. `move_cursor`).
- Constants: UPPER_SNAKE_CASE (e.g. `ESC`).
- Test files: `tests/test_<module>.py` or `tests/<module>_test.py` (pick one and stay consistent).
- Public API: keep names stable; prefer adding new functions over changing or removing existing ones.

API surface & exports
- Only export what you intend to be public from `__init__.py` with explicit names, for example:

```text
# src/libTerm/term/__init__.py
from .cursor import Cursor
from .types import Position

__all__ = ["Cursor", "Position"]
```

This makes it clear which symbols are part of the public API.

Code style & tooling
- Add docstrings for public APIs (Google or NumPy style is acceptable).


Suggested commands

```bash
# format
black src/ tests/ doc/
# lint (example with ruff)
ruff src/ tests/
# type-check
mypy src/
# tests
pytest -q
```

Tests
- Use `pytest` for unit and integration tests.
- Add tests under `tests/` at repository root.
- Use `tests/conftest.py` for shared fixtures.
- Unit tests should mock or stub OS-specific behavior where practical (for `posix.py` / `winnt.py`).

Adding a new module or feature (recommended workflow)
1. Branch: `feature/<short-description>` or `fix/<short-desc>`.
2. Add implementation under `src/libTerm/` or `src/libTerm/term/` for term-specific implementations.
3. Export public API explicitly in `__init__.py` if it is part of the public surface.
4. Add unit tests in `tests/` that cover normal and edge cases.
5. Run formatter, linter, and tests locally.
6. Open a PR with a clear description, how to test, and link issues if relevant.

Example: add a `keyboard.py` term helper
- Create `src/libTerm/term/keyboard.py` with functions/classes.
- Add `from .keyboard import ...` to `src/libTerm/term/__init__.py` if you want to expose it publicly.
- Add tests in `tests/test_keyboard.py`.

Packaging & distribution
- Project metadata and build backend are in `pyproject.toml`.
- Build artifacts are created with `python -m build` (sdist/wheel).
- Use `pip install -e .` for editable installs during development.
- Do not commit `build/` or `*.egg-info/` directories.

Continuous Integration
- CI should at minimum run: install, format check, lint, type-check, and tests.
- Typical CI steps: checkout, setup Python, install dev dependencies, run `black --check`, `ruff`, `mypy`, and `pytest`.

Code review checklist
- Does the code follow naming & style rules?
- Is the public API documented and kept stable?
- Are tests added for new behavior and edge cases?
- Are platform-specific concerns isolated under `term/`?
- Are there no secrets or large binaries in the change?

Commit messages & branches
- Keep commits small and focused.
- Commit summary: 50 characters or less, optional body for details.
- Branch naming: `feature/`, `fix/`, or `chore/` prefixes.

Security & secrets
- Never commit secrets, credentials, or private keys.
- Use environment variables for secrets and provide `env.example` for placeholders.

Onboarding checklist (for a new contributor)
- Clone repo and create virtualenv.
- Install dev dependencies and the package in editable mode.
- Run `pytest` and ensure tests pass.
- Run formatter and linter and fix any issues.
- Read this file and any `CONTRIBUTING` or `CODE_OF_CONDUCT` files.

Maintenance notes & conventions specific to this repository
- Keep platform-specific code in `src/libTerm/term/` and prefer small shim functions in `src/libTerm/` that re-export behavior.
- Where behavior differs by OS, clearly document expected behavior in docstrings and tests.
- Avoid introducing runtime dependencies unless necessary for the feature.

Next steps (for maintainers)
- Consider adding a `CONTRIBUTING.md` with branch/PR templates and CI requirements.
- Add `requirements-dev.txt` or `extras_require` in `pyproject.toml` for development dependencies.
- Add `tests/` directory and a minimal test to CI to ensure tests run on PRs.

Thanks for contributing — please keep changes small and well-tested.
