from mast.ast_nodes import Expr, Equation, BinaryOp, UnaryOp, Var


def collect_vars(node: Expr | Equation) -> set[str]:

    match node:
        case Equation(left, right):
            return collect_vars(left) | collect_vars(right)

        case BinaryOp(_, left, right):
            return collect_vars(left) | collect_vars(right)

        case UnaryOp(_, operand):
            return collect_vars(operand)

        case Var(name):
            return {name}

    return set()
