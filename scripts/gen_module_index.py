#!/usr/bin/env python3
"""Module index generator and verification tool for Cofunder.

Scans packages/ and apps/ directories for README.md files and synchronizes
or validates the manifest of files and public symbols between
<!-- BEGIN GENERATED --> and <!-- END GENERATED --> markers.
"""

from __future__ import annotations

import argparse
import ast
import sys
from collections.abc import Sequence
from pathlib import Path

BEGIN_MARKER = "<!-- BEGIN GENERATED -->"
END_MARKER = "<!-- END GENERATED -->"


def extract_public_symbols(file_path: Path) -> list[tuple[str, str]]:
    """Extract public functions and classes with their docstring summary.

    Args:
        file_path: Absolute path to the python file.

    Returns:
        List of tuples containing (symbol_name, docstring_summary).
    """
    symbols: list[tuple[str, str]] = []
    try:
        content = file_path.read_text(encoding="utf-8")
        tree = ast.parse(content, filename=str(file_path))
    except Exception:
        return symbols

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and not node.name.startswith("_"):
            docstring = ast.get_docstring(node) or "No docstring provided."
            first_line = docstring.strip().splitlines()[0] if docstring else ""
            symbols.append((node.name, first_line))
    return symbols


def generate_index_content(module_dir: Path) -> str:
    """Generate index markdown content for a given module directory.

    Args:
        module_dir: Path to the package/app directory containing README.md.

    Returns:
        Formatted markdown string for the generated index.
    """
    lines: list[str] = [BEGIN_MARKER, "\n### Files & Manifest\n"]

    py_files = sorted(
        [
            p
            for p in module_dir.rglob("*.py")
            if not any(part.startswith((".", "__pycache__", "tests")) for part in p.parts)
        ]
    )

    if not py_files:
        lines.append("- *No python files found in module.*\n")
    else:
        for py_file in py_files:
            rel_path = py_file.relative_to(module_dir)
            symbols = extract_public_symbols(py_file)
            symbol_desc = f" ({len(symbols)} public symbols)" if symbols else ""
            lines.append(f"- `{rel_path}`{symbol_desc}")
            for name, doc in symbols:
                lines.append(f"  - `{name}`: {doc}")

    lines.append(f"\n{END_MARKER}")
    return "\n".join(lines)


def process_readme(readme_path: Path, check_mode: bool) -> bool:
    """Process a single README.md file, verifying or updating generated index.

    Args:
        readme_path: Path to the README.md file.
        check_mode: If True, only checks without modifying.

    Returns:
        True if valid/updated successfully, False if out of sync in check mode.
    """
    content = readme_path.read_text(encoding="utf-8")
    if BEGIN_MARKER not in content or END_MARKER not in content:
        # If markers are missing, append them
        if check_mode:
            print(f"Error: {readme_path} is missing generation markers.", file=sys.stderr)
            return False
        content += f"\n\n## Module Index\n{BEGIN_MARKER}\n{END_MARKER}\n"

    prefix = content.split(BEGIN_MARKER)[0]
    suffix = content.split(END_MARKER)[1]

    new_block = generate_index_content(readme_path.parent)
    expected_content = f"{prefix}{new_block}{suffix}"

    if content != expected_content:
        if check_mode:
            print(f"Error: {readme_path} is out of sync. Run scripts/gen_module_index.py to fix.", file=sys.stderr)
            return False
        readme_path.write_text(expected_content, encoding="utf-8")
        print(f"Updated index in {readme_path}")
    return True


def main(argv: Sequence[str] | None = None) -> int:
    """Main execution entry point."""
    parser = argparse.ArgumentParser(description="Generate and verify module README indexes.")
    parser.add_argument("--check", action="store_true", help="Check if indexes are up to date.")
    args = parser.parse_args(argv)

    root_dir = Path(__file__).resolve().parent.parent
    readme_files: list[Path] = []

    for search_dir in [root_dir / "packages", root_dir / "apps"]:
        if search_dir.exists():
            for p in search_dir.glob("**/README.md"):
                if not any(part in ("node_modules", ".next", ".venv", "__pycache__") for part in p.parts):
                    readme_files.append(p)

    all_valid = True
    for readme in readme_files:
        if not process_readme(readme, check_mode=args.check):
            all_valid = False

    return 0 if all_valid else 1


if __name__ == "__main__":
    sys.exit(main())
