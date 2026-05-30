/**
 * services/api.js
 * ================
 * Servicio de comunicación con el backend FastAPI.
 *
 * Funciones:
 *   analyzeExpression(expr)  – POST /analyze
 *   fetchGrammar()           – GET  /grammar
 *   fetchExamples()          – GET  /examples
 */

const API_BASE = "http://localhost:8000";

/**
 * Analiza una expresión booleana enviándola al backend.
 * @param {string} expression - La expresión a analizar.
 * @returns {Promise<Object>} Respuesta con tokens, derivaciones, árbol, etc.
 */
export async function analyzeExpression(expression) {
  const response = await fetch(`${API_BASE}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ expression }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `Error ${response.status}`);
  }

  return response.json();
}

/**
 * Obtiene la definición formal de la gramática CFG.
 * @returns {Promise<Object>}
 */
export async function fetchGrammar() {
  const response = await fetch(`${API_BASE}/grammar`);
  if (!response.ok) throw new Error(`Error ${response.status}`);
  return response.json();
}

/**
 * Obtiene las expresiones de ejemplo registradas.
 * @returns {Promise<Array>}
 */
export async function fetchExamples() {
  const response = await fetch(`${API_BASE}/examples`);
  if (!response.ok) throw new Error(`Error ${response.status}`);
  return response.json();
}
