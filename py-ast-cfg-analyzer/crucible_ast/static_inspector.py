import ast
from dataclasses import dataclass, field
from typing import List, Set


FORBIDDEN_IMPORTS: Set[str] = {"subprocess", "shutil", "socket", "ctypes", "pty"}
FORBIDDEN_BUILTINS: Set[str] = {"eval", "exec", "compile", "__import__"}


@dataclass(frozen=True)
class AstInspectionReport:
    syntax_valid: bool
    cyclomatic_complexity: int
    max_loop_nesting_depth: int
    estimated_time_complexity: str
    security_violations: List[str] = field(default_factory=list)
    missing_type_annotations: bool = False
    production_ready: bool = False


class _ControlFlowVisitor(ast.NodeVisitor):
    """Walks a Python AST to compute McCabe complexity, loop nesting depth, and safety."""

    def __init__(self) -> None:
        self.complexity: int = 1
        self.current_loop_depth: int = 0
        self.max_loop_depth: int = 0
        self.violations: List[str] = []
        self.untyped_functions: int = 0

    def _enter_loop(self, node: ast.AST) -> None:
        self.complexity += 1
        self.current_loop_depth += 1
        if self.current_loop_depth > self.max_loop_depth:
            self.max_loop_depth = self.current_loop_depth
        self.generic_visit(node)
        self.current_loop_depth -= 1

    def visit_For(self, node: ast.For) -> None:
        self._enter_loop(node)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self._enter_loop(node)

    def visit_While(self, node: ast.While) -> None:
        # Detect literal infinite loop `while True:` without a `Break` node inside body
        if isinstance(node.test, ast.Constant) and node.test.value is True:
            has_break = any(isinstance(child, (ast.Break, ast.Return, ast.Raise)) for child in ast.walk(node))
            if not has_break:
                self.violations.append("INFINITE_LOOP_RISK: `while True` without break/return/raise")
        self._enter_loop(node)

    def visit_If(self, node: ast.If) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        self.complexity += 1
        if node.type is None:
            self.violations.append("BARE_EXCEPT_CLAUSE: catches SystemExit/KeyboardInterrupt")
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        self.complexity += max(0, len(node.values) - 1)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if node.returns is None or any(arg.annotation is None for arg in node.args.args):
            self.untyped_functions += 1
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            root_pkg = alias.name.split(".")[0]
            if root_pkg in FORBIDDEN_IMPORTS:
                self.violations.append(f"FORBIDDEN_IMPORT: {root_pkg}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module:
            root_pkg = node.module.split(".")[0]
            if root_pkg in FORBIDDEN_IMPORTS:
                self.violations.append(f"FORBIDDEN_IMPORT: {root_pkg}")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_BUILTINS:
            self.violations.append(f"FORBIDDEN_BUILTIN_CALL: {node.func.id}()")
        self.generic_visit(node)


def analyze_python_submission(source_code: str, max_allowed_complexity: int = 12) -> AstInspectionReport:
    """Parses AI-generated Python code and returns a deterministic static analysis report."""
    try:
        tree = ast.parse(source_code)
    except SyntaxError as exc:
        return AstInspectionReport(
            syntax_valid=False,
            cyclomatic_complexity=0,
            max_loop_nesting_depth=0,
            estimated_time_complexity="SYNTAX_ERROR",
            security_violations=[f"SYNTAX_ERROR: line {exc.lineno}"],
            missing_type_annotations=True,
            production_ready=False,
        )

    visitor = _ControlFlowVisitor()
    visitor.visit(tree)

    if visitor.max_loop_depth == 0:
        big_o = "O(1)"
    elif visitor.max_loop_depth == 1:
        big_o = "O(N)"
    elif visitor.max_loop_depth == 2:
        big_o = "O(N^2)"
    else:
        big_o = f"O(N^{visitor.max_loop_depth})"

    missing_types = visitor.untyped_functions > 0
    is_ready = (
        len(visitor.violations) == 0
        and visitor.complexity <= max_allowed_complexity
        and visitor.max_loop_depth <= 2
        and not missing_types
    )

    return AstInspectionReport(
        syntax_valid=True,
        cyclomatic_complexity=visitor.complexity,
        max_loop_nesting_depth=visitor.max_loop_depth,
        estimated_time_complexity=big_o,
        security_violations=visitor.violations,
        missing_type_annotations=missing_types,
        production_ready=is_ready,
    )
