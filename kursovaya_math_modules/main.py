"""Tkinter desktop application for the coursework project."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from math_engine import (
    ExpressionEvaluator,
    FinanceMath,
    FunctionSampler,
    GeometryService,
    NumberTheoryService,
    QuadraticSolver,
    StatisticsService,
)


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
        self.number_theory_service = NumberTheoryService()
        self.geometry_service = GeometryService()

        self._configure_styles()
        self._build_ui()

    def _configure_styles(self) -> None:
        self.configure(bg="#eef3f8")
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("App.TFrame", background="#eef3f8")
        style.configure("Card.TFrame", background="#ffffff", relief="flat")
        style.configure("Header.TLabel", background="#eef3f8", foreground="#1f2a44", font=("Segoe UI", 22, "bold"))
        style.configure("SubHeader.TLabel", background="#eef3f8", foreground="#5b6780", font=("Segoe UI", 10))
        style.configure("Section.TLabel", background="#ffffff", foreground="#1f2a44", font=("Segoe UI", 11, "bold"))
        style.configure("TLabel", background="#ffffff", foreground="#24324a")
        style.configure("TNotebook", background="#eef3f8", borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=(12, 8), background="#d8e3ef")
        style.map("TNotebook.Tab", background=[("selected", "#ffffff")], foreground=[("selected", "#0f172a")])
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), foreground="#ffffff", background="#2f6fed", borderwidth=0)
        style.map("Accent.TButton", background=[("active", "#2458bc")])

    def _build_ui(self) -> None:
        root = ttk.Frame(self, style="App.TFrame", padding=14)
        root.pack(fill="both", expand=True)

        header = ttk.Frame(root, style="App.TFrame")
        header.pack(fill="x", pady=(0, 12))
        ttk.Label(header, text="Math Modules Explorer", style="Header.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Курсовой проект по теме математических модулей Python: вычисления, графики, статистика и прикладные задачи.",
            style="SubHeader.TLabel",
        ).pack(anchor="w", pady=(4, 0))

        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True)

        notebook.add(self._build_calculator_tab(notebook), text="Калькулятор")
        notebook.add(self._build_equation_tab(notebook), text="Квадратное уравнение")
        notebook.add(self._build_statistics_tab(notebook), text="Статистика")
        notebook.add(self._build_finance_tab(notebook), text="Финансы")
        notebook.add(self._build_number_tab(notebook), text="Числа")
        notebook.add(self._build_geometry_tab(notebook), text="Геометрия")
        notebook.add(self._build_plot_tab(notebook), text="График")

    def _build_calculator_tab(self, parent: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(parent, padding=18, style="Card.TFrame")
        frame.columnconfigure(0, weight=1)

        ttk.Label(
            frame,
            text="Введите выражение. Доступны функции: sin, cos, tan, sqrt, log, exp, factorial, mean, median, max, min.",
            style="Section.TLabel",
            wraplength=900,
        ).grid(row=0, column=0, sticky="w")

        self.expression_var = tk.StringVar(value="sin(pi / 4) + sqrt(16)")
        ttk.Entry(frame, textvariable=self.expression_var, font=("Segoe UI", 12)).grid(
            row=1, column=0, sticky="ew", pady=(12, 8)
        )

        button_panel = ttk.Frame(frame, style="Card.TFrame")
        button_panel.grid(row=2, column=0, sticky="w", pady=(0, 8))

        quick_buttons = (
            ("sin(x)", "sin("),
            ("cos(x)", "cos("),
            ("tan(x)", "tan("),
            ("sqrt(x)", "sqrt("),
            ("log(x)", "log("),
            ("log10(x)", "log10("),
            ("exp(x)", "exp("),
            ("abs(x)", "abs("),
            ("pi", "pi"),
            ("e", "e"),
        )
        for index, (caption, token) in enumerate(quick_buttons):
            ttk.Button(
                button_panel,
                text=caption,
                command=lambda value=token: self._insert_expression_token(value),
            ).grid(row=index // 5, column=index % 5, padx=(0, 8), pady=(0, 8), sticky="w")

        ttk.Button(frame, text="Вычислить", style="Accent.TButton", command=self._calculate_expression).grid(row=3, column=0, sticky="w")

        self.calculator_output = tk.Text(
            frame, height=12, wrap="word", bg="#f8fbff", fg="#1f2a44", relief="flat", font=("Consolas", 11)
        )
        self.calculator_output.grid(row=4, column=0, sticky="nsew", pady=(12, 0))
        frame.rowconfigure(4, weight=1)
        return frame

    def _build_equation_tab(self, parent: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(parent, padding=18, style="Card.TFrame")

        ttk.Label(frame, text="Решение уравнения ax^2 + bx + c = 0", style="Section.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w"
        )

        self.a_var = tk.StringVar(value="1")
        self.b_var = tk.StringVar(value="-3")
        self.c_var = tk.StringVar(value="2")

        for row, (caption, variable) in enumerate((("a", self.a_var), ("b", self.b_var), ("c", self.c_var)), start=1):
            ttk.Label(frame, text=f"{caption}:").grid(row=row, column=0, sticky="e", pady=4, padx=(0, 8))
            ttk.Entry(frame, textvariable=variable, width=20).grid(row=row, column=1, sticky="w", pady=4)

        ttk.Button(frame, text="Найти корни", style="Accent.TButton", command=self._solve_quadratic).grid(
            row=4, column=0, columnspan=2, sticky="w", pady=10
        )

        self.quadratic_result = tk.Text(
            frame, width=60, height=12, bg="#f8fbff", fg="#1f2a44", relief="flat", font=("Consolas", 11)
        )
        self.quadratic_result.grid(row=5, column=0, columnspan=2, sticky="nsew")
        frame.rowconfigure(5, weight=1)
        frame.columnconfigure(1, weight=1)
        return frame

    def _build_statistics_tab(self, parent: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(parent, padding=18, style="Card.TFrame")
        frame.columnconfigure(0, weight=1)

        ttk.Label(frame, text="Введите числа через запятую или точку с запятой.", style="Section.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        self.stats_var = tk.StringVar(value="12, 14, 19, 21, 29")
        ttk.Entry(frame, textvariable=self.stats_var, font=("Segoe UI", 12)).grid(row=1, column=0, sticky="ew", pady=(12, 8))

        ttk.Button(frame, text="Рассчитать статистику", style="Accent.TButton", command=self._calculate_statistics).grid(
            row=2, column=0, sticky="w"
        )

        self.stats_output = tk.Text(
            frame, height=12, wrap="word", bg="#f8fbff", fg="#1f2a44", relief="flat", font=("Consolas", 11)
        )
        self.stats_output.grid(row=3, column=0, sticky="nsew", pady=(12, 0))
        frame.rowconfigure(3, weight=1)
        return frame

    def _build_finance_tab(self, parent: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(parent, padding=18, style="Card.TFrame")
        ttk.Label(frame, text="Расчет сложных процентов с модулем Decimal", style="Section.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 10)
        )
        labels = (
            ("Начальная сумма", "100000"),
            ("Годовая ставка, %", "12"),
            ("Срок, лет", "3"),
            ("Начислений в год", "12"),
        )
        self.finance_vars: list[tk.StringVar] = []
        for row, (caption, default) in enumerate(labels, start=1):
            ttk.Label(frame, text=caption + ":").grid(row=row, column=0, sticky="e", padx=(0, 8), pady=6)
            variable = tk.StringVar(value=default)
            self.finance_vars.append(variable)
            ttk.Entry(frame, textvariable=variable, width=24).grid(row=row, column=1, sticky="w", pady=6)

        ttk.Button(frame, text="Рассчитать сложный процент", style="Accent.TButton", command=self._calculate_finance).grid(
            row=len(labels) + 1, column=0, columnspan=2, sticky="w", pady=10
        )

        self.finance_output = tk.Text(
            frame, width=60, height=10, bg="#f8fbff", fg="#1f2a44", relief="flat", font=("Consolas", 11)
        )
        self.finance_output.grid(row=len(labels) + 2, column=0, columnspan=2, sticky="nsew")
        frame.rowconfigure(len(labels) + 2, weight=1)
        frame.columnconfigure(1, weight=1)
        return frame

    def _build_number_tab(self, parent: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(parent, padding=18, style="Card.TFrame")
        ttk.Label(
            frame,
            text="Теория чисел: наибольший общий делитель, наименьшее общее кратное и проверка на простоту",
            style="Section.TLabel",
            wraplength=880,
        ).grid(row=0, column=0, columnspan=2, sticky="w")
        ttk.Label(
            frame,
            text="НОД означает наибольший общий делитель, а НОК означает наименьшее общее кратное.",
            wraplength=880,
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(8, 10))

        self.number_a_var = tk.StringVar(value="24")
        self.number_b_var = tk.StringVar(value="36")

        ttk.Label(frame, text="Первое число:").grid(row=2, column=0, sticky="e", padx=(0, 8), pady=8)
        ttk.Entry(frame, textvariable=self.number_a_var, width=24).grid(row=2, column=1, sticky="w", pady=8)
        ttk.Label(frame, text="Второе число:").grid(row=3, column=0, sticky="e", padx=(0, 8), pady=8)
        ttk.Entry(frame, textvariable=self.number_b_var, width=24).grid(row=3, column=1, sticky="w", pady=8)

        ttk.Button(frame, text="Рассчитать", style="Accent.TButton", command=self._calculate_number_theory).grid(
            row=4, column=0, columnspan=2, sticky="w", pady=10
        )

        self.number_output = tk.Text(
            frame, width=60, height=12, bg="#f8fbff", fg="#1f2a44", relief="flat", font=("Consolas", 11)
        )
        self.number_output.grid(row=5, column=0, columnspan=2, sticky="nsew")
        frame.rowconfigure(5, weight=1)
        frame.columnconfigure(1, weight=1)
        return frame

    def _build_geometry_tab(self, parent: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(parent, padding=18, style="Card.TFrame")
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Геометрические вычисления", style="Section.TLabel").grid(
            row=0, column=0, columnspan=4, sticky="w"
        )

        self.circle_radius_var = tk.StringVar(value="5")
        self.rect_width_var = tk.StringVar(value="8")
        self.rect_height_var = tk.StringVar(value="3")

        ttk.Label(frame, text="Радиус круга:").grid(row=1, column=0, sticky="e", padx=(0, 8), pady=8)
        ttk.Entry(frame, textvariable=self.circle_radius_var, width=18).grid(row=1, column=1, sticky="w", pady=8)
        ttk.Button(frame, text="Круг", style="Accent.TButton", command=self._calculate_circle).grid(row=1, column=2, padx=12)

        ttk.Label(frame, text="Ширина прямоугольника:").grid(row=2, column=0, sticky="e", padx=(0, 8), pady=8)
        ttk.Entry(frame, textvariable=self.rect_width_var, width=18).grid(row=2, column=1, sticky="w", pady=8)
        ttk.Label(frame, text="Высота:").grid(row=2, column=2, sticky="e", padx=(8, 8), pady=8)
        ttk.Entry(frame, textvariable=self.rect_height_var, width=18).grid(row=2, column=3, sticky="w", pady=8)
        ttk.Button(frame, text="Прямоугольник", style="Accent.TButton", command=self._calculate_rectangle).grid(
            row=3, column=0, columnspan=2, sticky="w", pady=10
        )

        self.geometry_output = tk.Text(
            frame, width=70, height=12, bg="#f8fbff", fg="#1f2a44", relief="flat", font=("Consolas", 11)
        )
        self.geometry_output.grid(row=4, column=0, columnspan=4, sticky="nsew")
        frame.rowconfigure(4, weight=1)
        return frame

    def _build_plot_tab(self, parent: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(parent, padding=18, style="Card.TFrame")
        controls = ttk.Frame(frame, style="Card.TFrame")
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
        ttk.Button(controls, text="Построить график", style="Accent.TButton", command=self._draw_plot).grid(row=0, column=6)

        self.plot_canvas = tk.Canvas(frame, bg="#fbfdff", height=460, highlightthickness=1, highlightbackground="#b8c7d9")
        self.plot_canvas.pack(fill="both", expand=True, pady=(16, 0))
        self.plot_canvas.bind("<Configure>", lambda _event: self._draw_plot())
        return frame

    def _calculate_expression(self) -> None:
        try:
            result = self.evaluator.evaluate(self.expression_var.get())
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Ошибка вычисления", str(exc))
            return

        self.calculator_output.delete("1.0", tk.END)
        self.calculator_output.insert(
            tk.END,
            f"Выражение: {self.expression_var.get()}\nРезультат: {result}\n\n"
            "Проект использует модуль math и безопасный разбор AST, чтобы не выполнять произвольный код.",
        )

    def _insert_expression_token(self, token: str) -> None:
        current = self.expression_var.get().rstrip()
        separator = "" if not current or current.endswith(("(", " ", "+", "-", "*", "/", "%", ",")) else " "
        self.expression_var.set(f"{current}{separator}{token}")

    def _solve_quadratic(self) -> None:
        try:
            result = self.quadratic_solver.solve(float(self.a_var.get()), float(self.b_var.get()), float(self.c_var.get()))
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Ошибка решения", str(exc))
            return

        self.quadratic_result.delete("1.0", tk.END)
        self.quadratic_result.insert(
            tk.END,
            f"Дискриминант: {result.discriminant}\n"
            f"x1 = {result.root1}\n"
            f"x2 = {result.root2}\n\n"
            "При отрицательном дискриминанте приложение выводит комплексные корни.",
        )

    def _calculate_statistics(self) -> None:
        try:
            summary = self.statistics_service.summarize(self.stats_var.get())
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Ошибка статистики", str(exc))
            return

        self.stats_output.delete("1.0", tk.END)
        for key, value in summary.items():
            self.stats_output.insert(tk.END, f"{key}: {value}\n")

    def _calculate_finance(self) -> None:
        try:
            amount = self.finance_math.compound_interest(*(variable.get() for variable in self.finance_vars))
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Ошибка расчета", str(exc))
            return

        self.finance_output.delete("1.0", tk.END)
        self.finance_output.insert(
            tk.END,
            f"Итоговая сумма: {amount}\n\n"
            "Модуль decimal помогает избежать типичных ошибок округления при финансовых вычислениях.",
        )

    def _calculate_number_theory(self) -> None:
        try:
            result = self.number_theory_service.analyze(self.number_a_var.get(), self.number_b_var.get())
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Ошибка теории чисел", str(exc))
            return

        self.number_output.delete("1.0", tk.END)
        self.number_output.insert(
            tk.END,
            f"a = {result['a']}\n"
            f"b = {result['b']}\n"
            f"Наибольший общий делитель (НОД): {result['gcd']}\n"
            f"Наименьшее общее кратное (НОК): {result['lcm']}\n"
            f"a простое: {'да' if result['a_is_prime'] else 'нет'}\n"
            f"b простое: {'да' if result['b_is_prime'] else 'нет'}\n",
        )

    def _calculate_circle(self) -> None:
        try:
            result = self.geometry_service.circle(self.circle_radius_var.get())
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Ошибка геометрии", str(exc))
            return

        self.geometry_output.delete("1.0", tk.END)
        self.geometry_output.insert(
            tk.END,
            f"Круг\n"
            f"Радиус: {result['radius']:.4f}\n"
            f"Диаметр: {result['diameter']:.4f}\n"
            f"Длина окружности: {result['circumference']:.4f}\n"
            f"Площадь: {result['area']:.4f}\n",
        )

    def _calculate_rectangle(self) -> None:
        try:
            result = self.geometry_service.rectangle(self.rect_width_var.get(), self.rect_height_var.get())
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Ошибка геометрии", str(exc))
            return

        self.geometry_output.delete("1.0", tk.END)
        self.geometry_output.insert(
            tk.END,
            f"Прямоугольник\n"
            f"Ширина: {result['width']:.4f}\n"
            f"Высота: {result['height']:.4f}\n"
            f"Периметр: {result['perimeter']:.4f}\n"
            f"Площадь: {result['area']:.4f}\n"
            f"Диагональ: {result['diagonal']:.4f}\n",
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

        canvas.create_rectangle(20, 20, width - 20, height - 20, outline="#d8e1ea", fill="#ffffff")

        if zero_x is not None:
            canvas.create_line(zero_x, 20, zero_x, height - 20, fill="#b0bccc", dash=(4, 4))
        if zero_y is not None:
            canvas.create_line(20, zero_y, width - 20, zero_y, fill="#b0bccc", dash=(4, 4))

        points: list[float] = []
        for x_value, y_value in samples:
            points.extend((map_x(x_value), map_y(y_value)))
        canvas.create_line(*points, fill="#2f6fed", width=3, smooth=True)

        canvas.create_text(80, 30, text=f"y = {self.plot_expression_var.get()}", anchor="w", font=("Segoe UI", 11, "bold"))
        canvas.create_text(80, height - 22, text=f"x in [{x_min:.2f}; {x_max:.2f}], y in [{y_min:.2f}; {y_max:.2f}]", anchor="w")


if __name__ == "__main__":
    app = MathModulesApp()
    app.mainloop()
