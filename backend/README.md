# Backend – CFG Boolean Expression Analyzer

API REST para el análisis de expresiones lógicas booleanas mediante una Gramática Libre de Contexto.

## Requisitos

- Python 3.11+
- pip

## Instalación

```bash
cd backend
pip install -r requirements.txt
```

## Ejecución

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

El servidor estará disponible en `http://localhost:8000`.

Documentación interactiva (Swagger UI): `http://localhost:8000/docs`

## Endpoints

| Método | Ruta       | Descripción                              |
|--------|-----------|------------------------------------------|
| POST   | /analyze  | Analiza una expresión booleana           |
| GET    | /grammar  | Retorna la definición formal de la CFG   |
| GET    | /examples | Retorna las expresiones de ejemplo       |
| GET    | /health   | Health check                             |

## Ejemplo de uso

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"expression": "~(A | B) & (C | ~D)"}'
```

## Ejecutar pruebas

```bash
cd backend
python -m pytest tests/ -v
```

## Estructura

```
backend/
├── app/
│   ├── api/routes.py          # Endpoints REST
│   ├── services/analyzer.py   # Servicio de análisis
│   ├── parsers/
│   │   ├── tokenizer.py       # Analizador léxico
│   │   └── parser.py          # Parser descendente recursivo
│   ├── grammars/
│   │   ├── cfg.py             # Definición formal de la CFG
│   │   └── sample_expressions.py  # Registro de expresiones
│   ├── models/
│   │   ├── tree.py            # Nodos del árbol sintáctico
│   │   └── schemas.py         # Esquemas Pydantic
│   ├── utils/derivation.py    # Generador de derivaciones
│   └── main.py                # Punto de entrada FastAPI
├── tests/
│   └── test_analyzer.py       # Pruebas unitarias
└── requirements.txt
```
