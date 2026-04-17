"""Core math services for the coursework project."""

from __future__ import annotations

from ast import (
    Add,
    BinOp,
    Call,
    Constant,
    Div,
    Expression,
    Load,
    Mod,
    Mult,
    Name,
    NodeVisitor,
    Pow,
    Sub,
    UAdd,
    UnaryOp,
    USub,
    parse,
)
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, getcontext
from math import acos, asin, atan, cos, degrees, e, exp, factorial, log, log10, pi, radians, sin, sqrt, tan
from statistics import mean, median
from typing import Callable


ALLOWED_FUNCTIONS: dict[str, Callable[..., float]] = {
    "sin": sin,
    "cos": cos,
    "tan": tan,
    "asin": asin,
    "acos": acos,
    "atan": atan,
    "sqrt": sqrt,
    "log": log,
    "log10": log10,
    "exp": exp,
    "factorial": factorial,
    "abs": abs,
    "round": round,
    "degrees": degrees,
    "radians": radians,
    "mean": mean,
    "median": median,
    "max": max,
    "min": min,
}

ALLOWED_CONSTANTS = {
    "pi": pi,
    "e": e,
}

ALLOWED_BINARY_OPS = (Add, Sub, Mult, Div, Pow, Mod)
ALLOWED_UNARY_OPS = (UAdd, USub)


class UnsafeExpressionError(ValueError):
    """Raised when the entered expression uses unsupported syntax."""


class SafeMathValidator(NodeVisitor):
    """AST validator that allows only safe mathematical expressions."""

    def visit_Expression(self, node: Expression) -> None:
        self.visit(node.body)

    def visit_BinOp(self, node: BinOp) -> None:
        if not isinstance(node.op, ALLOWED_BINARY_OPS):
            raise UnsafeExpressionError("Unsupported binary operation.")
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node: UnaryOp) -> None:
        if not isinstance(node.op, ALLOWED_UNARY_OPS):
            raise UnsafeExpressionError("Unsupported unary operation.")
        self.visit(node.operand)

    def visit_Call(self, node: Call) -> None:
        if not isinstance(node.func, Name) or node.func.id not in ALLOWED_FUNCTIONS:
            raise UnsafeExpressionError("Unsupported function used.")
        for arg in node.args:
            self.visit(arg)

    def visit_Name(self, node: Name) -> None:
        if node.id not in ALLOWED_CONSTANTS and node.id != "x":
            raise UnsafeExpressionError(f"Unsupported name: {node.id}")

    def visit_Constant(self, node: Constant) -> None:
        if not isinstance(node.value, (int, float)):
            raise UnsafeExpressionError("Only numeric constants are allowed.")

    def generic_visit(self, node) -> None:
        allowed = (Expression, BinOp, UnaryOp, Call, Name, Constant, Load)
        if not isinstance(node, allowed):
            raise UnsafeExpressionError("The expression contains unsupported syntax.")
        super().generic_visit(node)


class ExpressionEvaluator:
    """Evaluates mathematical expressions based on Python math modules."""

    def __init__(self) -> None:
        self._validator = SafeMathValidator()

    def evaluate(self, expression: str, x_value: float | None = None) -> float:
        if not expression.strip():
            raise ValueError("Enter a mathematical expression.")

        tree = parse(expression, mode="eval")
        self._validator.visit(tree)

        namespace = dict(ALLOWED_FUNCTIONS)
        namespace.update(ALLOWED_CONSTANTS)
        if x_value is not None:
            namespace["x"] = x_value

        return eval(compile(tree, "<expression>", "eval"), {"__builtins__": {}}, namespace)


@dataclass(slots=True)
class QuadraticResult:
    """Result of a quadratic equation solution."""

    discriminant: float
    root1: complex | float
    root2: complex | float


class QuadraticSolver:
    """Solves quadratic equations ax^2 + bx + c = 0."""

    @staticmethod
    def solve(a: float, b: float, c: float) -> QuadraticResult:
        if a == 0:
            raise ValueError("Coefficient a must not be zero.")

        discriminant = b**2 - 4 * a * c
        if discriminant >= 0:
            sqrt_d = sqrt(discriminant)
        else:
            sqrt_d = complex(0, sqrt(abs(discriminant)))

        root1 = (-b + sqrt_d) / (2 * a)
        root2 = (-b - sqrt_d) / (2 * a)
        return QuadraticResult(discriminant=discriminant, root1=root1, root2=root2)


class StatisticsService:
    """Provides descriptive statistics for numeric sequences."""

    @staticmethod
    def parse_numbers(raw_values: str) -> list[float]:
        items = [item.strip() for item in raw_values.replace(";", ",").split(",") if item.strip()]
        if not items:
            raise ValueError("Enter at least one number.")
        return [float(item) for item in items]

    def summarize(self, raw_values: str) -> dict[str, float]:
        numbers = self.parse_numbers(raw_values)
        return {
            "count": len(numbers),
            "min": min(numbers),
            "max": max(numbers),
            "mean": mean(numbers),
            "median": median(numbers),
            "sum": sum(numbers),
        }


class FinanceMath:
    """Works with Decimal for stable financial calculations."""

    def __init__(self, precision: int = 28) -> None:
        getcontext().prec = precision

    def compound_interest(
        self,
        principal: str,
        annual_rate_percent: str,
        years: str,
        compounds_per_year: str,
    ) -> Decimal:
        try:
            p = Decimal(principal)
            rate = Decimal(annual_rate_percent) / Decimal("100")
            t = Decimal(years)
            n = Decimal(compounds_per_year)
        except InvalidOperation as exc:
            raise ValueError("Financial parameters must be numeric.") from exc

        if p <= 0 or n <= 0 or t < 0:
            raise ValueError("Check the correctness of the input values.")

        amount = p * (Decimal("1") + rate / n) ** (n * t)
        return amount.quantize(Decimal("0.01"))


class FunctionSampler:
    """Samples values for y = f(x) on the given interval."""

    def __init__(self, evaluator: ExpressionEvaluator) -> None:
        self._evaluator = evaluator

    def sample(self, expression: str, x_min: float, x_max: float, steps: int = 80) -> list[tuple[float, float]]:
        if x_min >= x_max:
            raise ValueError("The left boundary must be smaller than the right boundary.")
        if steps < 2:
            raise ValueError("The number of steps must be at least 2.")

        result: list[tuple[float, float]] = []
        delta = (x_max - x_min) / (steps - 1)
        for index in range(steps):
            x_value = x_min + index * delta
            y_value = self._evaluator.evaluate(expression, x_value=x_value)
            result.append((x_value, y_value))
        return result
