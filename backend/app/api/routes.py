"""
api/routes.py
=============
Endpoints REST de la aplicación.

Endpoints disponibles:
  POST /analyze          Analiza una expresión booleana
  GET  /grammar          Retorna la definición formal de la CFG
  GET  /examples         Retorna las expresiones de ejemplo registradas
  GET  /health           Health check
"""

from __future__ import annotations
from typing import Dict, Any, List

from fastapi import APIRouter

from app.models.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.analyzer import analyze_expression
from app.grammars.cfg import get_cfg_description, PRODUCTIONS, VARIABLES, TERMINALS, START_SYMBOL
from app.grammars.sample_expressions import get_all_expressions

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """
    Analiza una expresión lógica booleana.

    Recibe una expresión como cadena de texto y retorna:
    - Validación sintáctica
    - Lista de tokens
    - Derivación por la izquierda
    - Derivación por la derecha
    - Árbol sintáctico (Parse Tree)
    - Errores detallados (si existen)
    """
    return analyze_expression(request.expression)


@router.get("/grammar")
async def get_grammar() -> Dict[str, Any]:
    """Retorna la definición formal de la CFG."""
    return {
        "variables": sorted(VARIABLES),
        "terminals": sorted(TERMINALS),
        "start_symbol": START_SYMBOL,
        "productions": {
            lhs: [" ".join(rhs) for rhs in alternatives]
            for lhs, alternatives in PRODUCTIONS.items()
        },
        "description": get_cfg_description(),
    }


@router.get("/examples")
async def get_examples() -> List[Dict[str, Any]]:
    """Retorna todas las expresiones de ejemplo registradas."""
    return [
        {
            "name": sample.name,
            "expression": sample.expression,
            "description": sample.description,
            "tags": sample.tags,
        }
        for sample in get_all_expressions()
    ]


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check del servicio."""
    return {"status": "ok", "service": "CFG Boolean Expression Analyzer"}
