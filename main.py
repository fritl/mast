from mast.ast_nodes import Equation, Expr, BinaryOp, UnaryOp, Var, Num
from mast.parser import RDParser
from mast.lexer import tokenize
import pygraphviz as pgv


def main():
    print("Mathematical Abstract Syntax Tree")
    mathematical_string = input("Input your mathematical equation or expression: ")
    tokens = tokenize(mathematical_string)
    print("Mathematical string after processing:")
    ast: Equation | Expr = RDParser(tokens).parse()
    print(ast)
    draw(mathematical_string, ast)


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
