#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "projects" / "elite-ir"))
import elite_ir as I

class IRTests(unittest.TestCase):
    def test_dominators_exact(self):
        fn = I.FunctionIR(
            "f",
            [],
            [
                I.Block("entry", term=I.Instr("cjump", args=["c", "left", "right"])),
                I.Block("left", term=I.Instr("jump", args=["join"])),
                I.Block("right", term=I.Instr("jump", args=["join"])),
                I.Block("join", term=I.Instr("ret", args=["x"])),
            ],
        )
        self.assertEqual(
            I.dominators(fn),
            {
                "entry": {"entry"},
                "left": {"entry", "left"},
                "right": {"entry", "right"},
                "join": {"entry", "join"},
            },
        )

    def test_liveness_exact(self):
        fn = I.FunctionIR(
            "f",
            [],
            [
                I.Block(
                    "entry",
                    instrs=[
                        I.Instr("mov", "x", ["a"]),
                        I.Instr("bin", "y", ["+", "x", "b"]),
                    ],
                    term=I.Instr("ret", args=["y"]),
                )
            ],
        )
        live_in, live_out = I.liveness(fn)
        self.assertEqual(live_in["entry"], {"a", "b"})
        self.assertEqual(live_out["entry"], set())

    def test_large_integer_division_folds_exactly(self):
        fn = I.FunctionIR(
            "f",
            [],
            [
                I.Block(
                    "entry",
                    instrs=[
                        I.Instr("const", "a", [str(I.INT64_MAX)]),
                        I.Instr("const", "b", ["3"]),
                        I.Instr("bin", "q", ["/", "a", "b"]),
                    ],
                )
            ],
        )
        I.optimize_local(fn)
        q = fn.blocks[0].instrs[-1]
        self.assertEqual(q.op, "const")
        self.assertEqual(int(q.args[0]), 3074457345618258602)

    def test_wrapping_add_matches_i64(self):
        fn = I.FunctionIR(
            "f",
            [],
            [
                I.Block(
                    "entry",
                    instrs=[
                        I.Instr("const", "a", [str(I.INT64_MAX)]),
                        I.Instr("const", "b", ["1"]),
                        I.Instr("bin", "q", ["+", "a", "b"]),
                    ],
                )
            ],
        )
        I.optimize_local(fn)
        self.assertEqual(int(fn.blocks[0].instrs[-1].args[0]), I.INT64_MIN)

    def test_division_trap_is_not_folded_away(self):
        fn = I.FunctionIR(
            "f",
            [],
            [
                I.Block(
                    "entry",
                    instrs=[
                        I.Instr("const", "a", [str(I.INT64_MIN)]),
                        I.Instr("const", "b", ["-1"]),
                        I.Instr("bin", "q", ["/", "a", "b"]),
                    ],
                )
            ],
        )
        I.optimize_local(fn)
        self.assertEqual(fn.blocks[0].instrs[-1].op, "bin")

    def test_phi_candidates_are_explicitly_only_candidates(self):
        fn = I.FunctionIR(
            "f",
            [],
            [
                I.Block("entry", term=I.Instr("cjump", args=["c", "left", "right"])),
                I.Block(
                    "left",
                    instrs=[I.Instr("mov", "x", ["a"])],
                    term=I.Instr("jump", args=["join"]),
                ),
                I.Block(
                    "right",
                    instrs=[I.Instr("mov", "x", ["b"])],
                    term=I.Instr("jump", args=["join"]),
                ),
                I.Block("join", term=I.Instr("ret", args=["x"])),
            ],
        )
        self.assertEqual(I.ssa_phi_candidates(fn), {"join": ["x"]})

if __name__ == "__main__":
    unittest.main()
