"""
grammars/cfg.py
===============
Definición formal de la Gramática Libre de Contexto (CFG) para
expresiones lógicas booleanas.

Componentes formales de la CFG  G = (V, Σ, R, S):
  V  = { Exp, Term, Factor }          (Variables / No-terminales)
  Σ  = { id, |, &, ~, (, ) }          (Terminales)
  S  = Exp                             (Símbolo inicial)
  R  = { reglas de producción }        (Producciones)

Reglas de producción (R):
  Exp    → Exp | Term      (OR  – menor precedencia)
  Exp    → Term
  Term   → Term & Factor   (AND – mayor precedencia)
  Term   → Factor
  Factor → ~ Factor        (NOT – máxima precedencia)
  Factor → ( Exp )
  Factor → id

Precedencia (de menor a mayor):  OR < AND < NOT
Asociatividad: izquierda para OR y AND.
"""

from typing import Dict, List, Set


# ------------------------------------------------------------------ #
#  Definición formal
# ------------------------------------------------------------------ #

VARIABLES: Set[str] = {"Exp", "Term", "Factor"}

TERMINALS: Set[str] = {"id", "|", "&", "~", "(", ")"}

START_SYMBOL: str = "Exp"

# Cada producción: lado_izquierdo → lista de símbolos del lado derecho
PRODUCTIONS: Dict[str, List[List[str]]] = {
    "Exp": [
        ["Exp", "|", "Term"],   # Exp → Exp | Term
        ["Term"],                # Exp → Term
    ],
    "Term": [
        ["Term", "&", "Factor"],  # Term → Term & Factor
        ["Factor"],               # Term → Factor
    ],
    "Factor": [
        ["~", "Factor"],          # Factor → ~ Factor
        ["(", "Exp", ")"],        # Factor → ( Exp )
        ["id"],                   # Factor → id
    ],
}


def get_cfg_description() -> str:
    """Retorna una representación legible de la gramática."""
    lines = [
        "Gramática Libre de Contexto (CFG) para Expresiones Booleanas",
        "=" * 60,
        f"  V (No-terminales) = {VARIABLES}",
        f"  Σ (Terminales)    = {TERMINALS}",
        f"  S (Símbolo inicial) = {START_SYMBOL}",
        "",
        "  Reglas de producción (R):",
    ]
    for lhs, alternatives in PRODUCTIONS.items():
        for rhs in alternatives:
            lines.append(f"    {lhs} → {' '.join(rhs)}")
    return "\n".join(lines)
