"""
tests/test_analyzer.py
======================
Pruebas unitarias del analizador de expresiones booleanas.
"""

import sys
import os

# Agregar el directorio padre al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from app.parsers.tokenizer import tokenize, TokenType, TokenizerError
from app.parsers.parser import RecursiveDescentParser, ParserError
from app.services.analyzer import analyze_expression
from app.utils.derivation import generate_left_derivation, generate_right_derivation


class TestTokenizer:
    """Pruebas del tokenizador."""

    def test_simple_id(self):
        tokens = tokenize("A")
        assert tokens[0].type == TokenType.ID
        assert tokens[0].value == "A"

    def test_operators(self):
        tokens = tokenize("A | B & ~C")
        types = [t.type for t in tokens if t.type != TokenType.EOF]
        assert types == [
            TokenType.ID, TokenType.OR, TokenType.ID,
            TokenType.AND, TokenType.NOT, TokenType.ID,
        ]

    def test_parentheses(self):
        tokens = tokenize("(A)")
        types = [t.type for t in tokens if t.type != TokenType.EOF]
        assert types == [TokenType.LPAREN, TokenType.ID, TokenType.RPAREN]

    def test_complex_expression(self):
        tokens = tokenize("~(A | B) & (C | ~D)")
        values = [t.value for t in tokens if t.type != TokenType.EOF]
        assert values == ["~", "(", "A", "|", "B", ")", "&", "(", "C", "|", "~", "D", ")"]

    def test_invalid_character(self):
        with pytest.raises(TokenizerError):
            tokenize("A + B")

    def test_whitespace_handling(self):
        tokens1 = tokenize("A|B")
        tokens2 = tokenize("  A  |  B  ")
        vals1 = [t.value for t in tokens1 if t.type != TokenType.EOF]
        vals2 = [t.value for t in tokens2 if t.type != TokenType.EOF]
        assert vals1 == vals2


class TestParser:
    """Pruebas del parser."""

    def test_single_id(self):
        tokens = tokenize("A")
        parser = RecursiveDescentParser(tokens)
        tree = parser.parse()
        assert tree.symbol == "Exp"
        assert tree.production == "Exp → Term"

    def test_or_expression(self):
        tokens = tokenize("A | B")
        parser = RecursiveDescentParser(tokens)
        tree = parser.parse()
        assert tree.production == "Exp → Exp | Term"

    def test_and_expression(self):
        tokens = tokenize("A & B")
        parser = RecursiveDescentParser(tokens)
        tree = parser.parse()
        assert tree.production == "Exp → Term"
        # El hijo Term debería tener la producción Term → Term & Factor
        term = tree.children[0]
        assert term.production == "Term → Term & Factor"

    def test_not_expression(self):
        tokens = tokenize("~A")
        parser = RecursiveDescentParser(tokens)
        tree = parser.parse()
        # Exp → Term → Factor → ~Factor → id
        factor = tree.children[0].children[0]
        assert factor.production == "Factor → ~ Factor"

    def test_parentheses(self):
        tokens = tokenize("(A | B)")
        parser = RecursiveDescentParser(tokens)
        tree = parser.parse()
        factor = tree.children[0].children[0]
        assert factor.production == "Factor → ( Exp )"

    def test_complex_expression(self):
        tokens = tokenize("~(A | B) & (C | ~D)")
        parser = RecursiveDescentParser(tokens)
        tree = parser.parse()
        assert tree.symbol == "Exp"

    def test_missing_rparen(self):
        tokens = tokenize("(A | B")
        parser = RecursiveDescentParser(tokens)
        with pytest.raises(ParserError):
            parser.parse()

    def test_unexpected_token(self):
        tokens = tokenize("| A")
        parser = RecursiveDescentParser(tokens)
        with pytest.raises(ParserError):
            parser.parse()

    def test_extra_tokens(self):
        tokens = tokenize("A B")
        parser = RecursiveDescentParser(tokens)
        with pytest.raises(ParserError):
            parser.parse()


class TestDerivations:
    """Pruebas de generación de derivaciones."""

    def test_left_derivation_simple(self):
        tokens = tokenize("A")
        parser = RecursiveDescentParser(tokens)
        tree = parser.parse()
        left = generate_left_derivation(tree)
        assert left[0] == "Exp"
        assert left[-1] == "A"

    def test_right_derivation_simple(self):
        tokens = tokenize("A")
        parser = RecursiveDescentParser(tokens)
        tree = parser.parse()
        right = generate_right_derivation(tree)
        assert right[0] == "Exp"
        assert right[-1] == "A"

    def test_left_derivation_or(self):
        tokens = tokenize("A | B")
        parser = RecursiveDescentParser(tokens)
        tree = parser.parse()
        left = generate_left_derivation(tree)
        assert left[0] == "Exp"
        assert left[-1] == "A | B"
        # Debe tener pasos intermedios
        assert len(left) > 2

    def test_right_derivation_complex(self):
        tokens = tokenize("~(A | B) & (C | ~D)")
        parser = RecursiveDescentParser(tokens)
        tree = parser.parse()
        right = generate_right_derivation(tree)
        assert right[0] == "Exp"
        assert right[-1] == "~ ( A | B ) & ( C | ~ D )"


class TestAnalyzerService:
    """Pruebas del servicio de análisis completo."""

    def test_valid_expression(self):
        result = analyze_expression("~(A | B) & (C | ~D)")
        assert result.valid is True
        assert len(result.tokens) > 0
        assert len(result.left_derivation) > 0
        assert len(result.right_derivation) > 0
        assert result.parse_tree is not None
        assert result.errors == []

    def test_invalid_expression(self):
        result = analyze_expression("A & | B")
        assert result.valid is False
        assert len(result.errors) > 0

    def test_invalid_character(self):
        result = analyze_expression("A + B")
        assert result.valid is False

    def test_empty_parens(self):
        result = analyze_expression("()")
        assert result.valid is False

    def test_test_expression_1(self):
        """Expresión de prueba del docente: id | ~(id & id)"""
        result = analyze_expression("id | ~(id & id)")
        assert result.valid is True

    def test_test_expression_2(self):
        """Expresión de prueba del docente: A | B & C"""
        result = analyze_expression("A | B & C")
        assert result.valid is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
