#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = [
    "00-linux-lab",
    "01-computer-foundations",
    "02-c-machine-model",
    "03-x86-64-assembly",
    "04-abi-syscalls",
    "05-computer-architecture",
    "06-elf",
    "07-linker-loader",
    "08-debugging",
    "09-compiler-frontend",
    "10-compiler-ir",
    "11-compiler-backend",
    "12-my-compiler",
    "13-os-foundations",
    "14-my-os",
    "15-advanced-os",
    "16-reverse-engineering",
    "17-security-lab",
    "18-capstone",
]

REQUIRED = [
    "README.md",
    "THEORY.md",
    "LABS.md",
    "EXERCISES.md",
    "MASTERY_TEST.md",
    "ANSWERS.md",
    "LEARNER_GUIDE.md",
    "WORKED_EXAMPLES.md",
    "RUBRIC.md",
]

ROOT_REQUIRED = [
    "README.md",
    "COURSE_MAP.md",
    "STUDY_GUIDE.md",
    "LANGUAGE_SPEC.md",
    "CI.md",
    "COURSE_AUTHORING_STANDARD.md",
    "ASSESSMENT_POLICY.md",
]

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+\.md(?:#[^)]+)?)\)")

def fail(message: str, errors: list[str]) -> None:
    errors.append(message)
    print(f"[FAIL] {message}")

def check_local_markdown_links(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for raw in LINK_RE.findall(text):
        target = raw.split("#", 1)[0]
        if "://" in target or target.startswith("/"):
            continue
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            fail(f"{path.relative_to(ROOT)} link escapes repository: {target}", errors)
            continue
        if not resolved.exists():
            fail(f"{path.relative_to(ROOT)} broken markdown link: {target}", errors)

def main() -> int:
    errors: list[str] = []

    for root_file in ROOT_REQUIRED:
        path = ROOT / root_file
        if not path.is_file() or path.stat().st_size < 100:
            fail(f"missing/thin root quality file: {root_file}", errors)

    for chapter in CHAPTERS:
        chapter_dir = ROOT / chapter
        if not chapter_dir.is_dir():
            fail(f"missing chapter directory: {chapter}", errors)
            continue

        for name in REQUIRED:
            path = chapter_dir / name
            if not path.is_file():
                fail(f"{chapter}: missing {name}", errors)
                continue
            if path.stat().st_size < 250:
                fail(f"{chapter}: {name} is too thin ({path.stat().st_size} bytes)", errors)

        readme = (chapter_dir / "README.md").read_text(encoding="utf-8")
        exercises = (chapter_dir / "EXERCISES.md").read_text(encoding="utf-8")
        mastery = (chapter_dir / "MASTERY_TEST.md").read_text(encoding="utf-8")
        worked = (chapter_dir / "WORKED_EXAMPLES.md").read_text(encoding="utf-8")
        rubric = (chapter_dir / "RUBRIC.md").read_text(encoding="utf-8")

        if "Self-study quality path" not in readme:
            fail(f"{chapter}: README does not expose self-study path", errors)

        for marker in ("Explain", "Concrete example", "Evidence", "misconception"):
            if marker.lower() not in exercises.lower():
                fail(f"{chapter}: EXERCISES missing response contract marker {marker!r}", errors)

        if "Scoring — 100 points" not in mastery:
            fail(f"{chapter}: mastery has no explicit 100-point scoring", errors)

        if worked.count("## Example ") < 3:
            fail(f"{chapter}: fewer than 3 worked examples", errors)
        if worked.count("Expected key evidence") < 3:
            fail(f"{chapter}: worked examples lack expected evidence", errors)

        if "100" not in rubric or "Implementation" not in rubric:
            fail(f"{chapter}: rubric does not contain practical 100-point model", errors)

        for name in REQUIRED:
            path = chapter_dir / name
            if path.is_file():
                check_local_markdown_links(path, errors)

    capstone_required = [
        "ASSIGNMENT.md",
        "starter/README.md",
        "starter/compiler/design.md",
        "starter/os/design.md",
        "starter/re/report.md",
        "starter/security/report.md",
    ]
    for rel in capstone_required:
        path = ROOT / "18-capstone" / rel
        if not path.is_file() or path.stat().st_size == 0:
            fail(f"18-capstone: missing learner-created deliverable scaffold {rel}", errors)

    spec = (ROOT / "LANGUAGE_SPEC.md").read_text(encoding="utf-8")
    for marker in ("signed 64-bit", "truncates toward zero", "fn main() -> int"):
        if marker not in spec:
            fail(f"LANGUAGE_SPEC missing semantic contract: {marker}", errors)

    if errors:
        print(f"[FAIL] course quality checks: {len(errors)} problem(s)")
        return 1

    print(
        "[OK] course quality structure: 19 chapters have learner guides, "
        "worked evidence, exercise contracts and 100-point rubrics"
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
