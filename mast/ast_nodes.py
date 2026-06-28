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


@dataclass
class UnaryOp:
    operator: Literal["-", "+"]
    operand: Expr

    def __str__(self):
        return f"({self.operator}{self.operand})"

    @property
    def label(self) -> str:
        return self.operator


@dataclass
class Num:
    value: float

    def __str__(self):
        return f"{self.value}"

    @property
    def label(self) -> str:
        return f"{self.value}"


@dataclass
class Var:
    name: str

    def __str__(self):
        return self.name

    @property
    def label(self) -> str:
        return self.name
