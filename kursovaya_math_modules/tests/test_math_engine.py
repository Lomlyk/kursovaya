"""Automated tests for the coursework project."""

import unittest

from math_engine import ExpressionEvaluator, FinanceMath, GeometryService, NumberTheoryService, QuadraticSolver, StatisticsService


class ExpressionEvaluatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.evaluator = ExpressionEvaluator()

    def test_basic_expression(self) -> None:
        result = self.evaluator.evaluate("sin(pi / 2) + sqrt(9)")
        self.assertAlmostEqual(result, 4.0, places=5)

    def test_expression_with_variable(self) -> None:
        result = self.evaluator.evaluate("x**2 + 2*x + 1", x_value=3)
        self.assertEqual(result, 16)

    def test_unsafe_expression_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.evaluator.evaluate("__import__('os').system('dir')")


class QuadraticSolverTests(unittest.TestCase):
    def test_real_roots(self) -> None:
        result = QuadraticSolver.solve(1, -3, 2)
        self.assertEqual(result.root1, 2.0)
        self.assertEqual(result.root2, 1.0)

    def test_complex_roots(self) -> None:
        result = QuadraticSolver.solve(1, 0, 1)
        self.assertEqual(result.discriminant, -4)
        self.assertEqual(result.root1, 1j)
        self.assertEqual(result.root2, -1j)


class StatisticsServiceTests(unittest.TestCase):
    def test_summary(self) -> None:
        stats = StatisticsService().summarize("2, 4, 6, 8")
        self.assertEqual(stats["Количество чисел"], 4)
        self.assertEqual(stats["Сумма"], 20)
        self.assertEqual(stats["Медиана"], 5.0)


class FinanceMathTests(unittest.TestCase):
    def test_compound_interest(self) -> None:
        amount = FinanceMath().compound_interest("100000", "12", "3", "12")
        self.assertEqual(str(amount), "143076.88")


class NumberTheoryServiceTests(unittest.TestCase):
    def test_number_theory_summary(self) -> None:
        result = NumberTheoryService().analyze("24", "36")
        self.assertEqual(result["gcd"], 12)
        self.assertEqual(result["lcm"], 72)
        self.assertFalse(result["a_is_prime"])


class GeometryServiceTests(unittest.TestCase):
    def test_circle(self) -> None:
        result = GeometryService().circle("2")
        self.assertAlmostEqual(result["diameter"], 4.0, places=5)
        self.assertAlmostEqual(result["area"], 12.566370, places=5)

    def test_rectangle(self) -> None:
        result = GeometryService().rectangle("3", "4")
        self.assertEqual(result["perimeter"], 14.0)
        self.assertEqual(result["diagonal"], 5.0)


if __name__ == "__main__":
    unittest.main()
