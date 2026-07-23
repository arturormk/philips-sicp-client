# Changelog

All notable changes to this project will be documented in this file.

This project follows a simple changelog format. Version numbers are expected to
align with `pyproject.toml` once releases begin.

## [Unreleased]

## [0.1.0] - 2026-07-23

First public alpha release.

### Added

- Initial dependency-free Philips SICP Python client and CLI.
- TCP packet construction, checksum handling, response parsing, ACK/NACK/NAV
  handling, typed command helpers, configuration collect/apply helpers, and raw
  DATA[] probing.
- `uv`-friendly packaging with a `sicp` console script.
- Standard project documents for licensing, contribution guidance, security,
  conduct, and notices.
