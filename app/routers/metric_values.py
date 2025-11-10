import re
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Optional
from sqlalchemy.orm import Session
from ..db.session import SessionLocal
from ..crud.metric_values import get_values
from ..schemas.metric_values import MetricValue as MetricValueSchema

router = APIRouter(prefix="/metric-values", tags=["metric_values"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[MetricValueSchema])
def list_metric_values(
    mdb_id: Optional[list[int]] = Query(None, description="Puede repetirse el parámetro para filtrar múltiples MDBs"),
    metric_id: Optional[list[str]] = Query(None, description="Se puede repetir para filtrar múltiples métricas"),
    year: Optional[list[int]] = Query(None, description="Lista de años exactos a incluir"),
    year_from: Optional[int] = Query(None, ge=1900, le=2100, description="Incluye valores con year >= year_from"),
    year_to: Optional[int] = Query(None, ge=1900, le=2100, description="Incluye valores con year <= year_to"),
    limit: Optional[int] = Query(None, ge=1, le=20000, description="Número máximo de filas a devolver"),
    db: Session = Depends(get_db),
):
    if mdb_id is not None and any(val is not None and val < 1 for val in mdb_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los valores de mdb_id deben ser positivos",
        )
    metric_pattern = re.compile(r"^[A-Za-z0-9_\-\.]+$")
    if metric_id is not None:
        for raw in metric_id:
            if raw is None:
                continue
            value = str(raw).strip()
            if not value or len(value) > 64 or not metric_pattern.match(value):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cada metric_id debe cumplir el patrón ^[A-Za-z0-9_\\-\\.]+$",
                )
    if year is not None and any(val is not None and (val < 1900 or val > 2100) for val in year):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los valores de year deben estar entre 1900 y 2100",
        )
    return get_values(
        db,
        mdb_ids=mdb_id,
        metric_ids=metric_id,
        years=year,
        year_from=year_from,
        year_to=year_to,
        limit=limit,
    )
