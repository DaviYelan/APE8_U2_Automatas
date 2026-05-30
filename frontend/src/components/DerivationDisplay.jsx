/**
 * DerivationDisplay.jsx
 * =====================
 * Muestra los pasos de una derivación (izquierda o derecha).
 * Cada paso se numera y se conecta con flechas ⇒.
 */

import "../styles/ResultCard.css";

export default function DerivationDisplay({ title, icon, steps }) {
  if (!steps || steps.length === 0) return null;

  return (
    <div className="result-card">
      <div className="result-card__header">
        <span className="result-card__icon">{icon}</span>
        <span className="result-card__title">{title}</span>
        <span className="result-card__badge badge-valid">
          {steps.length} pasos
        </span>
      </div>
      <div className="derivation-steps">
        {steps.map((step, idx) => (
          <div key={idx} className="derivation-step">
            <span className="step-number">{idx + 1}</span>
            <span className="step-arrow">{idx === 0 ? " " : "⇒"}</span>
            <span className="step-content">{step}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
