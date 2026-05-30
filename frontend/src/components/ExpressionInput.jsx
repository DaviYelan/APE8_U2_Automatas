/**
 * ExpressionInput.jsx
 * ===================
 * Campo de entrada para la expresión booleana con botón de análisis
 * y chips de expresiones de ejemplo.
 */

import { useState, useEffect } from "react";
import { fetchExamples } from "../services/api";
import "../styles/ExpressionInput.css";

export default function ExpressionInput({ onAnalyze, isLoading }) {
  const [expression, setExpression] = useState("");
  const [examples, setExamples] = useState([]);

  useEffect(() => {
    fetchExamples()
      .then(setExamples)
      .catch(() => setExamples([]));
  }, []);

  const handleSubmit = () => {
    const trimmed = expression.trim();
    if (trimmed && !isLoading) {
      onAnalyze(trimmed);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") handleSubmit();
  };

  return (
    <div className="expression-input">
      <label className="input-label">Expresión Booleana</label>
      <div className="input-row">
        <input
          type="text"
          className="input-field"
          value={expression}
          onChange={(e) => setExpression(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ej: ~(A | B) & (C | ~D)"
          disabled={isLoading}
        />
        <button
          className="btn-analyze"
          onClick={handleSubmit}
          disabled={isLoading || !expression.trim()}
        >
          {isLoading ? "Analizando…" : "Analizar"}
        </button>
      </div>

      {examples.length > 0 && (
        <div className="examples-row">
          <span className="examples-label">Ejemplos:</span>
          {examples.map((ex, idx) => (
            <button
              key={idx}
              className="example-chip"
              onClick={() => setExpression(ex.expression)}
              title={ex.description}
            >
              {ex.expression}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
