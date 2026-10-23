"""Validate every tracked SKILL.md without interpreting filenames as shell code."""
from pathlib import Path
import re
import subprocess
import sys


def validate(text, directory):
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return "missing opening frontmatter delimiter"
    try:
        end = lines.index("---", 1)
    except ValueError:
        return "missing closing frontmatter delimiter"
    header = "\n".join(lines[1:end])
    name = re.search(r"(?m)^name:\s*([^\n]+)$", header)
    description = re.search(r"(?m)^description:\s*(.*)$", header)
    if not name or not description:
        return "name and description are required"
    name = name.group(1).strip().strip("\"'")
    if name != directory or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name)>64:
        return "name must match its directory and naming rules"
    value = description.group(1).strip()
    if not value:
        return "description must not be empty"
    return None


def main():
    names = subprocess.check_output(["git", "ls-files", "-z"], text=False).split(b"\0")
    failures = []
    count = 0
    for raw in names:
        if not raw:
            continue
        path = Path(raw.decode("utf-8", errors="strict"))
        if path.name != "SKILL.md":
            continue
        if path.is_symlink():
            failures.append((str(path), "symlink refused"))
            continue
        count += 1
        error = validate(path.read_text(encoding="utf-8"), path.parent.name)
        if error:
            failures.append((str(path), error))
    for path, error in failures:
        print(repr(path), error)
    print(f"Validated {count} skill files; {len(failures)} failures")
    return bool(failures)


if __name__ == "__main__":
    sys.exit(main())
