"""Monty Sheets Engine — a spreadsheet formula engine powered by Monty.

Evaluates Python formulas in a sandboxed environment with cell references
resolved via dependency graph. Supports importing Excel formulas and
translating them to Python.
"""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Any

from pydantic_monty import Monty, MontyRuntimeError, ResourceLimits


# --- Excel-to-Python translation (rule-based) ---

# Mapping of Excel functions to Python equivalents
EXCEL_TO_PYTHON: dict[str, str] = {
    'SUM': 'sum',
    'MIN': 'min',
    'MAX': 'max',
    'ABS': 'abs',
    'ROUND': 'round',
    'LEN': 'len',
    'INT': 'int',
    'FLOAT': 'float',
    'STR': 'str',
    'SQRT': 'math.sqrt',
    'FLOOR': 'math.floor',
    'CEILING': 'math.ceil',
    'CEIL': 'math.ceil',
    'LOG': 'math.log',
    'LOG10': 'math.log10',
    'LN': 'math.log',
    'EXP': 'math.exp',
    'SIN': 'math.sin',
    'COS': 'math.cos',
    'TAN': 'math.tan',
    'ASIN': 'math.asin',
    'ACOS': 'math.acos',
    'ATAN': 'math.atan',
    'ATAN2': 'math.atan2',
    'POWER': 'math.pow',
    'MOD': 'math.fmod',
    'PI': 'math.pi',
    'GCD': 'math.gcd',
    'LCM': 'math.lcm',
    'FACT': 'math.factorial',
    'COMBIN': 'math.comb',
    'PERMUT': 'math.perm',
}

# Pattern to match cell references like A1, B2, AA100
CELL_REF_PATTERN = re.compile(r'\b([A-Z]{1,3})(\d{1,7})\b')

# Pattern to match Excel range references like A1:A10
RANGE_PATTERN = re.compile(r'\b([A-Z]{1,3}\d{1,7}):([A-Z]{1,3}\d{1,7})\b')

# Pattern to match Excel function calls like SUM(...), IF(...)
EXCEL_FUNC_PATTERN = re.compile(r'\b([A-Z][A-Z0-9]*)\s*\(')


def col_to_index(col: str) -> int:
    """Convert column letter(s) to 0-based index. A=0, B=1, ..., Z=25, AA=26."""
    result = 0
    for c in col:
        result = result * 26 + (ord(c) - ord('A') + 1)
    return result - 1


def index_to_col(index: int) -> str:
    """Convert 0-based index to column letter(s). 0=A, 1=B, ..., 25=Z, 26=AA."""
    result = ''
    index += 1
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        result = chr(ord('A') + remainder) + result
    return result


def parse_cell_ref(ref: str) -> tuple[str, int]:
    """Parse a cell reference like 'A1' into (column, row). Row is 1-based."""
    m = CELL_REF_PATTERN.fullmatch(ref)
    if not m:
        raise ValueError(f'Invalid cell reference: {ref}')
    return m.group(1), int(m.group(2))


def translate_excel_formula(formula: str) -> str:
    """Translate an Excel formula to a Python expression.

    Handles common patterns rule-based. Returns the Python expression string.
    Does not handle all Excel formulas — complex ones should use LLM translation.

    Examples:
        '=A1*B1'           -> 'A1 * B1'  (after removing =)
        '=SUM(A1, B1)'     -> 'sum(A1, B1)'
        '=IF(A1>0,A1,0)'   -> 'A1 if A1 > 0 else 0'
        '=FLOOR(A1, 1)'    -> 'math.floor(A1)'
        '=POWER(A1, 2)'    -> 'math.pow(A1, 2)'
        '=PI()'            -> 'math.pi'
    """
    # Strip leading =
    expr = formula.lstrip('=').strip()

    # Handle IF(condition, true_val, false_val) -> true_val if condition else false_val
    if_match = re.match(r'^IF\s*\((.+),\s*(.+),\s*(.+)\)$', expr, re.IGNORECASE)
    if if_match:
        cond = translate_excel_formula('=' + if_match.group(1).strip())
        true_val = translate_excel_formula('=' + if_match.group(2).strip())
        false_val = translate_excel_formula('=' + if_match.group(3).strip())
        return f'{true_val} if {cond} else {false_val}'

    # Handle AND/OR
    and_match = re.match(r'^AND\s*\((.+)\)$', expr, re.IGNORECASE)
    if and_match:
        parts = [translate_excel_formula('=' + p.strip()) for p in and_match.group(1).split(',')]
        return ' and '.join(parts)

    or_match = re.match(r'^OR\s*\((.+)\)$', expr, re.IGNORECASE)
    if or_match:
        parts = [translate_excel_formula('=' + p.strip()) for p in or_match.group(1).split(',')]
        return ' or '.join(parts)

    # Replace Excel function names with Python equivalents
    def replace_func(m: re.Match[str]) -> str:
        name = m.group(1).upper()
        py_name = EXCEL_TO_PYTHON.get(name)
        if py_name:
            # PI() is a constant, not a function — consume the '(' so cleanup can remove ')'
            if name == 'PI':
                return py_name + '#STRIP_PAREN#'
            return py_name + '('
        return m.group(0)

    expr = EXCEL_FUNC_PATTERN.sub(replace_func, expr)

    # Clean up PI() -> math.pi (the marker consumed '(' and now we remove ')')
    expr = expr.replace('#STRIP_PAREN#)', '')

    # Replace ^ with ** (Excel uses ^ for power)
    expr = expr.replace('^', '**')

    # Replace <> with != (Excel not-equal)
    expr = expr.replace('<>', '!=')

    return expr


# --- Cell and Sheet model ---


class Cell:
    """A single cell in the spreadsheet.

    Holds the formula (Python expression), computed value, dependencies,
    and optional metadata like the original Excel formula.
    """

    def __init__(
        self,
        formula: str | None = None,
        value: Any = None,
        excel_origin: str | None = None,
    ):
        self.formula = formula
        self.value = value
        self.excel_origin = excel_origin
        self.error: str | None = None
        self.dependencies: set[str] = set()

        if formula:
            self.dependencies = self._extract_refs(formula)

    @staticmethod
    def _extract_refs(formula: str) -> set[str]:
        """Extract cell references from a Python formula expression."""
        return set(CELL_REF_PATTERN.findall_str(formula) if hasattr(CELL_REF_PATTERN, 'findall_str') else
                   [m.group(0) for m in CELL_REF_PATTERN.finditer(formula)])

    def __repr__(self) -> str:
        if self.error:
            return f'Cell(error={self.error!r})'
        if self.formula:
            return f'Cell(={self.formula} -> {self.value!r})'
        return f'Cell({self.value!r})'


class Sheet:
    """A spreadsheet backed by Monty for formula evaluation.

    Cells are addressed by string keys like 'A1', 'B2', etc.
    Formulas are Python expressions that can reference other cells.
    """

    def __init__(self) -> None:
        self.cells: dict[str, Cell] = {}
        self._dep_graph: dict[str, set[str]] = defaultdict(set)
        self._reverse_deps: dict[str, set[str]] = defaultdict(set)

    def set_value(self, ref: str, value: Any) -> None:
        """Set a cell to a static value (no formula)."""
        ref = ref.upper()
        self.cells[ref] = Cell(value=value)
        self._rebuild_deps(ref)
        self._evaluate_dependents(ref)

    def set_formula(self, ref: str, formula: str, excel_origin: str | None = None) -> None:
        """Set a cell to a Python formula expression."""
        ref = ref.upper()
        cell = Cell(formula=formula, excel_origin=excel_origin)
        self.cells[ref] = cell
        self._rebuild_deps(ref)
        self._evaluate(ref)
        self._evaluate_dependents(ref)

    def import_excel_formula(self, ref: str, excel_formula: str) -> None:
        """Import an Excel formula, translating it to Python."""
        ref = ref.upper()
        python_formula = translate_excel_formula(excel_formula)
        self.set_formula(ref, python_formula, excel_origin=excel_formula)

    def get(self, ref: str) -> Any:
        """Get the computed value of a cell."""
        ref = ref.upper()
        cell = self.cells.get(ref)
        if cell is None:
            return None
        return cell.value

    def get_cell(self, ref: str) -> Cell | None:
        """Get the full Cell object."""
        return self.cells.get(ref.upper())

    def _rebuild_deps(self, ref: str) -> None:
        """Rebuild dependency tracking for a cell."""
        # Remove old reverse deps
        for dep in self._dep_graph.get(ref, set()):
            self._reverse_deps[dep].discard(ref)

        cell = self.cells.get(ref)
        if cell and cell.formula:
            self._dep_graph[ref] = cell.dependencies
            for dep in cell.dependencies:
                self._reverse_deps[dep].add(ref)
        else:
            self._dep_graph[ref] = set()

    def _evaluate(self, ref: str) -> None:
        """Evaluate a single cell's formula using Monty."""
        cell = self.cells.get(ref)
        if not cell or not cell.formula:
            return

        # Check for circular references
        if self._has_cycle(ref):
            cell.error = 'Circular reference detected'
            cell.value = None
            return

        # Build inputs from dependencies
        inputs: dict[str, Any] = {}
        input_names: list[str] = []
        for dep in cell.dependencies:
            dep_cell = self.cells.get(dep)
            if dep_cell is not None and dep_cell.value is not None:
                inputs[dep] = dep_cell.value
                input_names.append(dep)

        # Build the Monty code
        code = f'import math\n{cell.formula}'

        try:
            m = Monty(code, inputs=input_names if input_names else None)
            result = m.run(
                inputs=inputs if inputs else None,
                limits=ResourceLimits(
                    max_time=1.0,
                    max_memory=10 * 1024 * 1024,
                ),
            )
            cell.value = result
            cell.error = None
        except MontyRuntimeError as e:
            cell.error = str(e)
            cell.value = None

    def _evaluate_dependents(self, ref: str) -> None:
        """Re-evaluate all cells that depend on the given cell, in dependency order.

        Uses DFS post-order to ensure a cell is only evaluated after all of
        its dependencies have been evaluated first (proper topological sort).
        """
        # Collect all transitive dependents of ref
        all_dirty: set[str] = set()
        stack = list(self._reverse_deps.get(ref, set()))
        while stack:
            current = stack.pop()
            if current not in all_dirty:
                all_dirty.add(current)
                stack.extend(self._reverse_deps.get(current, set()))

        # Topological sort via DFS post-order on the dependency graph.
        # Visit dependencies (what a cell reads) before the cell itself,
        # so that by the time we evaluate a cell, its inputs are up to date.
        order: list[str] = []
        visited: set[str] = set()

        def dfs(node: str) -> None:
            if node in visited:
                return
            visited.add(node)
            # Visit dirty dependencies first (ensures inputs are evaluated before this cell)
            for dep in self._dep_graph.get(node, set()):
                if dep in all_dirty:
                    dfs(dep)
            order.append(node)

        for node in all_dirty:
            dfs(node)

        for dep_ref in order:
            self._evaluate(dep_ref)

    def _has_cycle(self, ref: str) -> bool:
        """Check if adding/evaluating ref would create a circular reference."""
        visited: set[str] = set()
        stack = list(self._dep_graph.get(ref, set()))
        while stack:
            current = stack.pop()
            if current == ref:
                return True
            if current in visited:
                continue
            visited.add(current)
            stack.extend(self._dep_graph.get(current, set()))
        return False

    def display(self) -> str:
        """Return a human-readable display of the sheet."""
        if not self.cells:
            return '(empty sheet)'

        lines: list[str] = []
        for ref in sorted(self.cells.keys(), key=lambda r: (int(re.sub(r'[A-Z]+', '', r)), re.sub(r'\d+', '', r))):
            cell = self.cells[ref]
            if cell.error:
                lines.append(f'  {ref}: #ERROR ({cell.error})')
            elif cell.formula:
                origin = f'  (was: {cell.excel_origin})' if cell.excel_origin else ''
                lines.append(f'  {ref}: {cell.formula}  = {cell.value!r}{origin}')
            else:
                lines.append(f'  {ref}: {cell.value!r}')
        return '\n'.join(lines)
