#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import re
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "projects" / "elite-ir"))

import elite_ir as I
import elite_ssa as S

class SSATests(unittest.TestCase):
    def lower_main(self, source: str):
        module = I.lower_source(source)
        return next(fn for fn in module.functions if fn.name == "main")

    def test_diamond_has_real_phi_and_versioned_uses(self):
        fn = self.lower_main(
            """
            fn main() -> int {
              let x:int = 0;
              if (true) { x = 1; } else { x = 2; }
              return x;
            }
            """
        )
        text = S.format_ssa(fn)
        self.assertRegex(text, r"x\.\d+ = phi \[then\d+: x\.\d+\] \[else\d+: x\.\d+\]")
        self.assertRegex(text, r"ret x\.\d+")

    def test_loop_header_gets_phi(self):
        fn = self.lower_main(
            """
            fn main() -> int {
              let i:int = 0;
              while (i < 3) {
                i = i + 1;
              }
              return i;
            }
            """
        )
        text = S.format_ssa(fn)
        self.assertIn("while_cond", text)
        self.assertRegex(text, r"i\.\d+ = phi ")
        self.assertNotRegex(text, r"\bret i\b")

    def test_immediate_dominators_diamond(self):
        fn = I.FunctionIR(
            "f", [],
            [
                I.Block("entry", term=I.Instr("cjump", args=["c", "left", "right"])),
                I.Block("left", term=I.Instr("jump", args=["join"])),
                I.Block("right", term=I.Instr("jump", args=["join"])),
                I.Block("join", term=I.Instr("ret", args=["x"])),
            ],
        )
        self.assertEqual(
            S.immediate_dominators(fn),
            {
                "entry": None,
                "left": "entry",
                "right": "entry",
                "join": "entry",
            },
        )

    def test_dominance_frontier_diamond(self):
        fn = I.FunctionIR(
            "f", [],
            [
                I.Block("entry", term=I.Instr("cjump", args=["c", "left", "right"])),
                I.Block("left", term=I.Instr("jump", args=["join"])),
                I.Block("right", term=I.Instr("jump", args=["join"])),
                I.Block("join", term=I.Instr("ret", args=["x"])),
            ],
        )
        frontier = S.dominance_frontiers(fn)
        self.assertEqual(frontier["left"], {"join"})
        self.assertEqual(frontier["right"], {"join"})

if __name__ == "__main__":
    unittest.main()
