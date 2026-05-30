"""
utils/derivation.py
===================
Generador de derivaciones (izquierda y derecha) a partir de un
árbol de derivación concreto.

Derivación por la izquierda:
  En cada paso se expande el no-terminal MÁS A LA IZQUIERDA.

Derivación por la derecha:
  En cada paso se expande el no-terminal MÁS A LA DERECHA.

Ambas se extraen recorriendo el Parse Tree con estrategias distintas.
"""

from __future__ import annotations
from typing import List, Union

from app.models.tree import ParseTreeNode


# Tipo para los elementos de la forma sentencial
_Symbol = ParseTreeNode


def _symbols_to_string(symbols: List[_Symbol]) -> str:
    """
    Convierte una lista de nodos (forma sentencial) a cadena legible.

    Los no-terminales se representan por su nombre de símbolo;
    los terminales por su valor léxico.
    """
    parts: List[str] = []
    for sym in symbols:
        if sym.is_terminal:
            parts.append(sym.value)
        else:
            parts.append(sym.symbol)
    return " ".join(parts)


def generate_left_derivation(root: ParseTreeNode) -> List[str]:
    """
    Genera la derivación por la izquierda a partir del árbol.

    Algoritmo:
      1. Iniciar con la forma sentencial  [raíz].
      2. Encontrar el no-terminal más a la izquierda.
      3. Reemplazarlo por sus hijos en el árbol.
      4. Registrar la nueva forma sentencial.
      5. Repetir hasta que no queden no-terminales.

    Retorna
    -------
    List[str]
        Lista de cadenas, cada una representando un paso de la derivación.
    """
    sentential_form: List[_Symbol] = [root]
    steps: List[str] = [_symbols_to_string(sentential_form)]

    while True:
        # Buscar el no-terminal más a la izquierda
        idx = _find_leftmost_nonterminal(sentential_form)
        if idx is None:
            break

        # Expandir: reemplazar el no-terminal por sus hijos
        node = sentential_form[idx]
        sentential_form = (
            sentential_form[:idx]
            + node.children
            + sentential_form[idx + 1:]
        )
        steps.append(_symbols_to_string(sentential_form))

    return steps


def generate_right_derivation(root: ParseTreeNode) -> List[str]:
    """
    Genera la derivación por la derecha a partir del árbol.

    Algoritmo idéntico a la izquierda, pero en cada paso se expande
    el no-terminal MÁS A LA DERECHA.

    Retorna
    -------
    List[str]
        Lista de cadenas, cada una representando un paso de la derivación.
    """
    sentential_form: List[_Symbol] = [root]
    steps: List[str] = [_symbols_to_string(sentential_form)]

    while True:
        # Buscar el no-terminal más a la derecha
        idx = _find_rightmost_nonterminal(sentential_form)
        if idx is None:
            break

        # Expandir
        node = sentential_form[idx]
        sentential_form = (
            sentential_form[:idx]
            + node.children
            + sentential_form[idx + 1:]
        )
        steps.append(_symbols_to_string(sentential_form))

    return steps


def _find_leftmost_nonterminal(symbols: List[_Symbol]) -> Union[int, None]:
    """Retorna el índice del primer no-terminal, o None."""
    for i, sym in enumerate(symbols):
        if not sym.is_terminal:
            return i
    return None


def _find_rightmost_nonterminal(symbols: List[_Symbol]) -> Union[int, None]:
    """Retorna el índice del último no-terminal, o None."""
    for i in range(len(symbols) - 1, -1, -1):
        if not symbols[i].is_terminal:
            return i
    return None
