"""Tkinter desktop application for the coursework project."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from math_engine import ExpressionEvaluator, FinanceMath, FunctionSampler, QuadraticSolver, StatisticsService


class MathModulesApp(tk.Tk):
    """Desktop application demonstrating Python math modules."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Math Modules Explorer")
        self.geometry("1040x760")
        self.minsize(920, 680)

        self.evaluator = ExpressionEvaluator()
        self.sampler = FunctionSampler(self.evaluator)
        self.quadratic_solver = QuadraticSolver()
        self.statistics_service = StatisticsService()
        self.finance_math = FinanceMath()

        self._build_ui()

    def _build_ui(self) -> None:
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=12, pady=12)

        notebook.add(self._build_calculator_tab(notebook), text="Calculator")
        notebook.add(self._build_equation_tab(notebook), text="Quadratic")
        notebook.add(self._build_statistics_tab(notebook), text="Statistics")
        notebook.add(self._build_finance_tab(notebook), text="Decimal")
        notebook.add(self._build_plot_tab(notebook), text="Plot")

    def _build_calculator_tab(self, parent: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(parent, padding=16)
        frame.columnconfigure(0, weight=1)

        ttk.Label(
            frame,
            text="Enter an expression. Available functions: sin, cos, tan, sqrt, log, exp, factorial, mean, median, max, min.",
            wraplength=900,
        ).grid(row=0, column=0, sticky="w")

        self.expression_var = tk.StringVar(value="sin(pi / 4) + sqrt(16)")
        ttk.Entry(frame, textvariable=self.expression_var, font=("Segoe UI", 12)).grid(
            row=1, column=0, sticky="ew", pady=(12, 8)
        )

        ttk.Button(frame, text="Calculate", command=self._calculate_expression).grid(row=2, column=0, sticky="w")

        self.calculator_output = tk.Text(frame, height=10, wrap="word")
        self.calculator_output.grid(row=3, column=0, sticky="nsew", pady=(12, 0))
        frame.rowconfigure(3, weight=1)
        return frame

    def _build_equation_tab(self, parent: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(parent, padding=16)

        ttk.Label(frame, text="Solve ax^2 + bx + c = 0").grid(row=0, column=0, columnspan=2, sticky="w")

        self.a_var = tk.StringVar(value="1")
        self.b_var = tk.StringVar(value="-3")
        self.c_var = tk.StringVar(value="2")

        for row, (caption, variable) in enumerate((("a", self.a_var), ("b", self.b_var), ("c", self.c_var)), start=1):
            ttk.Label(frame, text=f"{caption}:").grid(row=row, column=0, sticky="e", pady=4, padx=(0, 8))
            ttk.Entry(frame, textvariable=variable, width=20).grid(row=row, column=1, sticky="w", pady=4)

        ttk.Button(frame, text="Solve", command=self._solve_quadratic).grid(row=4, column=0, columnspan=2, sticky="w", pady=10)

        self.quadratic_result = tk.Text(frame, width=60, height=12)
        self.quadratic_result.grid(row=5, column=0, columnspan=2, sticky="nsew")
        frame.rowconfigure(5, weight=1)
        frame.columnconfigure(1, weight=1)
        return frame

    def _build_statistics_tab(self, parent: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(parent, padding=16)
        frame.columnconfigure(0, weight=1)

        ttk.Label(frame, text="Enter numbers separated by comma or semicolon.").grid(row=0, column=0, sticky="w")
        self.stats_var = tk.StringVar(value="12, 14, 19, 21, 29")
        ttk.Entry(frame, textvariable=self.stats_var, font=("Segoe UI", 12)).grid(row=1, column=0, sticky="ew", pady=(12, 8))

        ttk.Button(frame, text="Analyze", command=self._calculate_statistics).grid(row=2, column=0, sticky="w")

        self.stats_output = tk.Text(frame, height=12, wrap="word")
        self.stats_output.grid(row=3, column=0, sticky="nsew", pady=(12, 0))
        frame.rowconfigure(3, weight=1)
        return frame

    def _build_finance_tab(self, parent: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(parent, padding=16)
        labels = (
            ("Initial amount", "100000"),
            ("Annual rate, %", "12"),
            ("Years", "3"),
            ("Compounds per year", "12"),
        )
        self.finance_vars: list[tk.StringVar] = []
        for row, (caption, default) in enumerate(labels):
            ttk.Label(frame, text=caption + ":").grid(row=row, column=0, sticky="e", padx=(0, 8), pady=6)
            variable = tk.StringVar(value=default)
            self.finance_vars.append(variable)
            ttk.Entry(frame, textvariable=variable, width=24).grid(row=row, column=1, sticky="w", pady=6)

        ttk.Button(frame, text="Compound interest", command=self._calculate_finance).grid(
            row=len(labels), column=0, columnspan=2, sticky="w", pady=10
        )

        self.finance_output = tk.Text(frame, width=60, height=10)
        self.finance_output.grid(row=len(labels) + 1, column=0, columnspan=2, sticky="nsew")
        frame.rowconfigure(len(labels) + 1, weight=1)
        frame.columnconfigure(1, weight=1)
        return frame

    def _build_plot_tab(self, parent: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(parent, padding=16)
        controls = ttk.Frame(frame)
        controls.pack(fill="x")

        self.plot_expression_var = tk.StringVar(value="sin(x)")
        self.x_min_var = tk.StringVar(value="-6.28")
        self.x_max_var = tk.StringVar(value="6.28")

        ttk.Label(controls, text="f(x) =").grid(row=0, column=0, padx=(0, 6))
        ttk.Entry(controls, textvariable=self.plot_expression_var, width=26).grid(row=0, column=1, padx=(0, 12))
        ttk.Label(controls, text="x min").grid(row=0, column=2, padx=(0, 6))
        ttk.Entry(controls, textvariable=self.x_min_var, width=12).grid(row=0, column=3, padx=(0, 12))
        ttk.Label(controls, text="x max").grid(row=0, column=4, padx=(0, 6))
        ttk.Entry(controls, textvariable=self.x_max_var, width=12).grid(row=0, column=5, padx=(0, 12))
        ttk.Button(controls, text="Draw plot", command=self._draw_plot).grid(row=0, column=6)

        self.plot_canvas = tk.Canvas(frame, bg="white", height=460, highlightthickness=1, highlightbackground="#aaaaaa")
        self.plot_canvas.pack(fill="both", expand=True, pady=(16, 0))
        self.plot_canvas.bind("<Configure>", lambda _event: self._draw_plot())
        return frame

    def _calculate_expression(self) -> None:
        try:
            result = self.evaluator.evaluate(self.expression_var.get())
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Calculation error", str(exc))
            return

        self.calculator_output.delete("1.0", tk.END)
        self.calculator_output.insert(
            tk.END,
            f"Expression: {self.expression_var.get()}\nResult: {result}\n\n"
            "The project uses the math module and AST validation to avoid executing arbitrary code.",
        )

    def _solve_quadratic(self) -> None:
        try:
            result = self.quadratic_solver.solve(float(self.a_var.get()), float(self.b_var.get()), float(self.c_var.get()))
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Solver error", str(exc))
            return

        self.quadratic_result.delete("1.0", tk.END)
        self.quadratic_result.insert(
            tk.END,
            f"Discriminant: {result.discriminant}\n"
            f"x1 = {result.root1}\n"
            f"x2 = {result.root2}\n\n"
            "If the discriminant is negative, the program returns complex roots.",
        )

    def _calculate_statistics(self) -> None:
        try:
            summary = self.statistics_service.summarize(self.stats_var.get())
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Statistics error", str(exc))
            return

        self.stats_output.delete("1.0", tk.END)
        for key, value in summary.items():
            self.stats_output.insert(tk.END, f"{key}: {value}\n")

    def _calculate_finance(self) -> None:
        try:
            amount = self.finance_math.compound_interest(*(variable.get() for variable in self.finance_vars))
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Finance error", str(exc))
            return

        self.finance_output.delete("1.0", tk.END)
        self.finance_output.insert(
            tk.END,
            f"Final amount: {amount}\n\n"
            "The decimal module helps avoid common rounding issues in financial calculations.",
        )

    def _draw_plot(self) -> None:
        canvas = self.plot_canvas
        width = canvas.winfo_width() or 800
        height = canvas.winfo_height() or 460
        canvas.delete("all")

        try:
            samples = self.sampler.sample(
                self.plot_expression_var.get(),
                float(self.x_min_var.get()),
                float(self.x_max_var.get()),
                steps=max(40, width // 8),
            )
        except Exception as exc:  # noqa: BLE001
            canvas.create_text(width / 2, height / 2, text=str(exc), fill="red", font=("Segoe UI", 12))
            return

        y_values = [point[1] for point in samples]
        y_min = min(y_values)
        y_max = max(y_values)
        if y_min == y_max:
            y_min -= 1
            y_max += 1

        x_min = samples[0][0]
        x_max = samples[-1][0]

        def map_x(value: float) -> float:
            return 40 + (value - x_min) * (width - 80) / (x_max - x_min)

        def map_y(value: float) -> float:
            return height - 40 - (value - y_min) * (height - 80) / (y_max - y_min)

        zero_x = map_x(0) if x_min <= 0 <= x_max else None
        zero_y = map_y(0) if y_min <= 0 <= y_max else None

        if zero_x is not None:
            canvas.create_line(zero_x, 20, zero_x, height - 20, fill="#999999")
        if zero_y is not None:
            canvas.create_line(20, zero_y, width - 20, zero_y, fill="#999999")

        canvas.create_rectangle(20, 20, width - 20, height - 20, outline="#bbbbbb")

        points: list[float] = []
        for x_value, y_value in samples:
            points.extend((map_x(x_value), map_y(y_value)))
        canvas.create_line(*points, fill="#1f77b4", width=2, smooth=True)

        canvas.create_text(80, 30, text=f"y = {self.plot_expression_var.get()}", anchor="w", font=("Segoe UI", 11, "bold"))
        canvas.create_text(80, height - 22, text=f"x in [{x_min:.2f}; {x_max:.2f}], y in [{y_min:.2f}; {y_max:.2f}]", anchor="w")


if __name__ == "__main__":
    app = MathModulesApp()
    app.mainloop()
