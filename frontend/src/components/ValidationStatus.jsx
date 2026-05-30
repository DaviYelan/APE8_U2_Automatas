/**
 * ValidationStatus.jsx
 * ====================
 * Indicador visual del estado de validación de la expresión.
 */

import "../styles/ResultCard.css";

export default function ValidationStatus({ valid, message, errors }) {
  return (
    <div className="result-card">
      <div className="result-card__header">
        <span className="result-card__icon"></span>
        <span className="result-card__title">Validación</span>
        <span
          className={`result-card__badge ${valid ? "badge-valid" : "badge-invalid"}`}
        >
          {valid ? "Válida" : "Inválida"}
        </span>
      </div>
      <div className="validation-status">
        <div className={`validation-dot ${valid ? "valid" : "invalid"}`} />
        <div>
          <div className="validation-text">
            {valid
              ? "La expresión es sintácticamente correcta"
              : "Se encontraron errores sintácticos"}
          </div>
          <div className="validation-message">{message}</div>
        </div>
      </div>
      {errors && errors.length > 0 && (
        <div style={{ marginTop: "0.75rem" }}>
          {errors.map((err, idx) => (
            <div
              key={idx}
              style={{
                color: "var(--accent-red)",
                fontSize: "0.82rem",
                fontFamily: "var(--font-mono)",
                padding: "0.25rem 0",
              }}
            >
              ⚠ {err}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
