#!/usr/bin/env python3
"""Validate all 20 SKILL.md files for description budgets, YAML field order,
duplicate triggers, YAML validity, and language coverage.

Uses Python 3 standard library only (plus optional PyYAML).
Exit code: 0 if all checks pass, 1 otherwise.
"""

import os
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

# ---------------------------------------------------------------------------
# YAML parsing — prefer PyYAML if available, fall back to a minimal parser
# ---------------------------------------------------------------------------

try:
    import yaml  # type: ignore

    def parse_yaml(text: str) -> dict:
        return yaml.safe_load(text) or {}

except ImportError:
    import warnings
    warnings.warn(
        "PyYAML not installed — using minimal fallback parser that does NOT "
        "support nested mappings. Run `pip install pyyaml` for accurate results.",
        stacklevel=2,
    )

    def parse_yaml(text: str) -> dict:
        """Minimal YAML-subset parser for flat key: value and lists."""
        result: dict = {}
        current_key: str | None = None
        current_list: list | None = None
        indent_stack: list[tuple[str, dict | list]] = []

        for line in text.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            indent = len(line) - len(line.lstrip())

            # List item
            m_list = re.match(r"^(\s*)-\s+(.*)", line)
            if m_list:
                val = m_list.group(2).strip().strip("'\"")
                if current_list is not None:
                    current_list.append(val)
                continue

            # Key: value
            m_kv = re.match(r"^(\s*)([\w-]+)\s*:\s*(.*)", line)
            if m_kv:
                key = m_kv.group(2)
                val = m_kv.group(3).strip().strip("'\"")

                # Close any open list
                current_list = None

                if val:
                    result[key] = val
                else:
                    # Could be a nested mapping or upcoming list
                    current_key = key
                    current_list_candidate: list = []
                    result[key] = current_list_candidate
                    current_list = current_list_candidate

        return result


# ---------------------------------------------------------------------------
# Language detection heuristics
# ---------------------------------------------------------------------------

LANG_PATTERNS: dict[str, re.Pattern] = {
    "EN": re.compile(r"[A-Za-z]{3,}"),
    "ZH": re.compile(r"[\u4e00-\u9fff]"),
    "JA": re.compile(r"[\u3040-\u309f\u30a0-\u30ff]"),
    "KO": re.compile(r"[\uac00-\ud7af\u1100-\u11ff]"),
    "ES": re.compile(
        r"(?:investigaci[oó]n|palabras|clave|contenido|optimizaci[oó]n|"
        r"auditor[ií]a|autoridad|dominio|enlaces|rendimiento|alertas|"
        r"an[aá]lisis|competencia|b[uú]squeda|seguimiento|retroenlaces|"
        r"esquema|meta|etiquetas|calidad|entidad|memoria|rastreo|"
        r"t[eé]cnico|interno|actualizaci[oó]n)",
        re.IGNORECASE,
    ),
}


def detect_languages(text: str) -> list[str]:
    """Return sorted list of language codes found in *text*."""
    found = []
    for lang, pattern in LANG_PATTERNS.items():
        if pattern.search(text):
            found.append(lang)
    return sorted(found)


# ---------------------------------------------------------------------------
# Frontmatter extraction
# ---------------------------------------------------------------------------

def extract_frontmatter(content: str) -> tuple[str, bool]:
    """Return raw YAML frontmatter string and whether it parsed validly."""
    m = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not m:
        return "", False
    return m.group(1), True


def field_positions(yaml_text: str) -> dict[str, int]:
    """Return {field_name: first_line_number} for top-level YAML keys."""
    positions: dict[str, int] = {}
    for i, line in enumerate(yaml_text.splitlines()):
        m = re.match(r"^([\w-]+)\s*:", line)
        if m:
            key = m.group(1)
            if key not in positions:
                positions[key] = i
    return positions


# ---------------------------------------------------------------------------
# Core checks
# ---------------------------------------------------------------------------

class SkillResult:
    def __init__(self, path: str):
        self.path = path
        self.skill_name = ""
        self.description = ""
        self.desc_len = 0
        self.desc_budget_ok = True          # Budget A: <= 250 chars
        self.visible_pct = 0.0              # Budget B
        self.field_order_ok = True           # name < description < version
        self.duplicate_triggers: list[str] = []
        self.yaml_valid = True
        self.languages: list[str] = []
        self.errors: list[str] = []

    @property
    def passed(self) -> bool:
        return (
            self.yaml_valid
            and self.desc_budget_ok
            and self.field_order_ok
            and not self.duplicate_triggers
        )


def validate_skill(filepath: str) -> SkillResult:
    result = SkillResult(filepath)
    content = Path(filepath).read_text(encoding="utf-8")

    # --- YAML validity -------------------------------------------------
    yaml_raw, has_frontmatter = extract_frontmatter(content)
    if not has_frontmatter:
        result.yaml_valid = False
        result.errors.append("No YAML frontmatter found")
        return result

    try:
        data = parse_yaml(yaml_raw)
    except Exception as exc:
        result.yaml_valid = False
        result.errors.append(f"YAML parse error: {exc}")
        return result

    # --- Basic fields --------------------------------------------------
    result.skill_name = str(data.get("name", "<missing>"))
    result.description = str(data.get("description", ""))
    result.desc_len = len(result.description)

    # Budget A: description <= 250 chars
    if result.desc_len > 250:
        result.desc_budget_ok = False
        result.errors.append(
            f"Description length {result.desc_len} exceeds 250-char budget"
        )

    # Budget B: visibility in first 250 characters of the file
    first_250 = content[:250]
    if result.description:
        # How much of the description appears in those first 250 bytes?
        desc_in_preview = ""
        idx = first_250.find(result.description[:20])
        if idx >= 0:
            remaining = first_250[idx:]
            # Count how many description chars fit
            for i, ch in enumerate(result.description):
                if i < len(remaining) and remaining[i] == ch:
                    desc_in_preview += ch
                else:
                    break
            result.visible_pct = (
                len(desc_in_preview) / len(result.description) * 100
                if result.description
                else 0.0
            )
        else:
            result.visible_pct = 0.0
    else:
        result.visible_pct = 0.0

    # --- Field order: name < description < version ----------------------
    positions = field_positions(yaml_raw)
    name_pos = positions.get("name", -1)
    desc_pos = positions.get("description", -1)
    ver_pos = positions.get("version", -1)

    if name_pos == -1 or desc_pos == -1 or ver_pos == -1:
        result.field_order_ok = False
        missing = [
            f for f in ("name", "description", "version")
            if positions.get(f, -1) == -1
        ]
        result.errors.append(f"Missing required fields: {', '.join(missing)}")
    elif not (name_pos < desc_pos < ver_pos):
        result.field_order_ok = False
        result.errors.append(
            f"Field order violation: name@{name_pos}, "
            f"description@{desc_pos}, version@{ver_pos} "
            f"(expected name < description < version)"
        )

    # --- Duplicate triggers within this skill ---------------------------
    triggers: list[str] = []
    metadata = data.get("metadata", {})
    if isinstance(metadata, dict):
        trigs = metadata.get("triggers", [])
        if isinstance(trigs, list):
            triggers = [str(t).strip().lower() for t in trigs]
    else:
        # Fallback: scan YAML for trigger list items
        in_triggers = False
        for line in yaml_raw.splitlines():
            if re.match(r"\s+triggers\s*:", line):
                in_triggers = True
                continue
            if in_triggers:
                m = re.match(r"\s+-\s+['\"]?(.*?)['\"]?\s*$", line)
                if m:
                    triggers.append(m.group(1).strip().lower())
                elif re.match(r"\s+\w", line) and not line.strip().startswith("#"):
                    in_triggers = False

    seen: dict[str, int] = {}
    dupes: list[str] = []
    for t in triggers:
        if t in seen:
            dupes.append(t)
        seen[t] = seen.get(t, 0) + 1
    if dupes:
        result.duplicate_triggers = list(set(dupes))
        result.errors.append(
            f"Duplicate triggers: {', '.join(set(dupes))}"
        )

    # --- Language detection in description ------------------------------
    result.languages = detect_languages(result.description)

    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def find_skill_files(root: str) -> list[str]:
    """Recursively find all SKILL.md files."""
    found = []
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn == "SKILL.md":
                found.append(os.path.join(dirpath, fn))
    found.sort()
    return found


def main() -> int:
    # Determine repo root: script lives in scripts/
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent

    skill_files = find_skill_files(str(repo_root))
    if not skill_files:
        print("ERROR: No SKILL.md files found", file=sys.stderr)
        return 1

    results: list[SkillResult] = []
    for sf in skill_files:
        results.append(validate_skill(sf))

    # ---- Summary table ------------------------------------------------
    any_fail = False

    # Column widths
    name_w = max(len(r.skill_name) for r in results)
    name_w = max(name_w, 4)  # "Name" header

    header = (
        f"{'Name':<{name_w}}  "
        f"{'Chars':>5}  "
        f"{'Budget':>6}  "
        f"{'Vis%':>5}  "
        f"{'Order':>5}  "
        f"{'Dupes':>5}  "
        f"{'YAML':>4}  "
        f"{'Langs':<14}  "
        f"{'Status':<6}"
    )
    sep = "-" * len(header)

    print()
    print("SKILL.md Validation Report")
    print("=" * 26)
    print()
    print(header)
    print(sep)

    for r in results:
        status = "PASS" if r.passed else "FAIL"
        if not r.passed:
            any_fail = True

        langs_str = ",".join(r.languages) if r.languages else "-"

        print(
            f"{r.skill_name:<{name_w}}  "
            f"{r.desc_len:>5}  "
            f"{'OK' if r.desc_budget_ok else 'OVER':>6}  "
            f"{r.visible_pct:>4.0f}%  "
            f"{'OK' if r.field_order_ok else 'BAD':>5}  "
            f"{len(r.duplicate_triggers):>5}  "
            f"{'OK' if r.yaml_valid else 'ERR':>4}  "
            f"{langs_str:<14}  "
            f"{status:<6}"
        )

    print(sep)
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    failed = total - passed
    print(f"\nTotal: {total}  Passed: {passed}  Failed: {failed}")

    # ---- Error details ------------------------------------------------
    errors_exist = any(r.errors for r in results)
    if errors_exist:
        print("\n--- Errors ---")
        for r in results:
            if r.errors:
                rel = os.path.relpath(r.path, repo_root)
                for e in r.errors:
                    print(f"  {rel}: {e}")

    print()
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
