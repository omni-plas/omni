"""Compatibility entry point for the canonical Omni source parser.

The compiler pipeline must consume the real Omni AST, not a second line-based
parser that leaves statements as strings.
"""
from __future__ import annotations

from .omni_source import parse as parse_source

parse = parse_source
