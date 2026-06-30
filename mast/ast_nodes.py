from typing import Literal
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
