"""Compatibility shim for running the backend in-place.

This file maps common `app.*` imports to `app.backend.*` modules so the
existing code (which uses `from app.database import ...`) works without
moving files.

This is intentionally minimal and tolerant: it attempts to import the
corresponding `app.backend.*` module and registers it in sys.modules under
the `app.*` name.
"""
from __future__ import annotations

import importlib
import sys
from typing import Iterable

_BACKEND_PREFIX = "app.backend."

def _map_modules(names: Iterable[str]) -> None:
    for name in names:
        full_backend = _BACKEND_PREFIX + name
        target_name = "app." + name
        try:
            mod = importlib.import_module(full_backend)
            # register the backend module under the app.* name
            sys.modules[target_name] = mod
        except Exception:
            # if mapping fails, leave it to regular import errors later
            # (don't crash on import of this shim)
            pass


_map_modules(["database", "config", "routers", "models", "schemas", "services"])
