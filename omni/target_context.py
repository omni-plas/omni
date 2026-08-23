"""Explicit requested-target context for universal compilation."""
from __future__ import annotations

from dataclasses import replace
from typing import Any

from .targets import TargetDescriptor
from .uir import UIR


def apply_target_context(uir: UIR, target: TargetDescriptor) -> UIR:
    """Return UIR explicitly bound to the requested target.

    Frontends remain language-focused; target selection is a separate concern.
    This makes universal compilation deterministic and prevents a frontend from
    silently compiling for an unrelated target embedded in its own output.
    """
    if not isinstance(target, TargetDescriptor):
        raise TypeError("target must be a TargetDescriptor")
    target_doc = target.document()
    source = dict(uir.source)
    source["requested_target"] = target.identity()
    return replace(uir, target=target_doc, source=source)
