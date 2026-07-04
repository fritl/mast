from mast.draw import draw
from math import pi
import math
from mast.analysis import collect_vars
from pydantic import BaseModel
from mast.ast_nodes import Expr, Equation
from mast.tokens import Token
from mast.lexer import tokenize
from fastapi import APIRouter, HTTPException, Response
from mast.parser import RDParser

api_router = APIRouter()


class ExprRequest(BaseModel):
    expr: str


class EvaluationRequest(BaseModel):
    expr: str
    env: dict[str, float]


class DifferentationRequest(BaseModel):
    expr: str
    wrt: str = "x"


@api_router.post("/ast")
def api_ast(req: ExprRequest) -> Response:
    try:
        tokens: list[Token] = tokenize(req.expr)
        ast: Expr | Equation = RDParser(tokens).parse()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return Response(draw(req.expr, ast), media_type="image/svg+xml")


@api_router.post("/latex")
def api_latex(req: ExprRequest) -> str:
    try:
        tokens: list[Token] = tokenize(req.expr)
        ast: Expr | Equation = RDParser(tokens).parse()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return ast.latex()


@api_router.post("/simplify")
def api_simplify(req: ExprRequest) -> str:
    try:
        tokens: list[Token] = tokenize(req.expr)
        ast: Expr | Equation = RDParser(tokens).parse()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return str(ast.simplify())


@api_router.post("/evaluate")
def api_evalutae(req: EvaluationRequest) -> float:
    try:
        tokens: list[Token] = tokenize(req.expr)
        ast: Expr | Equation = RDParser(tokens).parse()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    vars = collect_vars(ast)
    vars -= {"pi", "e"}
    req.env["pi"] = pi
    req.env["e"] = math.e
    if not vars.issubset(req.env.keys()):
        missing = vars - req.env.keys()
        raise HTTPException(
            status_code=400,
            detail=f"Missing variable{'s' if len(missing) > 1 else ''}: {', '.join(missing)}",
        )

    return ast.eval(req.env)


@api_router.post("/differentiate")
def api_differentiate(req: DifferentationRequest) -> str:
    try:
        tokens: list[Token] = tokenize(req.expr)
        ast: Expr | Equation = RDParser(tokens).parse()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if isinstance(ast, Equation):
        raise HTTPException(status_code=400, detail="cannot differentiate equations")

    return str(ast.differentiate(req.wrt))
