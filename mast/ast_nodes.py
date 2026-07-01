from typing import Literal, Self
from dataclasses import dataclass

type Expr = BinaryOp | UnaryOp | Num | Var


@dataclass
class Equation:
    left: Expr
    right: Expr
    label: str = "="

    def __str__(self):
        return f"{self.left} = {self.right}"

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


@dataclass
class UnaryOp:
    operator: Literal["-", "+"]
    operand: Expr

    def __str__(self):
        return f"({self.operator}{self.operand})"

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


@dataclass
class Num:
    value: float

    def __str__(self):
        return f"{self.value}"

    @property
    def label(self) -> str:
        return f"{self.value}"

    def eval(self, _: dict[str, float]):
        return self.value

    def simplify(self) -> Self:
        return self


@dataclass
class Var:
    name: str

    def __str__(self):
        return self.name

    @property
    def label(self) -> str:
        return self.name

    def eval(self, env: dict[str, float]):
        return env[self.name]

    def simplify(self) -> Self:
        return self
