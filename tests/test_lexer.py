from src.mast.lexer import tokenize
from src.mast.tokens import TokenType as TT, Token
import pytest


@pytest.mark.parametrize(
    ["expression", "type", "value"],
    [
        ("+", TT.PLUS, None),
        ("-", TT.MINUS, None),
        ("*", TT.MUL, None),
        ("/", TT.DIV, None),
        ("=", TT.EQUAL, None),
        ("(", TT.LPAREN, None),
        (")", TT.RPAREN, None),
        ("x", TT.VAR, "x"),
        ("hallowelt", TT.VAR, "hallowelt"),
    ],
)
def test_single_tokens(expression: str, type: TT, value: str | float | None):
    tokens: list[Token] = tokenize(expression)
    assert len(tokens) == 1
    first_token = tokens[0]
    assert first_token.tokentype == type
    assert first_token.value == value


@pytest.mark.parametrize(
    ["expression", "value"],
    [
        ("100", 100),
        ("3", 3),
        (".14", 0.14),
        ("3.", 3),
    ],
)
def test_numbers(expression: str, value: str | float | None):
    tokens: list[Token] = tokenize(expression)
    assert len(tokens) == 1
    first_token = tokens[0]
    assert first_token.tokentype == TT.NUM
    assert first_token.value == pytest.approx(value)


def test_equation():
    tokens: list[Token] = tokenize("3x + 12 = 10")
    expected_tokens: list[Token] = [
        Token(TT.NUM, 3),
        Token(TT.VAR, "x"),
        Token(TT.PLUS),
        Token(TT.NUM, 12),
        Token(TT.EQUAL),
        Token(TT.NUM, 10),
    ]
    assert tokens == expected_tokens


def test_additional_whitespace():
    tokens: list[Token] = tokenize("    3+    12    ")
    expected_tokens: list[Token] = [
        Token(TT.NUM, 3),
        Token(TT.PLUS),
        Token(TT.NUM, 12),
    ]
    assert tokens == expected_tokens


def test_empty_strings_returning_empty_list():
    tokens: list[Token] = tokenize("")
    assert tokens == []
    tokens: list[Token] = tokenize(" ")
    assert tokens == []
    tokens: list[Token] = tokenize("     ")
    assert tokens == []


@pytest.mark.parametrize(
    ["expression", "position"],
    [("3x + 12 \\", 8), ("_", 0), ("))(()*+%", 7), ("                _", 16)],
)
def test_unknown_symbol(expression: str, position: int):
    with pytest.raises(
        SyntaxError, match=f"Unknown token found at position {position}"
    ):
        tokenize(expression)
