"""Módulo de definición de gramáticas y expresiones de ejemplo."""

from .cfg import VARIABLES, TERMINALS, START_SYMBOL, PRODUCTIONS, get_cfg_description
from .sample_expressions import (
    SampleExpression,
    register_expression,
    get_all_expressions,
    SAMPLE_EXPRESSIONS,
)

__all__ = [
    "VARIABLES",
    "TERMINALS",
    "START_SYMBOL",
    "PRODUCTIONS",
    "get_cfg_description",
    "SampleExpression",
    "register_expression",
    "get_all_expressions",
    "SAMPLE_EXPRESSIONS",
]
