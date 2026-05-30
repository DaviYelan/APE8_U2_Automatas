"""
parsers/tokenizer.py
====================
Analizador léxico (tokenizador) para expresiones lógicas booleanas.

Convierte una cadena de texto en una lista de tokens reconocidos
por la gramática libre de contexto:

  Terminales:  id, |, &, ~, (, )

Ejemplo:
  "~(A | B) & C"  →  [~, (, A, |, B, ), &, C]
"""

from __future__ import annotations
from enum import Enum
from typing import List, NamedTuple


class TokenType(Enum):
    """Tipos de token reconocidos por la gramática."""
    ID = "ID"          # Identificador (variable proposicional)
    OR = "OR"          # Operador OR  →  |
    AND = "AND"        # Operador AND →  &
    NOT = "NOT"        # Operador NOT →  ~
    LPAREN = "LPAREN"  # Paréntesis izquierdo  →  (
    RPAREN = "RPAREN"  # Paréntesis derecho     →  )
    EOF = "EOF"        # Fin de la entrada


class Token(NamedTuple):
    """Representación inmutable de un token."""
    type: TokenType
    value: str
    position: int  # posición del carácter en la cadena original


# Mapa de caracteres individuales a tipos de token
_SINGLE_CHAR_TOKENS = {
    "|": TokenType.OR,
    "&": TokenType.AND,
    "~": TokenType.NOT,
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
}


class TokenizerError(Exception):
    """Error durante la tokenización."""

    def __init__(self, message: str, position: int) -> None:
        self.position = position
        super().__init__(message)


def tokenize(expression: str) -> List[Token]:
    """
    Tokeniza una expresión booleana.

    Parámetros
    ----------
    expression : str
        Cadena con la expresión booleana (e.g. "~(A | B) & C").

    Retorna
    -------
    List[Token]
        Lista ordenada de tokens, terminada en un token EOF.

    Lanza
    -----
    TokenizerError
        Si encuentra un carácter no reconocido.
    """
    tokens: List[Token] = []
    i = 0
    length = len(expression)

    while i < length:
        ch = expression[i]

        # Ignorar espacios en blanco
        if ch.isspace():
            i += 1
            continue

        # Operadores y paréntesis de un solo carácter
        if ch in _SINGLE_CHAR_TOKENS:
            tokens.append(Token(_SINGLE_CHAR_TOKENS[ch], ch, i))
            i += 1
            continue

        # Identificadores: letras (admite nombres multiletter como "var1")
        if ch.isalpha() or ch == '_':
            start = i
            while i < length and (expression[i].isalnum() or expression[i] == '_'):
                i += 1
            value = expression[start:i]
            tokens.append(Token(TokenType.ID, value, start))
            continue

        # Carácter no reconocido
        raise TokenizerError(
            f"Carácter inesperado '{ch}' en la posición {i}",
            position=i,
        )

    # Token de fin de entrada
    tokens.append(Token(TokenType.EOF, "", length))
    return tokens
