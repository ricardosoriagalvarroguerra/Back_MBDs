from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .routers import mdbs, metrics, metric_values, moodys_ratings_daily, maturity, rating, wabr_wasr
from .routers import health

app = FastAPI(title="Indicadores Financieros API")

# CORS: si no hay orígenes definidos, por defecto no permitir todos
_origins = settings.allowed_origins or [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix=settings.api_prefix)
app.include_router(mdbs.router, prefix=settings.api_prefix)
app.include_router(metrics.router, prefix=settings.api_prefix)
app.include_router(metric_values.router, prefix=settings.api_prefix)
app.include_router(moodys_ratings_daily.router, prefix=settings.api_prefix)
app.include_router(maturity.router, prefix=settings.api_prefix)
app.include_router(rating.router, prefix=settings.api_prefix)
app.include_router(wabr_wasr.router, prefix=settings.api_prefix)


@app.get("/")
async def root():
    return {"status": "ok"}
