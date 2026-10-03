#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Iterable

ROOT = Path(__file__).resolve().parents[3]
CHAPTER = ROOT / "18-capstone"
BUILD = CHAPTER / "build"

ELITEC = ROOT / "12-my-compiler" / "projects" / "elitec" / "elitec.py"
BINARY_REPORT = ROOT / "16-reverse-engineering" / "projects" / "binary-report" / "binary_report.py"
CFG_EXTRACT = ROOT / "16-reverse-engineering" / "projects" / "cfg-extract" / "cfg_extract.py"
MULTIBOOT_CHECK = ROOT / "14-my-os" / "tests" / "check_multiboot.py"
SOURCE = CHAPTER / "examples" / "capstone.el"


class AuditError(RuntimeError):
    pass


def run(
    args: list[str],
    *,
    cwd: Path | None = None,
    output: Path | None = None,
    expect: int = 0,
) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(proc.stdout, encoding="utf-8")

    if proc.returncode != expect:
        command = " ".join(args)
        raise AuditError(
            f"command failed: {command}\n"
            f"expected={expect} actual={proc.returncode}\n"
            f"{proc.stdout}"
        )

    return proc


def version(command: list[str]) -> str:
    try:
        proc = subprocess.run(
            command,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        line = proc.stdout.splitlines()
        return line[0] if line else f"status={proc.returncode}"
    except OSError as exc:
        return f"unavailable: {exc}"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_manifest(paths: Iterable[Path]) -> dict[str, dict[str, object]]:
    manifest: dict[str, dict[str, object]] = {}
    for path in paths:
        rel = path.relative_to(CHAPTER)
        manifest[str(rel)] = {
            "sha256": sha256(path),
            "size": path.stat().st_size,
        }
    (BUILD / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    BUILD.mkdir(parents=True, exist_ok=True)

    cc = sys.argv[1] if len(sys.argv) > 1 else "gcc"
    py = sys.executable

    steps: list[dict[str, str]] = []

    def gate(name: str, args: list[str], *, cwd: Path | None = None, output: Path | None = None) -> None:
        run(args, cwd=cwd, output=output)
        steps.append({"name": name, "status": "passed"})

    # 1. Compiler: source -> IR -> assembly -> executable.
    gate(
        "elitec-check",
        [py, str(ELITEC), "--check", str(SOURCE)],
        output=BUILD / "elitec-check.txt",
    )
    gate(
        "elitec-ir",
        [py, str(ELITEC), "--opt", "--emit", "ir", str(SOURCE)],
        output=BUILD / "capstone.ir",
    )
    gate(
        "elitec-assembly",
        [py, str(ELITEC), "--opt", "--emit", "asm", str(SOURCE)],
        output=BUILD / "capstone.s",
    )
    gate(
        "elitec-link",
        [
            py,
            str(ELITEC),
            "--opt",
            "--cc",
            cc,
            str(SOURCE),
            "-o",
            str(BUILD / "capstone-app"),
        ],
        output=BUILD / "elitec-link.txt",
    )
    gate(
        "compiled-program",
        [str(BUILD / "capstone-app")],
        output=BUILD / "capstone-run.txt",
    )

    # 2. ELF / machine-level evidence.
    gate(
        "file",
        ["file", str(BUILD / "capstone-app")],
        output=BUILD / "capstone.file.txt",
    )
    gate(
        "readelf",
        ["readelf", "-hSWl", str(BUILD / "capstone-app")],
        output=BUILD / "capstone.elf.txt",
    )
    gate(
        "objdump",
        ["objdump", "-d", "-Mintel", str(BUILD / "capstone-app")],
        output=BUILD / "capstone.dis",
    )
    gate(
        "binary-report",
        [py, str(BINARY_REPORT), str(BUILD / "capstone-app")],
        output=BUILD / "binary-report.json",
    )
    gate(
        "cfg-extract",
        [py, str(CFG_EXTRACT), str(BUILD / "capstone-app")],
        output=BUILD / "cfg.txt",
    )

    # 3. Kernel artifact / boot contract.
    gate(
        "eliteos-kernel-test",
        ["make", "clean", "test"],
        cwd=ROOT / "14-my-os",
        output=BUILD / "eliteos-test.txt",
    )
    kernel = ROOT / "14-my-os" / "build" / "kernel.elf"
    kernel_copy = BUILD / "eliteos64-kernel.elf"
    shutil.copy2(kernel, kernel_copy)
    gate(
        "multiboot2-validation",
        [py, str(MULTIBOOT_CHECK), str(kernel_copy)],
        output=BUILD / "multiboot.txt",
    )

    # 4. Advanced OS algorithm gates.
    gate(
        "advanced-os",
        ["make", "clean", "test", f"CC={cc}"],
        cwd=ROOT / "15-advanced-os",
        output=BUILD / "advanced-os.txt",
    )

    # 5. Authorized RE suite + tooling.
    gate(
        "reverse-engineering-suite",
        ["make", "clean", "test", f"CC={cc}"],
        cwd=ROOT / "16-reverse-engineering",
        output=BUILD / "reverse-engineering.txt",
    )

    # 6. Defensive fixed-code regression/fuzz suite.
    gate(
        "security-regression-suite",
        ["make", "clean", "test", f"CC={cc}"],
        cwd=ROOT / "17-security-lab",
        output=BUILD / "security-lab.txt",
    )

    artifacts = [
        BUILD / "capstone-app",
        BUILD / "capstone.ir",
        BUILD / "capstone.s",
        BUILD / "capstone.elf.txt",
        BUILD / "capstone.dis",
        BUILD / "binary-report.json",
        BUILD / "cfg.txt",
        kernel_copy,
        BUILD / "multiboot.txt",
        BUILD / "advanced-os.txt",
        BUILD / "reverse-engineering.txt",
        BUILD / "security-lab.txt",
    ]
    manifest = write_manifest(artifacts)

    git_commit = version(["git", "-C", str(ROOT), "rev-parse", "HEAD"])
    summary = {
        "status": "passed",
        "scope": "course-owned artifacts and defensive tests only",
        "source": str(SOURCE.relative_to(ROOT)),
        "compiler_driver": cc,
        "environment": {
            "python": version([py, "--version"]),
            "compiler": version([cc, "--version"]),
            "ld": version(["ld", "--version"]),
            "readelf": version(["readelf", "--version"]),
            "objdump": version(["objdump", "--version"]),
            "git_commit": git_commit,
        },
        "steps": steps,
        "artifact_count": len(manifest),
        "limitations": [
            "The capstone build gate does not require QEMU/GRUB.",
            "Chapter 15 scheduler/COW/VFS/IPC projects are host-side algorithm simulators.",
            "EliteC remains an educational compiler with known optimization/allocation limitations.",
            "Security checks are defensive regression/fuzz checks on course-owned code, not a security proof.",
        ],
    }
    (BUILD / "audit-summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(
        f"[OK] final capstone audit: {len(steps)} gates, "
        f"{len(manifest)} hashed artifacts"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, AuditError, shutil.Error) as exc:
        print(f"[FAIL] capstone audit: {exc}", file=sys.stderr)
        raise SystemExit(1)
