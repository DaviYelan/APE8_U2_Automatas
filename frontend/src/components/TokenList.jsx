/**
 * TokenList.jsx
 * =============
 * Muestra la lista de tokens resultante de la tokenización.
 * Cada token se presenta como una "pill" con tipo y valor.
 */

import "../styles/ResultCard.css";

const TYPE_CLASS = {
  ID: "token-id",
  OR: "token-op",
  AND: "token-op",
  NOT: "token-op",
  LPAREN: "",
  RPAREN: "",
};

export default function TokenList({ tokens }) {
  if (!tokens || tokens.length === 0) return null;

  return (
    <div className="result-card">
      <div className="result-card__header">
        <span className="result-card__icon"></span>
        <span className="result-card__title">Tokens</span>
        <span className="result-card__badge badge-valid">{tokens.length}</span>
      </div>
      <div className="token-list">
        {tokens.map((token, idx) => (
          <span
            key={idx}
            className={`token-pill ${TYPE_CLASS[token.type] || ""}`}
          >
            <span className="token-type">{token.type}</span>
            <span className="token-value">{token.value}</span>
          </span>
        ))}
      </div>
    </div>
  );
}
