"""
services/analyzer.py
====================
Servicio principal de análisis de expresiones booleanas.

Orquesta los componentes:
  1. Tokenizador  →  lista de tokens
  2. Parser       →  árbol de derivación
  3. Derivaciones →  izquierda y derecha
  4. Serialización → respuesta JSON

Este servicio es el punto de contacto entre la API y la lógica del parser.
"""

from __future__ import annotations
from typing import List

from app.parsers.tokenizer import tokenize, TokenizerError, Token
from app.parsers.parser import RecursiveDescentParser, ParserError
from app.models.schemas import AnalyzeResponse, TokenInfo
from app.models.tree import ParseTreeNode
from app.utils.derivation import generate_left_derivation, generate_right_derivation


def analyze_expression(expression: str) -> AnalyzeResponse:
    """
    Analiza una expresión booleana completa.

    Pasos:
      1. Tokenización
      2. Parsing (construcción del árbol sintáctico)
      3. Generación de derivaciones izquierda y derecha
      4. Construcción de la respuesta

    Parámetros
    ----------
    expression : str
        Expresión booleana a analizar.

    Retorna
    -------
    AnalyzeResponse
        Respuesta completa con tokens, derivaciones, árbol y estado.
    """
    errors: List[str] = []

    # ── Paso 1: Tokenización ──────────────────────────────────────── #
    try:
        tokens = tokenize(expression)
    except TokenizerError as e:
        return AnalyzeResponse(
            valid=False,
            tokens=[],
            left_derivation=[],
            right_derivation=[],
            parse_tree=None,
            message=f"Error léxico: {e}",
            errors=[str(e)],
        )

    # Convertir tokens a esquema de salida (excluir EOF)
    token_infos = [
        TokenInfo(type=tok.type.value, value=tok.value, position=tok.position)
        for tok in tokens
        if tok.type.value != "EOF"
    ]

    # ── Paso 2: Análisis sintáctico ──────────────────────────────── #
    try:
        parser = RecursiveDescentParser(tokens)
        tree: ParseTreeNode = parser.parse()
    except ParserError as e:
        return AnalyzeResponse(
            valid=False,
            tokens=token_infos,
            left_derivation=[],
            right_derivation=[],
            parse_tree=None,
            message=f"Error sintáctico: {e}",
            errors=[str(e)],
        )

    # ── Paso 3: Derivaciones ─────────────────────────────────────── #
    left_deriv = generate_left_derivation(tree)
    right_deriv = generate_right_derivation(tree)

    # ── Paso 4: Respuesta ────────────────────────────────────────── #
    return AnalyzeResponse(
        valid=True,
        tokens=token_infos,
        left_derivation=left_deriv,
        right_derivation=right_deriv,
        parse_tree=tree.to_dict(),
        message="Cadena válida según la gramática CFG",
        errors=[],
    )
