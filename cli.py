from math import e, pi
from mast.analysis import collect_vars
from mast.ast_nodes import (
    Equation,
    Expr,
)
from mast.parser import RDParser
from mast.lexer import tokenize
from rich import print
from rich.console import Console


def parse_float(s: str) -> float | None:
    try:
        return float(s)
    except ValueError:
        return None


def main():
    console = Console()
    print("[#f18825]Mathematical Abstract Syntax Tree")
    mathematical_string = console.input(
        "[grey66]Input your mathematical equation or expression: "
    )
    tokens = tokenize(mathematical_string)
    # print("Mathematical string after processing:")
    ast: Equation | Expr = RDParser(tokens).parse()
    ast = ast.simplify()
    if isinstance(ast, Equation):
        print("[red]Cannot diff equation")
        return
    ast = ast.differentiate()
    ast = ast.simplify()
    print(f"[grey66]Derivative:[default] {ast}")
    print(f"[grey66]LaTeX:[default] {ast.latex()}")
    variables = collect_vars(ast)
    variable_env: dict[str, float] = {"e": e, "pi": pi}
    variables -= {"e", "pi"}
    if len(variables) > 0:
        print("[grey66]Input variable values:")
        for v in sorted(variables):
            value = parse_float(console.input(f"[grey66]{v}: "))
            while value is None:
                value = parse_float(console.input(f"[grey66]{v}: "))
            variable_env[v] = value
    # draw(mathematical_string, ast)
    print(f"[grey66]Result:[default] {ast.eval(variable_env)}")


if __name__ == "__main__":
    main()
