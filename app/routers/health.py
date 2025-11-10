from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from ..db.session import engine

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/ping")
def ping():
    return {"status": "ok"}


@router.get("/db")
def db_healthcheck():
    try:
        with engine.connect() as conn:
            value = conn.execute(text("SELECT 1")).scalar_one()
            return {"db": "ok", "result": int(value)}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"DB connection failed: {exc}")
