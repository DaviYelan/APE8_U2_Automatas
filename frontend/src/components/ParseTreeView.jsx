/**
 * ParseTreeView.jsx
 * =================
 * Visualización SVG del árbol sintáctico (Parse Tree).
 *
 * Algoritmo de layout:
 *   1. Calcular el ancho de cada subárbol (bottom-up).
 *   2. Asignar posiciones x,y a cada nodo (top-down).
 *   3. Dibujar aristas y nodos.
 */

import { useState, useMemo } from "react";
import "../styles/ParseTree.css";
import "../styles/ResultCard.css";

const NODE_W = 64;
const NODE_H = 30;
const H_GAP = 16;
const V_GAP = 56;
const PAD_X = 40;
const PAD_Y = 40;

/**
 * Calcula recursivamente el ancho necesario para cada subárbol.
 */
function computeWidths(node) {
  if (!node.children || node.children.length === 0) {
    return { ...node, _width: NODE_W };
  }
  const kids = node.children.map(computeWidths);
  const totalW = kids.reduce((s, k) => s + k._width, 0) + H_GAP * (kids.length - 1);
  return { ...node, children: kids, _width: Math.max(NODE_W, totalW) };
}

/**
 * Asigna posiciones (x, y) a cada nodo del árbol.
 */
function assignPositions(node, x, y, positions, edges) {
  const id = positions.length;
  const label = node.is_terminal ? node.value : node.symbol;
  positions.push({ id, x, y, label, is_terminal: node.is_terminal });

  if (node.children && node.children.length > 0) {
    const totalW = node.children.reduce((s, k) => s + k._width, 0) + H_GAP * (node.children.length - 1);
    let cx = x - totalW / 2;

    for (const child of node.children) {
      const childX = cx + child._width / 2;
      const childY = y + V_GAP;
      const childId = positions.length;
      edges.push({ from: id, to: childId });
      assignPositions(child, childX, childY, positions, edges);
      cx += child._width + H_GAP;
    }
  }
}

export default function ParseTreeView({ tree }) {
  const [scale, setScale] = useState(1);

  const layout = useMemo(() => {
    if (!tree) return null;

    const sized = computeWidths(tree);
    const positions = [];
    const edges = [];
    const rootX = sized._width / 2 + PAD_X;
    assignPositions(sized, rootX, PAD_Y, positions, edges);

    // Calcular bounds
    let minX = Infinity, maxX = -Infinity, maxY = -Infinity;
    for (const p of positions) {
      if (p.x - NODE_W / 2 < minX) minX = p.x - NODE_W / 2;
      if (p.x + NODE_W / 2 > maxX) maxX = p.x + NODE_W / 2;
      if (p.y + NODE_H / 2 > maxY) maxY = p.y + NODE_H / 2;
    }

    const width = maxX - minX + PAD_X * 2;
    const height = maxY + PAD_Y;
    const offsetX = -minX + PAD_X;

    return { positions, edges, width, height, offsetX };
  }, [tree]);

  if (!tree) {
    return (
      <div className="result-card full-width">
        <div className="result-card__header">
          <span className="result-card__icon">🌳</span>
          <span className="result-card__title">Árbol Sintáctico</span>
        </div>
        <div className="tree-empty">
          Ingresa una expresión y presiona "Analizar" para ver el árbol.
        </div>
      </div>
    );
  }

  const { positions, edges, width, height, offsetX } = layout;
  const svgW = width * scale;
  const svgH = height * scale;

  return (
    <div className="result-card full-width">
      <div className="result-card__header">
        <span className="result-card__icon"></span>
        <span className="result-card__title">Árbol Sintáctico (Parse Tree)</span>
      </div>
      <div className="parse-tree-container">
        <svg
          className="parse-tree-svg"
          width={svgW}
          height={svgH}
          viewBox={`0 0 ${width} ${height}`}
        >
          {/* Aristas */}
          {edges.map((e, idx) => {
            const from = positions[e.from];
            const to = positions[e.to];
            return (
              <line
                key={`e-${idx}`}
                className="tree-edge"
                x1={from.x + offsetX}
                y1={from.y + NODE_H / 2}
                x2={to.x + offsetX}
                y2={to.y - NODE_H / 2}
              />
            );
          })}
          {/* Nodos */}
          {positions.map((p) => {
            const cls = p.is_terminal ? "terminal" : "nonterminal";
            const textLen = p.label.length * 8 + 16;
            const rw = Math.max(NODE_W, textLen);
            return (
              <g key={p.id} className="tree-node-group">
                <rect
                  className={`tree-node-rect ${cls}`}
                  x={p.x + offsetX - rw / 2}
                  y={p.y - NODE_H / 2}
                  width={rw}
                  height={NODE_H}
                />
                <text
                  className={`tree-node-text ${cls}`}
                  x={p.x + offsetX}
                  y={p.y}
                >
                  {p.label}
                </text>
              </g>
            );
          })}
        </svg>
      </div>
      <div className="tree-controls">
        <button className="tree-control-btn" onClick={() => setScale((s) => Math.max(0.3, s - 0.15))}>
          −
        </button>
        <button className="tree-control-btn" onClick={() => setScale(1)}>
          1:1
        </button>
        <button className="tree-control-btn" onClick={() => setScale((s) => Math.min(2, s + 0.15))}>
          +
        </button>
      </div>
    </div>
  );
}
