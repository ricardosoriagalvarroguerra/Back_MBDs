# Backend FastAPI

## Requisitos
- Python 3.11+
- PostgreSQL en `localhost:5433` (DB `indicadores_financieros`)

## Configuración

```bash
cd "Moodys_S&P/backend"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Crea/ajusta `.env` (ya creado):

- POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
- API_PREFIX (por defecto `/api`)
- ALLOWED_ORIGINS (CSV)

## Ejecutar

```bash
cd "Moodys_S&P/backend"
python uvicorn_app.py
```

La API estará en `http://localhost:8000` y endpoints en `http://localhost:8000/api`.
- GET `/api/mdbs/`
- GET `/api/metrics/`
- GET `/api/metrics/by-code?metric_code=...`
- GET `/api/metric-values/?mdb_id=...&metric_id=...&year=...`

## Deploy en Railway

Opción recomendada: 1 servicio para el backend (Python) y otro para el frontend (Static Site).

1) Backend (Python/FastAPI)
- Crea un nuevo servicio apuntando al subdirectorio `backend`.
- Build: `pip install -r requirements.txt`
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Variables de entorno:
  - Usa `DATABASE_URL` del plugin de PostgreSQL (o configura `POSTGRES_HOST/PORT/DB/USER/PASSWORD`).
  - `API_PREFIX=/api`
  - `ALLOWED_ORIGINS=https://<frontend>.up.railway.app`

2) Base de datos
- Añade el plugin de PostgreSQL en Railway y conéctalo al servicio backend.
- La app soporta `DATABASE_URL` automáticamente (coerciona a `postgresql+psycopg`).

- Crea un servicio de Static Site apuntando al subdirectorio `frontend`.
- Build Command: `npm ci && npm run build`
- Publish Directory: `dist`
- Env: define `VITE_API_BASE_URL=https://<backend>.up.railway.app/api` (u otro dominio si el backend vive en otra ruta o dominio).
- Incluye SPA fallback vía `frontend/static.json`.

Comprueba siempre que el backend sirva los endpoints públicos esperados (`/api/mdbs/`, `/api/metrics/`, `/api/metric-values/`, etc.) y que las respuestas incluyan la cabecera `Content-Type: application/json` junto con JSON válido. Cualquier respuesta HTML hará que el frontend vuelva a mostrar el error de conexión.

Notas
- Ajusta CORS con `ALLOWED_ORIGINS` al dominio del frontend en Railway.
- Revisa `backend/.env.example` y `frontend/.env.example` para ejemplos de configuración.
