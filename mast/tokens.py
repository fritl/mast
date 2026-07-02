from enum import Enum, auto
from dataclasses import dataclass


class TokenType(Enum):
    """Token types the lexer can output"""

    # Number and Identifier
    NUM = auto()
    IDENTIFIER = auto()

    # Basic operations
    PLUS = auto()
    MINUS = auto()
    DIV = auto()
    MUL = auto()
    POW = auto()

    EQUAL = auto()

    # Parenthesis
    LPAREN = auto()
    RPAREN = auto()

    EOF = auto()


@dataclass(frozen=True)
class Token:
    """One token output by the lexer

    Attributes:
        tokentype: The type of the token
        value: Optional value. Can be string (for future use) or float (for numbers)
    """

    tokentype: TokenType
    value: str | float | None = None
