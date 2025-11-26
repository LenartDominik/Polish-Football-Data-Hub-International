"""check_reqs.py - small utility to verify installed packages vs requirements files

Usage:
    python tools/check_reqs.py [requirements_file ...]

If no files are provided, the script checks `requirements.txt` and
`app/frontend/requirements.txt` if present.

Exit codes:
    0 - all requirements satisfied
    1 - missing requirements found

This script is conservative about parsing requirements: it strips extras
e.g. `uvicorn[standard] -> uvicorn`, handles `-r other.txt` includes,
ignores editable and URL installs, and ignores environment markers.
"""
from __future__ import annotations

import re
import sys
import os
from typing import Iterable, Set, List

try:
    # Python 3.8+
    import importlib.metadata as importlib_metadata
except Exception:
    try:
        import importlib_metadata  # type: ignore
    except Exception:
        importlib_metadata = None


def get_installed_packages() -> Set[str]:
    """Return a set of installed package names (lowercased)."""
    installed: Set[str] = set()
    if importlib_metadata is not None:
        for d in importlib_metadata.distributions():
            # Try common metadata fields
            name = None
            try:
                name = d.metadata.get('Name')
            except Exception:
                name = getattr(d, 'name', None)
            if not name:
                try:
                    name = d.name
                except Exception:
                    continue
            installed.add(name.lower())
    else:
        try:
            import pkg_resources  # type: ignore

            installed = {p.key for p in pkg_resources.working_set}
        except Exception:
            installed = set()
    return installed


REQ_LINE_RE = re.compile(r"^\s*(?:-r\s+)?(?P<pkg>[^#;\n]+)")


def parse_requirements_file(path: str, seen: Set[str] | None = None) -> List[str]:
    """Parse a requirements file and return a list of package names (no versions).

    This function handles `-r other.txt` includes (relative to the current file)
    and strips extras (e.g. package[extra1,extra2]) and environment markers.
    """
    seen = seen or set()
    path = os.path.abspath(path)
    if path in seen:
        return []
    seen.add(path)

    reqs: List[str] = []
    if not os.path.exists(path):
        return reqs

    with open(path, "r", encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            # include files
            if line.startswith('-r '):
                ref = line.split(None, 1)[1].strip()
                ref_path = os.path.join(os.path.dirname(path), ref)
                reqs.extend(parse_requirements_file(ref_path, seen=seen))
                continue
            # skip editable and VCS/URL installs
            if line.startswith('-e') or line.startswith('git+') or '://' in line:
                continue
            # remove environment markers (PEP 508) after ';'
            if ';' in line:
                line = line.split(';', 1)[0].strip()
            # strip version specifiers and extras
            name = re.split(r"[<=>@]", line, 1)[0].strip()
            # strip extras like package[extra1,extra2]
            name = re.sub(r"\[.*\]", "", name).strip()
            if name:
                reqs.append(name.lower())
    return reqs


def main(argv: Iterable[str] | None = None) -> int:
    argv = list(argv or sys.argv[1:])
    files: List[str]
    if argv:
        files = argv
    else:
        candidates = ["requirements.txt", os.path.join("app", "frontend", "requirements.txt")]
        files = [p for p in candidates if os.path.exists(p)]

    installed = get_installed_packages()

    total_required = 0
    total_missing = 0
    missing_summary = {}

    for f in files:
        reqs = parse_requirements_file(f)
        total_required += len(reqs)
        missing = [r for r in reqs if r not in installed]
        total_missing += len(missing)
        missing_summary[f] = missing
        print(f"{f}: required {len(reqs)}, missing {len(missing)}")
        if missing:
            print("  Missing: " + ", ".join(missing))

    if not files:
        print("No requirements files found. Provide filenames as arguments.")

    if total_missing:
        print(f"\nTotal required: {total_required}, total missing: {total_missing}")
        return 1

    print(f"\nAll requirements satisfied ({total_required} packages checked).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
