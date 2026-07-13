from mast.ast_nodes import (
    Equation,
    Expr,
    BinaryOp,
    UnaryOp,
    Power,
    FunctionCall,
    Num,
    Var,
)
import pygraphviz as pgv


def draw(label: str, ast: Expr | Equation) -> bytes:
    graph = pgv.AGraph(
        directed=True,
        # label=f"<<B>{label}</B>>",
        fontcolor="black",
        fontname="JetBrains Mono",
        labelloc="t",
        labeljust="c",
        fontsize="20",
        bgcolor="transparent",
    )
    add_node(None, graph, ast)
    return graph.draw(prog="dot", format="svg")


def add_node(cur_node_id: str | None, graph: pgv.AGraph, node: Expr | Equation):
    nid = str(id(node))
    if isinstance(node, Equation):
        fg_color = "#7a2aff"
        font_color = "white"
    elif isinstance(node, Var | Num):
        fg_color = "#00ccff"
        font_color = "#0b132b"
    else:
        fg_color = "#ff6600"
        font_color = "white"
    style = {
        "fontname": "JetBrains Mono",
        "fontsize": "14",
        "fillcolor": fg_color,
        "style": "filled",
        "color": "white",
        "fontcolor": font_color,
        # "shape": "circle",
        # "width": ".7",
        # "fixedsize": True,
    }

    match node:
        case BinaryOp(_, left, right):
            graph.add_node(nid, label=node.label, **style)
            add_node(nid, graph, left)
            add_node(nid, graph, right)

        case UnaryOp(_, operand):
            graph.add_node(nid, label=node.label, **style)
            add_node(nid, graph, operand)

        case Equation(left, right):
            graph.add_node(nid, label=node.label, **style)
            add_node(nid, graph, left)
            add_node(nid, graph, right)

        case Power(base, exponent):
            graph.add_node(nid, label=node.label, **style)
            add_node(nid, graph, base)
            add_node(nid, graph, exponent)

        case FunctionCall(_, parameter):
            graph.add_node(nid, label=node.label, **style)

            add_node(nid, graph, parameter)

        case Num():
            graph.add_node(nid, label=node.label, **style)

        case Var():
            graph.add_node(nid, label=node.label, **style)

    if cur_node_id is not None:
        graph.add_edge(cur_node_id, nid)
