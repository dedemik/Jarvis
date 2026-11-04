import unittest

from jarvis.calculator import calculate


class CalculateTests(unittest.TestCase):
    def test_calculates_arithmetic_with_precedence(self):
        self.assertEqual(calculate("12 * (3 + 2)"), 60)
        self.assertEqual(calculate("-4 + 2 ** 3"), 4)

    def test_rejects_code_and_unsupported_operations(self):
        for expression in ("__import__('os')", "2 ** 11", "1 < 2", ""):
            with self.subTest(expression=expression):
                with self.assertRaises(ValueError):
                    calculate(expression)

    def test_reports_division_by_zero(self):
        with self.assertRaisesRegex(ValueError, "hesaplanamıyor"):
            calculate("1 / 0")
