"""Stable public exception types for Omni clients."""

from __future__ import annotations


class OmniError(Exception):
    """Base class for recoverable Omni failures."""


class ValidationError(OmniError):
    """Raised when a source or semantic model is invalid."""


class LoweringError(OmniError):
    """Raised when semantic lowering cannot preserve required meaning."""


class BackendError(OmniError):
    """Raised when a target backend cannot produce a requested artifact."""


class CapabilityError(OmniError):
    """Raised when requested capabilities cannot be satisfied."""
