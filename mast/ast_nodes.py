from math import sin, cos, tan, log, sqrt, log10
from typing import Literal, Self
from dataclasses import dataclass

type Expr = BinaryOp | UnaryOp | Num | Var | Power | FunctionCall


@dataclass
class Equation:
    left: Expr
    right: Expr
    label: str = "="

    def __str__(self):
        return f"{self.left} = {self.right}"

    def latex(self) -> str:
        return f"{self.left.latex()} = {self.right.latex()}"

    def eval(self, env: dict[str, float]) -> bool:
        left = self.left.eval(env)
        right = self.right.eval(env)
        if left == right:
            return True
        return False

    def simplify(self) -> Self:
        self.left = self.left.simplify()
        self.right = self.left.simplify()
        return self

    def contains_var(self, var: str) -> bool:
        return self.left.contains_var(var) or self.right.contains_var(var)


def is_zero(node):
    return isinstance(node, Num) and node.value == 0


def is_one(node):
    return isinstance(node, Num) and node.value == 1


def equal(node_a, node_b):
    if type(node_a) is not type(node_b):
        return False

    if isinstance(node_a, Num):
        return node_a.value == node_b.value

    if isinstance(node_a, Var):
        return node_a.name == node_b.name

    if isinstance(node_a, UnaryOp):
        return node_a.operator == node_b.operator and equal(
            node_a.operand, node_b.operand
        )

    if isinstance(node_a, BinaryOp):
        return (
            (node_a.operator == node_b.operator)
            and equal(node_a.left, node_b.left)
            and equal(node_a.right, node_b.right)
        )

    if isinstance(node_a, Power):
        return equal(node_a.base, node_b.base) and equal(
            node_a.exponent, node_b.exponent
        )


@dataclass
class Power:
    base: Expr
    exponent: Expr

    label: str = "^"

    def __str__(self):
        return f"({self.base}^{self.exponent})"

    def latex(self) -> str:
        if isinstance(self.base, BinaryOp | Power):
            return f"\\left({self.base.latex()}\\right)^{{{self.exponent.latex()}}}"
        return f"{self.base.latex()}^{{{self.exponent.latex()}}}"

    def eval(self, env: dict[str, float]) -> float:
        base = self.base.eval(env)
        exponent = self.exponent.eval(env)
        return base**exponent

    def simplify(self) -> Expr:
        self.base = self.base.simplify()
        self.exponent = self.exponent.simplify()
        if is_zero(self.exponent):
            return Num(1)
        if is_zero(self.base):
            return Num(0)
        if is_one(self.base):
            return Num(1)
        if is_one(self.exponent):
            return self.base

        if isinstance(self.base, Num) and isinstance(self.exponent, Num):
            return Num(self.base.value**self.exponent.value)
        return self

    def contains_var(self, var: str) -> bool:
        return self.base.contains_var(var) or self.exponent.contains_var(var)

    def differentiate(self, wrt: str = "x") -> Expr:
        # x^2x = e^(2x*ln(x))
        if self.base.contains_var(wrt) and self.exponent.contains_var(wrt):
            return Power(
                Var("e"), BinaryOp("*", self.exponent, FunctionCall("ln", self.base))
            ).differentiate(wrt)

        if self.base.contains_var(wrt):
            return BinaryOp(
                "*",
                self.exponent,
                Power(self.base, BinaryOp("-", self.exponent, Num(1))),
            )

        if self.base == Var("e"):
            return BinaryOp(
                "*",
                self.exponent.differentiate(wrt),
                Power(self.base, self.exponent),
            )

        else:
            return BinaryOp(
                "*",
                self.exponent.differentiate(wrt),
                BinaryOp(
                    "*",
                    Power(self.base, self.exponent),
                    FunctionCall("ln", self.base),
                ),
            )


@dataclass
class BinaryOp:
    operator: Literal["+", "-", "*", "/"]
    left: Expr
    right: Expr

    @property
    def label(self) -> str:
        return self.operator

    def __str__(self):
        return f"({self.left} {self.operator} {self.right})"

    def latex(self) -> str:
        if self.operator == "/":
            return f"\\frac{{{self.left.latex()}}}{{{self.right.latex()}}}"
        return f"{self.left.latex()}{self.operator}{self.right.latex()}"

    def eval(self, env: dict[str, float]) -> float:
        left = self.left.eval(env)
        right = self.right.eval(env)
        match self.operator:
            case "+":
                return left + right
            case "-":
                return left - right
            case "*":
                return left * right
            case "/":
                return left / right

    def __simplify_add(self):
        if is_zero(self.left):
            return self.right
        if is_zero(self.right):
            return self.left

        if isinstance(self.left, Num) and isinstance(self.right, Num):
            return Num(self.left.value + self.right.value)

        if equal(self.left, self.right):
            return BinaryOp("*", Num(2), self.left)

        return self

    def __simplify_sub(self):
        if is_zero(self.left):
            return UnaryOp("-", self.right)
        if is_zero(self.right):
            return self.left

        if isinstance(self.left, Num) and isinstance(self.right, Num):
            return Num(self.left.value - self.right.value)

        if equal(self.left, self.right):
            return Num(0)

        return self

    def __simplify_mul(self):
        if is_zero(self.left) or is_zero(self.right):
            return Num(0)

        if is_one(self.left):
            return self.right
        if is_one(self.right):
            return self.left

        if isinstance(self.left, Num) and isinstance(self.right, Num):
            return Num(self.left.value * self.right.value)

        if equal(self.left, self.right):
            return Power(self.left, Num(2))

        return self

    def __simplify_div(self):
        if is_zero(self.left) and not is_zero(self.right):
            return Num(0)

        if is_one(self.right):
            return self.left

        if equal(self.left, self.right) and not is_zero(self.right):
            return Num(1)

        if (
            isinstance(self.left, Num)
            and isinstance(self.right, Num)
            and not is_zero(self.right)
        ):
            return Num(self.left.value / self.right.value)

        return self

    def simplify(self) -> Self:
        self.left = self.left.simplify()
        self.right = self.right.simplify()
        match self.operator:
            case "+":
                return self.__simplify_add()
            case "-":
                return self.__simplify_sub()
            case "*":
                return self.__simplify_mul()
            case "/":
                return self.__simplify_div()

    def contains_var(self, var: str) -> bool:
        return self.left.contains_var(var) or self.right.contains_var(var)

    def __diff_add(self, wrt: str = "x") -> Expr:
        return BinaryOp(
            "+", self.left.differentiate(wrt), self.right.differentiate(wrt)
        )

    def __diff_sub(self, wrt: str = "x") -> Expr:
        return BinaryOp(
            "-", self.left.differentiate(wrt), self.right.differentiate(wrt)
        )

    def __diff_mul(self, wrt: str = "x") -> Expr:
        # 2*x
        if self.left.contains_var(wrt) and not self.right.contains_var(wrt):
            return BinaryOp("*", self.right, self.left.differentiate(wrt))
        # x*2
        if self.right.contains_var(wrt) and not self.left.contains_var(wrt):
            return BinaryOp("*", self.left, self.right.differentiate(wrt))

        return BinaryOp(
            "+",
            BinaryOp("*", self.left.differentiate(wrt), self.right),
            BinaryOp("*", self.left, self.right.differentiate()),
        )

    def __diff_div(self, wrt: str = "x") -> Expr:
        # x/(2+3) -> 1/(2+3) * x'
        if self.left.contains_var(wrt) and not self.right.contains_var(wrt):
            return BinaryOp(
                "*", BinaryOp("/", Num(1), self.right), self.right.differentiate()
            )
        return BinaryOp(
            "/",
            BinaryOp(
                "-",
                BinaryOp("*", self.left.differentiate(wrt), self.right),
                BinaryOp("*", self.left, self.right.differentiate()),
            ),
            Power(self.right, Num(2)),
        )

    def differentiate(self, wrt: str = "x") -> Expr:
        match self.operator:
            case "+":
                return self.__diff_add(wrt)
            case "-":
                return self.__diff_sub(wrt)
            case "*":
                return self.__diff_mul(wrt)
            case "/":
                return self.__diff_div(wrt)


@dataclass
class UnaryOp:
    operator: Literal["-", "+"]
    operand: Expr

    def __str__(self):
        return f"({self.operator}{self.operand})"

    def latex(self) -> str:
        if isinstance(self.operand, BinaryOp):
            return f"{self.operator}\\left({self.operand.latex()}\\right)"
        return f"{self.operator}{self.operand.latex()}"

    @property
    def label(self) -> str:
        return self.operator

    def eval(self, env: dict[str, float]):
        if self.operator == "-":
            return -self.operand.eval(env)
        return self.operand.eval(env)

    def simplify(self) -> Expr:
        self.operand = self.operand.simplify()
        if isinstance(self.operand, UnaryOp):
            if self.operand.operator == self.operator:
                return self.operand.operand
            return UnaryOp("-", self.operand.operand)
        if self.operator == "+":
            return self.operand
        return self

    def contains_var(self, var: str) -> bool:
        return self.operand.contains_var(var)

    def differentiate(self, wrt: str = "x") -> Expr:
        return UnaryOp(self.operator, self.operand.differentiate(wrt))


@dataclass
class FunctionCall:
    name: str
    parameter: Expr

    def __str__(self):
        return f"{self.name}({self.parameter})"

    def latex(self) -> str:
        # Sqrt has special syntax because LaTeX is bad.
        if self.name == "sqrt":
            return f"\\sqrt{{{self.parameter.latex()}}}"
        return f"\\{self.name}({self.parameter.latex()})"

    @property
    def label(self) -> str:
        return self.name

    def eval(self, env: dict[str, float]) -> float:
        parameter_value = self.parameter.eval(env)
        match self.name:
            case "sin":
                result = sin(parameter_value)
                return result
            case "cos":
                result = cos(parameter_value)
                return result
            case "tan":
                result = tan(parameter_value)
                return result
            case "ln":
                result = log(parameter_value)
                return result
            case "log":
                result = log10(parameter_value)
                return result
            case "sqrt":
                result = sqrt(parameter_value)
                return result
            case _:
                raise RuntimeError(f"Function {self.name} not found")

    def simplify(self) -> Expr:
        self.parameter = self.parameter.simplify()
        if isinstance(self.parameter, Num):
            return Num(self.eval({}))
        return self

    def contains_var(self, var: str) -> bool:
        return self.parameter.contains_var(var)

    def differentiate(self, wrt: str = "x") -> Expr:
        if not self.contains_var(wrt):
            return Num(0)

        inner_diff = self.parameter.differentiate(wrt)
        match self.name:
            case "sin":
                outer_diff = FunctionCall("cos", self.parameter)

            case "cos":
                outer_diff = UnaryOp("-", FunctionCall("sin", self.parameter))

            case "tan":
                outer_diff = BinaryOp(
                    "/", Num(1), Power(FunctionCall("cos", self.parameter), Num(2))
                )

            case "ln":
                outer_diff = BinaryOp("/", Num(1), self.parameter)

            case "log":
                outer_diff = BinaryOp(
                    "/",
                    Num(1),
                    BinaryOp("*", self.parameter, FunctionCall("ln", Num(10))),
                )

            case "sqrt":
                outer_diff = BinaryOp(
                    "/",
                    Num(1),
                    BinaryOp("*", Num(2), FunctionCall("sqrt", self.parameter)),
                )

            case _:
                raise RuntimeError(f"Can't differentiate unknown function {self.name}")

        return BinaryOp("*", inner_diff, outer_diff)


@dataclass
class Num:
    value: float

    def __str__(self):
        return f"{self.value}"

    def latex(self) -> str:
        return str(self.value)

    @property
    def label(self) -> str:
        return f"{self.value}"

    def eval(self, _: dict[str, float]):
        return self.value

    def simplify(self) -> Self:
        return self

    def contains_var(self, _: str) -> bool:
        return False

    def differentiate(self, _: str = "x") -> Expr:
        return Num(0)


@dataclass
class Var:
    name: str

    def __str__(self):
        return self.name

    def latex(self) -> str:
        if self.name in {"pi"}:
            return f"\\{self.name}"
        return self.name

    @property
    def label(self) -> str:
        return self.name

    def eval(self, env: dict[str, float]):
        return env[self.name]

    def simplify(self) -> Self:
        return self

    def contains_var(self, var: str) -> bool:
        return var == self.name

    def differentiate(self, wrt: str = "x") -> Expr:
        if wrt == self.name:
            return Num(1)
        return Num(0)
