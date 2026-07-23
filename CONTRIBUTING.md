# Contributing

Thanks for considering a contribution. This project is intentionally small,
standard-library based, and focused on reliable Philips SICP command behavior.

## Good Contributions

- Bug fixes with a reproducible packet, command, or CLI example.
- New command support backed by vendor documentation, observed packet logs, or
  tests.
- README and command documentation improvements.
- Tests that cover packet construction, response parsing, or CLI validation.

## Development Setup

Use Python 3.10 or newer. With `uv`:

```bash
uv sync
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run python -m unittest discover -v
uv run sicp --help
```

Without `uv`:

```bash
python3 -m unittest discover -v
python3 -m py_compile sicp.py philips_sicp/*.py tests/*.py
```

## Code Style

- Keep runtime dependencies at zero unless there is a clear maintenance win.
- Prefer explicit command/value mappings over clever abstractions.
- Keep protocol parsing strict and error messages actionable.
- Keep `ruff` and `mypy` clean. The package code is checked with strict mypy.
- Add tests for packet bytes, report parsing, and CLI argument behavior when a
  command changes.
- Do not include secrets, private hostnames, or display credentials in logs,
  tests, or issues.

## Pull Requests

Before opening a pull request:

1. Run the full test suite.
2. Update README or docs when command behavior changes.
3. Include the display model and firmware version if the change depends on
   hardware behavior.
4. Call out commands that are destructive, operationally risky, or known to be
   platform-specific.
