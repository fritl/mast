import pytest
from mast.tokens import Token, TokenType as TT
from mast.parser import RDParser
from mast.ast_nodes import Num, Var, BinaryOp, UnaryOp, Equation


def t(*args) -> list[Token]:
    """Hilfsfunktion: baut Token-Listen, EOF wird automatisch angehängt."""
    result = []
    for arg in args:
        if isinstance(arg, tuple):
            tt, value = arg
            result.append(Token(tt, value))
        else:
            result.append(Token(arg))
    result.append(Token(TT.EOF))
    return result


def parse(tokens: list[Token]):
    return RDParser(tokens).parse()


class TestBasicExpressions:
    def test_single_number(self):
        assert parse(t((TT.NUM, 3.0))) == Num(3.0)

    def test_single_variable(self):
        assert parse(t((TT.IDENTIFIER, "x"))) == Var("x")

    def test_addition(self):
        result = parse(t((TT.NUM, 3.0), TT.PLUS, (TT.IDENTIFIER, "x")))
        assert result == BinaryOp("+", Num(3.0), Var("x"))

    def test_subtraction(self):
        result = parse(t((TT.IDENTIFIER, "x"), TT.MINUS, (TT.NUM, 2.0)))
        assert result == BinaryOp("-", Var("x"), Num(2.0))

    def test_multiplication(self):
        result = parse(t((TT.NUM, 3.0), TT.MUL, (TT.IDENTIFIER, "x")))
        assert result == BinaryOp("*", Num(3.0), Var("x"))

    def test_division(self):
        result = parse(t((TT.IDENTIFIER, "x"), TT.DIV, (TT.NUM, 2.0)))
        assert result == BinaryOp("/", Var("x"), Num(2.0))


class TestPrecedence:
    def test_mul_binds_tighter_than_add(self):
        # 3 + 2 * x  →  3 + (2*x)
        result = parse(
            t((TT.NUM, 3.0), TT.PLUS, (TT.NUM, 2.0), TT.MUL, (TT.IDENTIFIER, "x"))
        )
        assert result == BinaryOp("+", Num(3.0), BinaryOp("*", Num(2.0), Var("x")))

    def test_div_binds_tighter_than_sub(self):
        # x - 6 / 2  →  x - (6/2)
        result = parse(
            t((TT.IDENTIFIER, "x"), TT.MINUS, (TT.NUM, 6.0), TT.DIV, (TT.NUM, 2.0))
        )
        assert result == BinaryOp("-", Var("x"), BinaryOp("/", Num(6.0), Num(2.0)))

    def test_parens_override_precedence(self):
        # (3 + 2) * x
        result = parse(
            t(
                TT.LPAREN,
                (TT.NUM, 3.0),
                TT.PLUS,
                (TT.NUM, 2.0),
                TT.RPAREN,
                TT.MUL,
                (TT.IDENTIFIER, "x"),
            )
        )
        assert result == BinaryOp("*", BinaryOp("+", Num(3.0), Num(2.0)), Var("x"))


class TestAssociativity:
    def test_subtraction_is_left_associative(self):
        # 3 - 2 - 1  →  (3-2)-1
        result = parse(
            t((TT.NUM, 3.0), TT.MINUS, (TT.NUM, 2.0), TT.MINUS, (TT.NUM, 1.0))
        )
        assert result == BinaryOp("-", BinaryOp("-", Num(3.0), Num(2.0)), Num(1.0))

    def test_division_is_left_associative(self):
        # 8 / 4 / 2  →  (8/4)/2
        result = parse(t((TT.NUM, 8.0), TT.DIV, (TT.NUM, 4.0), TT.DIV, (TT.NUM, 2.0)))
        assert result == BinaryOp("/", BinaryOp("/", Num(8.0), Num(4.0)), Num(2.0))


class TestUnaryOperators:
    def test_unary_minus(self):
        assert parse(t(TT.MINUS, (TT.IDENTIFIER, "x"))) == UnaryOp("-", Var("x"))

    def test_unary_plus(self):
        assert parse(t(TT.PLUS, (TT.IDENTIFIER, "x"))) == UnaryOp("+", Var("x"))

    def test_double_unary_minus(self):
        # --x
        result = parse(t(TT.MINUS, TT.MINUS, (TT.IDENTIFIER, "x")))
        assert result == UnaryOp("-", UnaryOp("-", Var("x")))

    def test_unary_minus_in_expression(self):
        # 3 + -x
        result = parse(t((TT.NUM, 3.0), TT.PLUS, TT.MINUS, (TT.IDENTIFIER, "x")))
        assert result == BinaryOp("+", Num(3.0), UnaryOp("-", Var("x")))


class TestParentheses:
    def test_simple_parens(self):
        result = parse(t(TT.LPAREN, (TT.IDENTIFIER, "x"), TT.RPAREN))
        assert result == Var("x")

    def test_nested_parens(self):
        result = parse(
            t(TT.LPAREN, TT.LPAREN, (TT.IDENTIFIER, "x"), TT.RPAREN, TT.RPAREN)
        )
        assert result == Var("x")

    def test_complex_nesting(self):
        # 3 * (x + (y - 1))
        result = parse(
            t(
                (TT.NUM, 3.0),
                TT.MUL,
                TT.LPAREN,
                (TT.IDENTIFIER, "x"),
                TT.PLUS,
                TT.LPAREN,
                (TT.IDENTIFIER, "y"),
                TT.MINUS,
                (TT.NUM, 1.0),
                TT.RPAREN,
                TT.RPAREN,
            )
        )
        assert result == BinaryOp(
            "*",
            Num(3.0),
            BinaryOp("+", Var("x"), BinaryOp("-", Var("y"), Num(1.0))),
        )


class TestEquations:
    def test_simple_equation(self):
        result = parse(t((TT.IDENTIFIER, "x"), TT.EQUAL, (TT.NUM, 3.0)))
        assert result == Equation(Var("x"), Num(3.0))

    def test_equation_with_expressions_on_both_sides(self):
        # 3*x + 1 = 2*x + 5
        result = parse(
            t(
                (TT.NUM, 3.0),
                TT.MUL,
                (TT.IDENTIFIER, "x"),
                TT.PLUS,
                (TT.NUM, 1.0),
                TT.EQUAL,
                (TT.NUM, 2.0),
                TT.MUL,
                (TT.IDENTIFIER, "x"),
                TT.PLUS,
                (TT.NUM, 5.0),
            )
        )
        assert result == Equation(
            BinaryOp("+", BinaryOp("*", Num(3.0), Var("x")), Num(1.0)),
            BinaryOp("+", BinaryOp("*", Num(2.0), Var("x")), Num(5.0)),
        )

    def test_expression_without_eq_is_not_equation(self):
        result = parse(t((TT.NUM, 3.0), TT.PLUS, (TT.IDENTIFIER, "x")))
        assert not isinstance(result, Equation)


class TestErrors:
    def test_unmatched_lparen_raises(self):
        with pytest.raises(SyntaxError):
            parse(t(TT.LPAREN, (TT.NUM, 3.0)))

    def test_unexpected_token_raises(self):
        with pytest.raises(RuntimeError):
            parse(t(TT.PLUS_PLUS) if hasattr(TT, "PLUS_PLUS") else t(TT.MUL))

    def test_dangling_operator_raises(self):
        with pytest.raises(RuntimeError):
            parse(t(TT.MUL))
