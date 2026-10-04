#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "projects" / "linear-scan"))

from linear_scan import Allocation, Interval, linear_scan_allocate

class LinearScanTests(unittest.TestCase):
    def test_non_overlapping_intervals_reuse_register(self):
        result = linear_scan_allocate(
            [Interval("a", 0, 1), Interval("b", 2, 3)],
            ["r10"],
        )
        self.assertEqual(result["a"].location, "r10")
        self.assertEqual(result["b"].location, "r10")
        self.assertFalse(result["a"].spilled)
        self.assertFalse(result["b"].spilled)

    def test_overlapping_intervals_need_distinct_registers(self):
        result = linear_scan_allocate(
            [Interval("a", 0, 4), Interval("b", 1, 3)],
            ["r10", "r11"],
        )
        self.assertNotEqual(result["a"].location, result["b"].location)

    def test_pressure_causes_spill(self):
        result = linear_scan_allocate(
            [
                Interval("a", 0, 10),
                Interval("b", 1, 9),
                Interval("c", 2, 3),
            ],
            ["r10", "r11"],
        )
        spilled = {name for name, item in result.items() if item.spilled}
        self.assertEqual(len(spilled), 1)
        self.assertIn("a", spilled)
        self.assertFalse(result["c"].spilled)

    def test_duplicate_names_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate interval"):
            linear_scan_allocate(
                [Interval("a", 0, 1), Interval("a", 2, 3)],
                ["r10"],
            )

    def test_invalid_interval_is_rejected(self):
        with self.assertRaises(ValueError):
            Interval("bad", 5, 4)

if __name__ == "__main__":
    unittest.main()
