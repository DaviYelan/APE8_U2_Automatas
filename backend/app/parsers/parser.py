"""
parsers/parser.py
=================
Parser descendente recursivo para la gramática libre de contexto (CFG)
de expresiones lógicas booleanas.

Gramática original (con recursión izquierda):
  Exp    → Exp | Term   |  Term
  Term   → Term & Factor  |  Factor
  Factor → ~ Factor  |  ( Exp )  |  id

El parser elimina internamente la recursión izquierda para poder
usar descenso recursivo, pero construye el árbol de derivación
concreto en términos de la gramática *original* (asociatividad izquierda).

Esto permite generar derivaciones correctas por la izquierda
y por la derecha a partir del árbol resultante.
"""

from __future__ import annotations
from typing import List, Optional

from app.parsers.tokenizer import Token, TokenType, tokenize
from app.models.tree import ParseTreeNode


class ParserError(Exception):
    """Error sintáctico durante el análisis."""

    def __init__(self, message: str, position: int = -1) -> None:
        self.position = position
        super().__init__(message)


class RecursiveDescentParser:
    """
    Parser descendente recursivo que construye un Parse Tree concreto.

    Uso:
        parser = RecursiveDescentParser(tokens)
        tree = parser.parse()
    """

    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.pos: int = 0
        self.errors: List[str] = []

    # ------------------------------------------------------------------ #
    #  Helpers de navegación
    # ------------------------------------------------------------------ #
    def _current(self) -> Token:
        """Token actual."""
        return self.tokens[self.pos]

    def _current_type(self) -> TokenType:
        """Tipo del token actual."""
        return self._current().type

    def _advance(self) -> Token:
        """Consume el token actual y avanza al siguiente."""
        tok = self._current()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return tok

    def _expect(self, expected: TokenType) -> Token:
        """Consume un token del tipo esperado o lanza error."""
        tok = self._current()
        if tok.type != expected:
            msg = (
                f"Se esperaba {expected.value} pero se encontró "
                f"'{tok.value}' ({tok.type.value}) en la posición {tok.position}"
            )
            raise ParserError(msg, tok.position)
        return self._advance()

    # ------------------------------------------------------------------ #
    #  Punto de entrada
    # ------------------------------------------------------------------ #
    def parse(self) -> ParseTreeNode:
        """
        Analiza la lista completa de tokens y retorna la raíz
        del árbol de derivación concreto.
        """
        tree = self._parse_exp()

        # Verificar que se consumió toda la entrada
        if self._current_type() != TokenType.EOF:
            tok = self._current()
            raise ParserError(
                f"Token inesperado '{tok.value}' en la posición {tok.position}. "
                f"Se esperaba fin de la expresión.",
                tok.position,
            )
        return tree

    # ------------------------------------------------------------------ #
    #  Reglas de producción
    # ------------------------------------------------------------------ #
    def _parse_exp(self) -> ParseTreeNode:
        """
        Exp → Exp | Term   (asociatividad izquierda, OR)
        Exp → Term

        Implementación sin recursión izquierda:
          Exp  → Term ( '|' Term )*
        Se reconstruye el árbol con asociatividad izquierda.
        """
        term_node = self._parse_term()

        # Caso base: Exp → Term
        result = ParseTreeNode("Exp")
        result.add_child(term_node)
        result.production = "Exp → Term"

        # Mientras haya operador OR, construir asociatividad izquierda
        while self._current_type() == TokenType.OR:
            new_exp = ParseTreeNode("Exp")
            new_exp.add_child(result)                                     # Exp (izquierda)
            new_exp.add_child(ParseTreeNode("|", is_terminal=True))       # |
            self._advance()                                               # consumir |
            new_exp.add_child(self._parse_term())                         # Term (derecha)
            new_exp.production = "Exp → Exp | Term"
            result = new_exp

        return result

    def _parse_term(self) -> ParseTreeNode:
        """
        Term → Term & Factor   (asociatividad izquierda, AND)
        Term → Factor

        Implementación sin recursión izquierda:
          Term → Factor ( '&' Factor )*
        Se reconstruye el árbol con asociatividad izquierda.
        """
        factor_node = self._parse_factor()

        # Caso base: Term → Factor
        result = ParseTreeNode("Term")
        result.add_child(factor_node)
        result.production = "Term → Factor"

        # Mientras haya operador AND, construir asociatividad izquierda
        while self._current_type() == TokenType.AND:
            new_term = ParseTreeNode("Term")
            new_term.add_child(result)                                    # Term (izquierda)
            new_term.add_child(ParseTreeNode("&", is_terminal=True))      # &
            self._advance()                                               # consumir &
            new_term.add_child(self._parse_factor())                      # Factor (derecha)
            new_term.production = "Term → Term & Factor"
            result = new_term

        return result

    def _parse_factor(self) -> ParseTreeNode:
        """
        Factor → ~ Factor
        Factor → ( Exp )
        Factor → id
        """
        tok_type = self._current_type()

        # Factor → ~ Factor
        if tok_type == TokenType.NOT:
            node = ParseTreeNode("Factor")
            node.add_child(ParseTreeNode("~", is_terminal=True))
            self._advance()
            node.add_child(self._parse_factor())
            node.production = "Factor → ~ Factor"
            return node

        # Factor → ( Exp )
        if tok_type == TokenType.LPAREN:
            node = ParseTreeNode("Factor")
            node.add_child(ParseTreeNode("(", is_terminal=True))
            self._advance()
            node.add_child(self._parse_exp())
            self._expect(TokenType.RPAREN)
            node.add_child(ParseTreeNode(")", is_terminal=True))
            node.production = "Factor → ( Exp )"
            return node

        # Factor → id
        if tok_type == TokenType.ID:
            node = ParseTreeNode("Factor")
            tok = self._advance()
            id_node = ParseTreeNode("id", is_terminal=True, value=tok.value)
            node.add_child(id_node)
            node.production = "Factor → id"
            return node

        # Error: ningún caso coincide
        tok = self._current()
        expected = "un identificador, '~' o '('"
        raise ParserError(
            f"Se esperaba {expected} pero se encontró "
            f"'{tok.value}' ({tok.type.value}) en la posición {tok.position}",
            tok.position,
        )
