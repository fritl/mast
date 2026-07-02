from .tokens import TokenType, Token


def tokenize(math_expr: str) -> list[Token]:
    """Deconstruct a mathematical expression into a list of tokens

    Args:
        math_expr: The mathematical expression. e.g. 3+2 = 5, 4.3+5 = 12, ))(4x/100)

    Returns: List of tokens


    Raises:
        RuntimeError: If a unknown token is found
    """
    token_stream: list[Token] = []
    i = 0
    while i < len(math_expr):
        if math_expr[i].isspace():
            i += 1
        elif math_expr[i].isdigit() or math_expr[i] == ".":
            j = i + 1
            while j < len(math_expr) and (
                math_expr[j].isdigit() or math_expr[j] == "."
            ):
                j += 1

            token_stream.append(Token(TokenType.NUM, float(math_expr[i:j])))
            i = j

        elif math_expr[i].isalpha():
            j = i + 1
            while j < len(math_expr) and math_expr[j].isalpha():
                j += 1
            token_stream.append(Token(TokenType.IDENTIFIER, math_expr[i:j]))
            i = j
        else:
            token_map = {
                "+": TokenType.PLUS,
                "-": TokenType.MINUS,
                "*": TokenType.MUL,
                "/": TokenType.DIV,
                "(": TokenType.LPAREN,
                ")": TokenType.RPAREN,
                "=": TokenType.EQUAL,
                "^": TokenType.POW,
            }

            if math_expr[i] not in token_map.keys():
                raise SyntaxError(f"Unknown token found at position {i}")

            token_type = token_map[math_expr[i]]
            token_stream.append(Token(token_type))
            i += 1

    token_stream.append(Token(TokenType.EOF))
    return token_stream
