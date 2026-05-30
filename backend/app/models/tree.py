"""
models/tree.py
==============
Define la estructura de nodo para el Árbol Sintáctico (Parse Tree).

Cada nodo almacena:
  - symbol:      símbolo gramatical (Exp, Term, Factor o terminal)
  - is_terminal: indica si es un símbolo terminal
  - value:       valor léxico (para terminales como identificadores)
  - children:    lista de hijos (vacía en terminales)
  - production:  regla de producción utilizada (solo no-terminales)
"""

from __future__ import annotations
from typing import List, Optional, Dict, Any


class ParseTreeNode:
    """Nodo del árbol de derivación concreto (Concrete Parse Tree)."""

    def __init__(
        self,
        symbol: str,
        is_terminal: bool = False,
        value: Optional[str] = None,
    ) -> None:
        self.symbol: str = symbol
        self.is_terminal: bool = is_terminal
        self.value: str = value if value is not None else symbol
        self.children: List[ParseTreeNode] = []
        self.production: Optional[str] = None  # e.g. "Exp → Exp | Term"

    # ------------------------------------------------------------------ #
    #  Construcción
    # ------------------------------------------------------------------ #
    def add_child(self, child: ParseTreeNode) -> None:
        """Agrega un hijo al nodo."""
        self.children.append(child)

    # ------------------------------------------------------------------ #
    #  Serialización
    # ------------------------------------------------------------------ #
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el árbol a un diccionario anidado (JSON-serializable)."""
        result: Dict[str, Any] = {
            "symbol": self.symbol,
            "value": self.value,
            "is_terminal": self.is_terminal,
        }
        if self.production:
            result["production"] = self.production
        if self.children:
            result["children"] = [child.to_dict() for child in self.children]
        return result

    # ------------------------------------------------------------------ #
    #  Representación legible
    # ------------------------------------------------------------------ #
    def pretty(self, indent: int = 0) -> str:
        """Representación textual indentada del árbol."""
        prefix = "  " * indent
        label = self.value if self.is_terminal else self.symbol
        lines = [f"{prefix}{label}"]
        for child in self.children:
            lines.append(child.pretty(indent + 1))
        return "\n".join(lines)

    def __repr__(self) -> str:
        if self.is_terminal:
            return f"Terminal({self.value!r})"
        return f"NonTerminal({self.symbol!r}, children={len(self.children)})"
