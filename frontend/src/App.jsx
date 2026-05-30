/**
 * App.jsx
 * =======
 * Componente raíz de la aplicación.
 *
 * Orquesta los componentes de entrada, resultados y visualización.
 */

import { useState } from "react";
import { analyzeExpression } from "./services/api";
import ExpressionInput from "./components/ExpressionInput";
import TokenList from "./components/TokenList";
import DerivationDisplay from "./components/DerivationDisplay";
import ValidationStatus from "./components/ValidationStatus";
import ParseTreeView from "./components/ParseTreeView";
import "./styles/App.css";

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async (expression) => {
    setLoading(true);
    setError(null);
    try {
      const data = await analyzeExpression(expression);
      setResult(data);
    } catch (err) {
      setError(
        err.message || "No se pudo conectar con el servidor. Verifica que el backend esté corriendo."
      );
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <h1>
          Analizador <span>CFG</span>
        </h1>
        <p className="subtitle">
          Construcción y Validación de Gramáticas Libres de Contexto
        </p>
        <p className="university">
          Teoría de Autómatas y Computabilidad Avanzada — Universidad Nacional de Loja
        </p>
      </header>

      {/* Gramática */}
      <section className="grammar-section">
        <h2>Gramática Libre de Contexto (CFG)</h2>
        <div className="grammar-rules">
          <div className="rule">
            <span className="lhs">Exp</span>
            <span className="arrow">→</span>
            <span className="rhs">
              Exp <span className="terminal">|</span> Term
              <span className="separator"> | </span>
              Term
            </span>
          </div>
          <div className="rule">
            <span className="lhs">Term</span>
            <span className="arrow">→</span>
            <span className="rhs">
              Term <span className="terminal">&</span> Factor
              <span className="separator"> | </span>
              Factor
            </span>
          </div>
          <div className="rule">
            <span className="lhs">Factor</span>
            <span className="arrow">→</span>
            <span className="rhs">
              <span className="terminal">~</span> Factor
              <span className="separator"> | </span>
              <span className="terminal">(</span> Exp <span className="terminal">)</span>
              <span className="separator"> | </span>
              <span className="terminal">id</span>
            </span>
          </div>
        </div>
      </section>

      {/* Input */}
      <ExpressionInput onAnalyze={handleAnalyze} isLoading={loading} />

      {/* Error global */}
      {error && (
        <div className="error-banner">
          <div className="error-title">Error de conexión</div>
          {error}
        </div>
      )}

      {/* Resultados */}
      {result && (
        <div className="results-grid">
          <ValidationStatus
            valid={result.valid}
            message={result.message}
            errors={result.errors}
          />
          <TokenList tokens={result.tokens} />
          <DerivationDisplay
            title="Derivación por la Izquierda"
            icon=""
            steps={result.left_derivation}
          />
          <DerivationDisplay
            title="Derivación por la Derecha"
            icon=""
            steps={result.right_derivation}
          />
          <ParseTreeView tree={result.valid ? result.parse_tree : null} />
        </div>
      )}
    </div>
  );
}
