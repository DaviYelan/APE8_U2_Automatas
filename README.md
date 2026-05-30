# APE_08_Automatas

**Construcción y Validación de Gramáticas Libres de Contexto (CFG)**

Práctica Nro. 8 – Teoría de Autómatas y Computabilidad Avanzada  
Universidad Nacional de Loja – FEIRNNR – Carrera de Computación

Por: Luis Armijos, Anthony Gutierrez y Alexis Roman - 6 Ciclo

---

## Descripción

Aplicación web que analiza expresiones lógicas booleanas utilizando una Gramática Libre de Contexto (CFG). La aplicación realiza:

- **Tokenización** (análisis léxico)
- **Validación sintáctica** mediante un parser descendente recursivo
- **Generación de derivaciones** por la izquierda y por la derecha
- **Construcción y visualización** del árbol sintáctico (Parse Tree)
- **Detección de errores** sintácticos detallados

## Gramática Libre de Contexto

```
G = (V, Σ, R, S)

V = { Exp, Term, Factor }
Σ = { id, |, &, ~, (, ) }
S = Exp

Reglas de producción:
  Exp    → Exp | Term  |  Term
  Term   → Term & Factor  |  Factor
  Factor → ~ Factor  |  ( Exp )  |  id
```

**Precedencia** (de menor a mayor): OR (`|`) < AND (`&`) < NOT (`~`)

---

## Estructura del Proyecto

```
APE_08_Automatas/
│
├── backend/
│   ├── app/
│   │   ├── api/routes.py              # Endpoints REST
│   │   ├── services/analyzer.py       # Orquestador del análisis
│   │   ├── parsers/
│   │   │   ├── tokenizer.py           # Analizador léxico
│   │   │   └── parser.py              # Parser descendente recursivo
│   │   ├── grammars/
│   │   │   ├── cfg.py                 # Definición formal de la CFG
│   │   │   └── sample_expressions.py  # Registro de expresiones ejemplo
│   │   ├── models/
│   │   │   ├── tree.py                # Clase ParseTreeNode
│   │   │   └── schemas.py             # Esquemas Pydantic (request/response)
│   │   ├── utils/derivation.py        # Generador de derivaciones
│   │   └── main.py                    # Entrada FastAPI
│   ├── tests/test_analyzer.py         # 25 pruebas unitarias
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ExpressionInput.jsx    # Campo de entrada
│   │   │   ├── TokenList.jsx          # Visualización de tokens
│   │   │   ├── DerivationDisplay.jsx  # Pasos de derivación
│   │   │   ├── ValidationStatus.jsx   # Estado de validación
│   │   │   └── ParseTreeView.jsx      # Árbol SVG interactivo
│   │   ├── services/api.js            # Comunicación con backend
│   │   ├── styles/                    # CSS modular por componente
│   │   ├── App.jsx                    # Componente raíz
│   │   └── main.jsx                   # Punto de entrada
│   ├── package.json
│   └── vite.config.js
│
└── README.md                          # Este archivo
```

---

## Instrucciones de Ejecución

### Requisitos Previos

- Python 3.11+
- Node.js 18+
- npm

### 1. Backend

```bash
# Entrar al directorio del backend
cd APE_08_Automatas/backend

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor
uvicorn app.main:app --reload --port 8000
```

El backend estará en: `http://localhost:8000`  
Documentación Swagger: `http://localhost:8000/docs`

### 2. Frontend

```bash
# Entrar al directorio del frontend (en otra terminal)
cd APE_08_Automatas/frontend

# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
npm run dev
```

El frontend estará en: `http://localhost:5173`

### 3. Ejecutar Pruebas

```bash
cd APE_08_Automatas/backend
python -m pytest tests/ -v
```

---

## Ejemplos de Uso

### Desde la interfaz web

1. Abrir `http://localhost:5173` en el navegador
2. Escribir una expresión booleana: `~(A | B) & (C | ~D)`
3. Presionar "Analizar"
4. Ver los resultados: tokens, derivaciones, validación y árbol

### Desde la API REST

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"expression": "~(A | B) & (C | ~D)"}'
```

**Respuesta:**
```json
{
  "valid": true,
  "tokens": [
    {"type": "NOT", "value": "~", "position": 0},
    {"type": "LPAREN", "value": "(", "position": 1},
    {"type": "ID", "value": "A", "position": 2},
    ...
  ],
  "left_derivation": [
    "Exp",
    "Term",
    "Term & Factor",
    "Factor & Factor",
    "~ Factor & Factor",
    "~ ( Exp ) & Factor",
    "~ ( Exp | Term ) & Factor",
    ...
  ],
  "right_derivation": [...],
  "parse_tree": { "symbol": "Exp", "children": [...] },
  "message": "Cadena válida según la gramática CFG"
}
```

---

## Cómo Agregar Nuevas Expresiones

Pueden agregar nuevas expresiones **sin modificar el parser ni la lógica del sistema**. Solo hay que editar un archivo:

### Archivo: `backend/app/grammars/sample_expressions.py`

Agregar al final del archivo:

```python
register_expression(SampleExpression(
    name="Mi expresión",
    expression="(A & B) | (C & D)",
    description="OR de dos conjunciones",
    tags=["AND", "OR"],
))
```

¡Eso es todo! La nueva expresión aparecerá automáticamente:
- En la API (`GET /examples`)
- En los chips de ejemplo del frontend
- Lista para ser analizada con todas las funcionalidades

### Pasos detallados:

1. Abrir `backend/app/grammars/sample_expressions.py`
2. Buscar la sección "ESPACIO RESERVADO PARA NUEVAS EXPRESIONES"
3. Copiar y pegar el bloque de ejemplo
4. Modificar los campos `name`, `expression`, `description` y `tags`
5. Guardar el archivo
6. Reiniciar el backend (si no tiene `--reload`)

**No es necesario:**
- Modificar el parser
- Modificar la API
- Modificar el frontend
- Crear nuevos archivos

---

## Arquitectura

### Backend

- **FastAPI** como framework web con documentación automática
- **Pydantic** para validación de datos de entrada/salida
- **Parser descendente recursivo** que elimina internamente la recursión izquierda pero construye el árbol con la gramática original
- **Módulo de derivaciones** que genera derivaciones recorriendo el árbol de derivación concreto

### Frontend

- **React + Vite** para desarrollo rápido
- **SVG personalizado** para renderizar el árbol sintáctico
- **CSS modular** organizado por componente
- **Diseño responsivo** adaptable a distintos tamaños de pantalla

---

## Tecnologías

| Componente | Tecnología |
|-----------|-----------|
| Backend   | Python 3.11+, FastAPI, Pydantic, Uvicorn |
| Frontend  | React, Vite, JavaScript, CSS |
| Testing   | pytest |
