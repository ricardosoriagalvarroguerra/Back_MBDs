from __future__ import annotations

import re
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session

from ..db.session import SessionLocal
from ..crud.wabr_wasr import get_wabr_wasr_values


router = APIRouter(prefix="/wabr-wasr", tags=["wabr-wasr"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def list_wabr_wasr(
    response: Response,
    metric: Optional[list[str]] = Query(None, description="WABR y/o WASR (por defecto ambas)"),
    metric_id: Optional[list[str]] = Query(None, description="alias de metric: WABR y/o WASR"),
    mdb_id: Optional[list[int]] = Query(None, description="Puede repetirse para filtrar múltiples MDBs"),
    year: Optional[list[int]] = Query(None, description="Lista de años exactos a incluir"),
    year_from: Optional[int] = Query(None, ge=1900, le=2100, description="Incluye valores con year >= year_from"),
    year_to: Optional[int] = Query(None, ge=1900, le=2100, description="Incluye valores con year <= year_to"),
    limit: Optional[int] = Query(None, ge=1, le=20000, description="Número máximo de filas a devolver"),
    db: Session = Depends(get_db),
):
    if mdb_id is not None and any(val is not None and val < 1 for val in mdb_id):
        raise HTTPException(status_code=400, detail="Los valores de mdb_id deben ser positivos")
    if year is not None and any(val is not None and (val < 1900 or val > 2100) for val in year):
        raise HTTPException(status_code=400, detail="Los valores de year deben estar entre 1900 y 2100")
    metrics_in = metric if metric is not None else metric_id
    if metrics_in is not None:
        pat = re.compile(r"^(WABR|WASR)$", re.IGNORECASE)
        for v in metrics_in:
            if v is None or not pat.match(str(v).strip()):
                raise HTTPException(status_code=400, detail="metric debe ser WABR y/o WASR")

    response.headers["Cache-Control"] = "public, max-age=300"
    data = get_wabr_wasr_values(
        db,
        metrics=metrics_in,
        mdb_ids=mdb_id,
        years=year,
        year_from=year_from,
        year_to=year_to,
        limit=limit,
    )
    return data


