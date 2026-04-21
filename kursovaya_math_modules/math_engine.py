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
from math import gcd


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
            raise UnsafeExpressionError("Недопустимая бинарная операция.")
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node: UnaryOp) -> None:
        if not isinstance(node.op, ALLOWED_UNARY_OPS):
            raise UnsafeExpressionError("Недопустимая унарная операция.")
        self.visit(node.operand)

    def visit_Call(self, node: Call) -> None:
        if not isinstance(node.func, Name) or node.func.id not in ALLOWED_FUNCTIONS:
            raise UnsafeExpressionError("Использована неподдерживаемая функция.")
        for arg in node.args:
            self.visit(arg)

    def visit_Name(self, node: Name) -> None:
        if node.id not in ALLOWED_CONSTANTS and node.id != "x":
            raise UnsafeExpressionError(f"Недопустимое имя: {node.id}")

    def visit_Constant(self, node: Constant) -> None:
        if not isinstance(node.value, (int, float)):
            raise UnsafeExpressionError("Разрешены только числовые константы.")

    def generic_visit(self, node) -> None:
        allowed = (Expression, BinOp, UnaryOp, Call, Name, Constant, Load)
        if not isinstance(node, allowed):
            raise UnsafeExpressionError("В выражении обнаружена недопустимая конструкция.")
        super().generic_visit(node)


class ExpressionEvaluator:
    """Evaluates mathematical expressions based on Python math modules."""

    def __init__(self) -> None:
        self._validator = SafeMathValidator()

    def evaluate(self, expression: str, x_value: float | None = None) -> float:
        if not expression.strip():
            raise ValueError("Введите математическое выражение.")

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
            raise ValueError("Коэффициент a не должен быть равен нулю.")

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
            raise ValueError("Введите хотя бы одно число.")
        return [float(item) for item in items]

    def summarize(self, raw_values: str) -> dict[str, float]:
        numbers = self.parse_numbers(raw_values)
        return {
            "Количество чисел": len(numbers),
            "Минимум": min(numbers),
            "Максимум": max(numbers),
            "Среднее арифметическое": mean(numbers),
            "Медиана": median(numbers),
            "Сумма": sum(numbers),
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
            raise ValueError("Финансовые параметры должны быть числами.") from exc

        if p <= 0 or n <= 0 or t < 0:
            raise ValueError("Проверьте корректность исходных данных.")

        amount = p * (Decimal("1") + rate / n) ** (n * t)
        return amount.quantize(Decimal("0.01"))


class FunctionSampler:
    """Samples values for y = f(x) on the given interval."""

    def __init__(self, evaluator: ExpressionEvaluator) -> None:
        self._evaluator = evaluator

    def sample(self, expression: str, x_min: float, x_max: float, steps: int = 80) -> list[tuple[float, float]]:
        if x_min >= x_max:
            raise ValueError("Левая граница должна быть меньше правой.")
        if steps < 2:
            raise ValueError("Количество шагов должно быть не меньше 2.")

        result: list[tuple[float, float]] = []
        delta = (x_max - x_min) / (steps - 1)
        for index in range(steps):
            x_value = x_min + index * delta
            y_value = self._evaluator.evaluate(expression, x_value=x_value)
            result.append((x_value, y_value))
        return result


class NumberTheoryService:
    """Provides integer number theory calculations."""

    @staticmethod
    def parse_int(value: str) -> int:
        try:
            return int(value.strip())
        except ValueError as exc:
            raise ValueError("Введите целое число.") from exc

    @staticmethod
    def lcm(a: int, b: int) -> int:
        if a == 0 or b == 0:
            return 0
        return abs(a * b) // gcd(a, b)

    @staticmethod
    def is_prime(value: int) -> bool:
        if value < 2:
            return False
        if value in (2, 3):
            return True
        if value % 2 == 0:
            return False
        divisor = 3
        while divisor * divisor <= value:
            if value % divisor == 0:
                return False
            divisor += 2
        return True

    def analyze(self, raw_a: str, raw_b: str) -> dict[str, int | bool]:
        a = self.parse_int(raw_a)
        b = self.parse_int(raw_b)
        return {
            "a": a,
            "b": b,
            "gcd": gcd(a, b),
            "lcm": self.lcm(a, b),
            "a_is_prime": self.is_prime(a),
            "b_is_prime": self.is_prime(b),
        }


class GeometryService:
    """Calculates areas and lengths for basic geometric figures."""

    @staticmethod
    def parse_positive(value: str, name: str) -> float:
        try:
            result = float(value.strip())
        except ValueError as exc:
            raise ValueError(f"Параметр {name} должен быть числом.") from exc
        if result <= 0:
            raise ValueError(f"Параметр {name} должен быть больше нуля.")
        return result

    def circle(self, radius: str) -> dict[str, float]:
        r = self.parse_positive(radius, "r")
        return {
            "radius": r,
            "diameter": 2 * r,
            "circumference": 2 * pi * r,
            "area": pi * r * r,
        }

    def rectangle(self, width: str, height: str) -> dict[str, float]:
        w = self.parse_positive(width, "a")
        h = self.parse_positive(height, "b")
        return {
            "width": w,
            "height": h,
            "perimeter": 2 * (w + h),
            "area": w * h,
            "diagonal": sqrt(w * w + h * h),
        }
