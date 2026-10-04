#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


REPORT = load_module(
    "course_binary_report",
    ROOT / "projects" / "binary-report" / "binary_report.py",
)
CFG = load_module(
    "course_cfg_extract",
    ROOT / "projects" / "cfg-extract" / "cfg_extract.py",
)


class BinaryReportTests(unittest.TestCase):
    def test_required_tool_nonzero_raises(self):
        completed = subprocess.CompletedProcess(
            args=("readelf", "-hW", "bad"),
            returncode=1,
            stdout="readelf: Error: Not an ELF file\n",
        )
        with mock.patch.object(REPORT.subprocess, "run", return_value=completed):
            with self.assertRaises(REPORT.ReportError):
                REPORT.run_required("readelf", "-hW", "bad")

    def test_optional_tool_nonzero_is_structured_not_silent(self):
        completed = subprocess.CompletedProcess(
            args=("nm", "-an", "stripped"),
            returncode=1,
            stdout="nm: no symbols\n",
        )
        with mock.patch.object(REPORT.subprocess, "run", return_value=completed):
            result = REPORT.run_optional("nm", "-an", "stripped")
        self.assertEqual(result["status"], "nonzero")
        self.assertEqual(result["returncode"], 1)
        self.assertIn("no symbols", result["output"])


class CFGTests(unittest.TestCase):
    SAMPLE = """\
0000000000401000 <demo>:
  401000: 83 ff 00              cmp    edi,0x0
  401003: 74 05                 je     40100a <demo+0xa>
  401005: b8 01 00 00 00        mov    eax,0x1
  40100a: c3                    ret
"""

    def test_conditional_branch_creates_branch_and_fallthrough_edges(self):
        functions = CFG.parse_objdump(self.SAMPLE)
        self.assertEqual(len(functions), 1)
        result = CFG.analyze_function(functions[0])

        blocks = {block["start"]: block for block in result["blocks"]}
        self.assertIn(0x401000, blocks)
        first_edges = {
            (edge["kind"], edge["target"])
            for edge in blocks[0x401000]["edges"]
        }
        self.assertEqual(
            first_edges,
            {
                ("branch", 0x40100A),
                ("fallthrough", 0x401005),
            },
        )

    def test_call_is_not_misclassified_as_cfg_branch(self):
        text = """\
0000000000402000 <caller>:
  402000: e8 fb 0f 00 00        call   403000 <callee>
  402005: c3                    ret
"""
        result = CFG.analyze_function(CFG.parse_objdump(text)[0])
        self.assertEqual(len(result["calls"]), 1)
        self.assertEqual(result["calls"][0]["target"], 0x403000)
        all_edges = [
            edge
            for block in result["blocks"]
            for edge in block["edges"]
        ]
        self.assertFalse(
            any(edge["target"] == 0x403000 for edge in all_edges)
        )

    def test_indirect_jump_is_left_unresolved_not_invented(self):
        text = """\
0000000000403000 <dispatch>:
  403000: ff e0                 jmp    rax
"""
        result = CFG.analyze_function(CFG.parse_objdump(text)[0])
        self.assertEqual(len(result["blocks"]), 1)
        self.assertEqual(result["blocks"][0]["edges"], [])


if __name__ == "__main__":
    unittest.main()
