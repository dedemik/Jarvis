import ast
import math
import operator


_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def calculate(expression: str) -> int | float:
    """Evaluate basic arithmetic without allowing arbitrary Python execution."""
    if not expression.strip() or len(expression) > 100:
        raise ValueError("İşlem boş olamaz ve en fazla 100 karakter olabilir.")

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as error:
        raise ValueError("İşlem biçimini anlayamadım.") from error

    if sum(1 for _ in ast.walk(tree)) > 32:
        raise ValueError("İşlem çok uzun.")

    def evaluate(node: ast.AST) -> int | float:
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
            left = evaluate(node.left)
            right = evaluate(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError("Üs değeri -10 ile 10 arasında olmalı.")
            result = _BINARY_OPERATORS[type(node.op)](left, right)
            if not math.isfinite(result) or abs(result) > 1e100:
                raise ValueError("Sonuç izin verilen sınırın dışında.")
            return result
        if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
            return _UNARY_OPERATORS[type(node.op)](evaluate(node.operand))
        raise ValueError("Yalnızca sayılar ve temel matematik işlemleri kullanılabilir.")

    try:
        return evaluate(tree)
    except (ArithmeticError, OverflowError) as error:
        raise ValueError("Bu işlem hesaplanamıyor.") from error
