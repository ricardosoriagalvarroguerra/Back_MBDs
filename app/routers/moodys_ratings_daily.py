import re
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from ..db.session import SessionLocal
from ..crud.moodys_ratings_daily import get_moodys_ratings_daily
from ..schemas.moodys_ratings_daily import MoodysRatingDaily as MoodysRatingDailySchema

router = APIRouter(prefix="/moodys-ratings-daily", tags=["moodys_ratings_daily"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[MoodysRatingDailySchema])
def list_moodys_ratings_daily(
    mdb_id: list[int] | None = Query(None, description="Puede repetirse para filtrar múltiples MDBs"),
    metric_id: list[str] | None = Query(None, description="Puede repetirse para filtrar múltiples métricas"),
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    db: Session = Depends(get_db),
):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date must be before or equal to end_date",
        )
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
    return get_moodys_ratings_daily(
        db,
        mdb_ids=mdb_id,
        metric_ids=metric_id,
        start_date=start_date,
        end_date=end_date,
    )
