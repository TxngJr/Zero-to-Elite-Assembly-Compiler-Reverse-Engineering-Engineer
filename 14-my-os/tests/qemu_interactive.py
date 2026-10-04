#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path
import selectors
import subprocess
import sys
import time


class BootFailure(RuntimeError):
    pass


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Boot EliteOS64 in QEMU and verify real serial shell I/O"
    )
    parser.add_argument("iso")
    parser.add_argument("log")
    parser.add_argument("--qemu", default="qemu-system-x86_64")
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args()

    iso = Path(args.iso).resolve()
    log = Path(args.log).resolve()
    log.parent.mkdir(parents=True, exist_ok=True)

    command = [
        args.qemu,
        "-accel", "tcg",
        "-m", "128M",
        "-cdrom", str(iso),
        "-serial", "stdio",
        "-display", "none",
        "-no-reboot",
        "-no-shutdown",
    ]

    proc = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=0,
    )

    if proc.stdin is None or proc.stdout is None:
        proc.kill()
        raise BootFailure("failed to open QEMU stdio pipes")

    selector = selectors.DefaultSelector()
    selector.register(proc.stdout, selectors.EVENT_READ)
    transcript = bytearray()

    def read_until(needle: bytes, *, start: int, deadline: float) -> None:
        while needle not in transcript[start:]:
            if proc.poll() is not None:
                raise BootFailure(
                    f"QEMU exited before {needle!r}; status={proc.returncode}"
                )

            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise BootFailure(f"timeout waiting for {needle!r}")

            events = selector.select(timeout=min(0.25, remaining))
            if not events:
                continue

            chunk = os.read(proc.stdout.fileno(), 4096)
            if not chunk:
                raise BootFailure(f"QEMU output closed before {needle!r}")
            transcript.extend(chunk)

    deadline = time.monotonic() + args.timeout

    try:
        # These reads enforce milestone order, not just marker presence.
        cursor = 0
        for marker in (
            b"EliteOS64 booted",
            b"[BOOT] console ok",
            b"[BOOT] pmm/heap ok",
            b"[BOOT] idt/pic/pit configured",
            b"[BOOT] pit irq ok",
            b"[BOOT] shell ready (serial + ps2 input)",
            b"elite> ",
        ):
            read_until(marker, start=cursor, deadline=deadline)
            cursor = transcript.find(marker, cursor) + len(marker)

        # Prove COM1 receive -> shell_feed_char -> command execution -> COM1 output.
        interaction_start = len(transcript)
        proc.stdin.write(b"ticks\r")
        proc.stdin.flush()

        read_until(b"ticks=", start=interaction_start, deadline=deadline)
        read_until(b"elite> ", start=interaction_start, deadline=deadline)

        log.write_bytes(transcript)
        print("[OK] QEMU booted, PIT IRQs fired, and serial shell executed ticks")
        return 0

    except BootFailure as exc:
        log.write_bytes(transcript)
        print(f"[FAIL] QEMU runtime: {exc}", file=sys.stderr)
        return 1

    finally:
        selector.close()
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=2)


if __name__ == "__main__":
    raise SystemExit(main())
