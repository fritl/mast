from mast.analysis import collect_vars
from mast.ast_nodes import Equation, Expr, BinaryOp, UnaryOp, Var, Num
from mast.parser import RDParser
from mast.lexer import tokenize
from rich import print
from rich.console import Console
import pygraphviz as pgv


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
    print(f"[grey66]Simplified:[default] {ast}")
    variables = collect_vars(ast)
    variable_env: dict[str, float] = {}
    if len(variables) > 0:
        print("[grey66]Input variable values:")
        for v in sorted(variables):
            value = parse_float(console.input(f"[grey66]{v}: "))
            while value is None:
                value = parse_float(console.input(f"[grey66]{v}: "))
            variable_env[v] = value
    # draw(mathematical_string, ast)
    print(f"[grey66]Result:[default] {ast.eval(variable_env)}")


def add_node(cur_node_id: str | None, graph: pgv.AGraph, node: Expr | Equation):
    nid = str(id(node))

    match node:
        case BinaryOp(_, left, right):
            graph.add_node(nid, label=node.label)
            add_node(nid, graph, left)
            add_node(nid, graph, right)

        case UnaryOp(_, operand):
            graph.add_node(nid, label=node.label)
            add_node(nid, graph, operand)

        case Equation(left, right):
            graph.add_node(nid, label=node.label)
            add_node(nid, graph, left)
            add_node(nid, graph, right)

        case Num():
            graph.add_node(nid, label=node.label)

        case Var():
            graph.add_node(nid, label=node.label)

    if cur_node_id is not None:
        graph.add_edge(cur_node_id, nid)


def draw(label: str, ast: Expr | Equation):
    graph = pgv.AGraph(
        directed=True,
        label=f"<<B>{label}</B>>",
        labelloc="t",
        labeljust="c",
        fontsize="20",
    )
    add_node(None, graph, ast)
    graph.draw(f"./{label}.png", prog="dot")


if __name__ == "__main__":
    main()
