"""
grammars/sample_expressions.py
==============================
Registro de expresiones booleanas de ejemplo.

CÓMO AGREGAR UNA NUEVA EXPRESIÓN
---------------------------------
1. Crear una instancia de SampleExpression con:
   - name:        nombre descriptivo
   - expression:  la expresión booleana como string
   - description: explicación breve de qué demuestra

2. Agregarla a la lista SAMPLE_EXPRESSIONS o usar register_expression().

Ejemplo:
    register_expression(SampleExpression(
        name="Doble negación",
        expression="~~A",
        description="Demuestra la negación aplicada dos veces",
    ))

No se requiere modificar ningún otro archivo del proyecto.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass
class SampleExpression:
    """Representa una expresión booleana de ejemplo registrada."""
    name: str
    expression: str
    description: str
    tags: List[str] = field(default_factory=list)


# ------------------------------------------------------------------ #
#  Registro global de expresiones
# ------------------------------------------------------------------ #
SAMPLE_EXPRESSIONS: List[SampleExpression] = []



def register_expression(sample: SampleExpression) -> None:
    """
    Registra una nueva expresión de ejemplo en el sistema.

    Parámetros
    ----------
    sample : SampleExpression
        Expresión a registrar.
    """
    SAMPLE_EXPRESSIONS.append(sample)


def get_all_expressions() -> List[SampleExpression]:
    """Retorna todas las expresiones registradas."""
    return list(SAMPLE_EXPRESSIONS)


# ------------------------------------------------------------------ #
#  Expresiones pre-registradas
# ------------------------------------------------------------------ #

# Expresión 1 – Requerida por la práctica
register_expression(SampleExpression(
    name="Negación con OR y AND",
    expression="~(A | B) & (C | ~D)",
    description=(
        "Combina NOT, OR y AND con paréntesis. "
        "Demuestra precedencia y asociatividad de operadores."
    ),
    tags=["NOT", "OR", "AND", "paréntesis"],
))

register_expression(SampleExpression(
    name="Precedencia de AND sobre OR",
    expression="A | B & C",
    description=(
        "Demuestra la precedencia de AND sobre OR sin paréntesis. "
        "Es equivalente a A | B & C."
    ),
    tags=["OR", "AND"],   
))

#                                                                      #
#  Ejemplo:                                                            #
#    register_expression(SampleExpression(                             #
#        name="Mi expresión",                                          #
#        expression="(A & B) | (C & D)",                               #
#        description="OR de dos conjunciones",                         #
#        tags=["AND", "OR"],                                           #
#    ))                                                                #
# ──────────────────────────────────────────────────────────────────── #

# Expresión 2
register_expression(SampleExpression(
    name="Prueba APE 8",
    expression="id | ~ ( id & id )",
    description=(
        "Evalúa la precedencia correcta de los niveles: OR (Nivel 1), "
        "AND (Nivel 2) y NOT/Paréntesis (Nivel 3)."
    ),
    tags=["OR", "AND", "NOT", "id"]
))