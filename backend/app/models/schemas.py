"""
models/schemas.py
=================
Esquemas Pydantic para la API REST.

Define los modelos de entrada y salida del endpoint /analyze.
"""

from __future__ import annotations
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """Cuerpo de la petición POST /analyze."""
    expression: str = Field(
        ...,
        min_length=1,
        description="Expresión lógica booleana a analizar",
        json_schema_extra={"example": "~(A | B) & (C | ~D)"},
    )


class TokenInfo(BaseModel):
    """Información de un token individual."""
    type: str = Field(..., description="Tipo del token (ID, OR, AND, NOT, LPAREN, RPAREN)")
    value: str = Field(..., description="Valor léxico del token")
    position: int = Field(..., description="Posición (índice) en la cadena original")


class AnalyzeResponse(BaseModel):
    """Respuesta del endpoint POST /analyze."""
    valid: bool = Field(..., description="Indica si la expresión es sintácticamente válida")
    tokens: List[TokenInfo] = Field(default_factory=list, description="Lista de tokens")
    left_derivation: List[str] = Field(
        default_factory=list,
        description="Pasos de la derivación por la izquierda",
    )
    right_derivation: List[str] = Field(
        default_factory=list,
        description="Pasos de la derivación por la derecha",
    )
    parse_tree: Optional[Dict[str, Any]] = Field(
        None,
        description="Árbol sintáctico en formato JSON anidado",
    )
    message: str = Field(..., description="Mensaje descriptivo del resultado")
    errors: List[str] = Field(
        default_factory=list,
        description="Lista de errores sintácticos encontrados",
    )
