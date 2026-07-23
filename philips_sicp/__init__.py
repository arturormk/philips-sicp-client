"""Small Philips SICP client package."""

__version__ = "0.1.0"

from .client import InputSourceState, SicpClient
from .protocol import SicpPacket, build_packet, parse_packet, xor_checksum

__all__ = [
    "InputSourceState",
    "SicpClient",
    "SicpPacket",
    "__version__",
    "build_packet",
    "parse_packet",
    "xor_checksum",
]
