#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "projects" / "elite-frontend"))
import elite_frontend as F

class FrontendTests(unittest.TestCase):
    def parse(self, body: str):
        return F.parse_source(body)

    def assert_compile_error(self, source: str, contains: str | None = None):
        with self.assertRaises(F.CompileError) as ctx:
            self.parse(source)
        if contains is not None:
            self.assertIn(contains, str(ctx.exception))

    def test_precedence_multiplication_before_addition(self):
        program = self.parse("fn main() -> int { return 1 + 2 * 3; }")
        expr = program.functions[0].body.statements[0].value
        self.assertIsInstance(expr, F.Binary)
        self.assertEqual(expr.op, "+")
        self.assertIsInstance(expr.right, F.Binary)
        self.assertEqual(expr.right.op, "*")

    def test_main_signature_is_fixed(self):
        self.assert_compile_error(
            "fn main(x:int) -> int { return x; }",
            "main must have signature",
        )
        self.assert_compile_error(
            "fn main() -> bool { return true; }",
            "main must have signature",
        )

    def test_missing_main(self):
        self.assert_compile_error(
            "fn helper() -> int { return 1; }",
            "must define main",
        )

    def test_literal_range(self):
        self.parse("fn main() -> int { return 9223372036854775807; }")
        self.assert_compile_error(
            "fn main() -> int { return 9223372036854775808; }",
            "out of signed 64-bit range",
        )

    def test_duplicate_function_and_parameter(self):
        self.assert_compile_error(
            "fn main() -> int { return 0; } fn main() -> int { return 1; }",
            "duplicate function",
        )
        self.assert_compile_error(
            "fn f(x:int,x:int) -> int { return x; } "
            "fn main() -> int { return 0; }",
            "duplicate parameter",
        )

    def test_unknown_variable_and_function(self):
        self.assert_compile_error(
            "fn main() -> int { return nope; }",
            "unknown variable",
        )
        self.assert_compile_error(
            "fn main() -> int { return nope(); }",
            "unknown function",
        )

    def test_wrong_arity(self):
        self.assert_compile_error(
            "fn f(x:int) -> int { return x; } "
            "fn main() -> int { return f(); }",
            "expects 1 args",
        )

    def test_if_and_while_require_bool(self):
        self.assert_compile_error(
            "fn main() -> int { if (1) { return 1; } else { return 0; } }",
            "if condition must be bool",
        )
        self.assert_compile_error(
            "fn main() -> int { let x:int=0; while (x) { x=x+1; } return x; }",
            "while condition must be bool",
        )

    def test_short_circuit_ast(self):
        program = self.parse(
            "fn main() -> int { if (false && true || true) { return 0; } else { return 1; } }"
        )
        cond = program.functions[0].body.statements[0].cond
        self.assertIsInstance(cond, F.Binary)
        self.assertEqual(cond.op, "||")
        self.assertIsInstance(cond.left, F.Binary)
        self.assertEqual(cond.left.op, "&&")

if __name__ == "__main__":
    unittest.main()
