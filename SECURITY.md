# Security Policy

## Supported Versions

Security fixes are handled on the default branch until versioned releases are
introduced.

## Reporting a Vulnerability

After the GitHub repository is published, please report security issues through
GitHub private vulnerability reporting if it is enabled. If it is not enabled,
open a minimal public issue asking for a private contact path and do not include
exploit details.

Please include:

- Affected command or module.
- Steps to reproduce.
- Impact and expected behavior.
- Whether real display hardware is required.

## Operational Safety

This tool can send commands that change display state, restart a display, or
factory reset a display. Treat hostnames, IP addresses, packet logs, and
configuration files as potentially sensitive when they identify private
networks or production hardware.

## Scope

In scope:

- Bugs in packet parsing or CLI handling that could cause unintended commands.
- Unsafe handling of configuration files or command arguments.
- Issues that expose sensitive local data.

Out of scope:

- Security of Philips, TPV, or PPDS display firmware.
- Physical access risks on display hardware.
- Network exposure caused by deploying displays on untrusted networks.
