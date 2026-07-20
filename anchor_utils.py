from __future__ import annotations

import json
from typing import Optional


def extract_named_range_id(anchor: str) -> Optional[str]:
    """
    Extract a Docs named-range id from a Drive comment anchor value.

    Anchors may arrive as:
    - plain named-range id string (current write path)
    - JSON payload in Drive anchor format
    """
    if not anchor:
        return None

    trimmed = anchor.strip()
    if not trimmed:
        return None

    # Current write path uses the bare named-range id string.
    if not trimmed.startswith("{") and not trimmed.startswith("["):
        return trimmed

    try:
        parsed = json.loads(trimmed)
    except Exception:
        return None

    if isinstance(parsed, str):
        return parsed.strip() or None

    if isinstance(parsed, dict):
        for part in parsed.get("a", []):
            if part.get("t") == "r":
                return part.get("v")

    return None
