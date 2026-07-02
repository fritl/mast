from .tokens import Token
from .tokens import TokenType as TT
from .ast_nodes import Expr, Num, Var, BinaryOp, Equation, UnaryOp, Power


class RDParser:
    """Recursive descent parser"""

    def __init__(self, tokens: list[Token]):
        self.tokens: list[Token] = tokens
        self.pos: int = 0

    def __consume(self, token_type: TT) -> Token:
        next_token = self.__peek()
        if next_token.tokentype is not token_type:
            raise SyntaxError(
                f"Parsing error at token {self.pos + 1}. Expected token {token_type} found {next_token.tokentype}"
            )
        self.pos += 1
        return next_token

    def __peek(self) -> Token:
        return self.tokens[self.pos]

    def parse(self) -> Equation | Expr:
        return self.__equation()

    def __equation(self) -> Equation | Expr:
        """Equation   = Expression, "=", Expression | Expression ;"""
        node = self.__expression()
        if self.__peek().tokentype is TT.EOF:
            return node
        self.__consume(TT.EQUAL)
        return Equation(node, self.__expression())

    def __expression(self) -> Expr:
        """Expression = Term, { ("+" | "-"), Term } ;"""
        node = self.__term()
        while self.__peek().tokentype in (TT.PLUS, TT.MINUS):
            op = "+" if self.__peek().tokentype == TT.PLUS else "-"
            self.__consume(self.__peek().tokentype)
            # left associative
            node = BinaryOp(op, node, self.__term())
        return node

    def __term(self) -> Expr:
        """Term = Factor, { ("*" | "/"), Factor } ;"""
        node = self.__factor()
        while self.__peek().tokentype in (TT.DIV, TT.MUL):
            op = "*" if self.__peek().tokentype == TT.MUL else "/"
            self.__consume(self.__peek().tokentype)
            # left associative
            node = BinaryOp(op, node, self.__factor())
        return node

    def __factor(self) -> Expr:
        """Factor = Base, [ "^", Factor ] ;"""
        node = self.__base()
        if self.__peek().tokentype == TT.POW:
            self.__consume(TT.POW)
            node = Power(node, self.__factor())
        return node

    def __base(self) -> Expr:
        """
        Base = "-", Base
             | "+", Base
             | "(", Expression, ")"
             | Number
             | Variable ;
               "^", Factor ] ;
        """
        next_token = self.__peek()
        match next_token.tokentype:
            case TT.MINUS:
                self.__consume(TT.MINUS)
                return UnaryOp("-", self.__base())

            case TT.PLUS:
                self.__consume(TT.PLUS)
                return UnaryOp("+", self.__base())

            case TT.LPAREN:
                self.__consume(TT.LPAREN)
                node = self.__expression()
                self.__consume(TT.RPAREN)
                return node

            case TT.NUM:
                self.__consume(TT.NUM)
                if next_token.value is None:
                    raise RuntimeError("Value of number token is None")
                if isinstance(next_token.value, str):
                    raise RuntimeError(
                        f"Malformed token stream. Value of Num token should be float found str '{next_token.value}'"
                    )
                return Num(next_token.value)

            case TT.IDENTIFIER:
                self.__consume(TT.IDENTIFIER)
                if next_token.value is None:
                    raise RuntimeError("Value of variable token is None")
                if isinstance(next_token.value, float):
                    raise RuntimeError(
                        f"Malformed token stream. Value of Num token should be str found float '{next_token.value}'"
                    )
                if isinstance(next_token.value, int):
                    raise RuntimeError(
                        f"Malformed token stream. Value of Num token should be str found int '{next_token.value}'"
                    )

                return Var(next_token.value)

        raise RuntimeError(f"Unexpected Token {next_token.tokentype}")
