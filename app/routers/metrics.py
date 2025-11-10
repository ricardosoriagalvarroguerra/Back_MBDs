from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session
from ..db.session import SessionLocal
from ..crud.metrics import get_all_metrics, get_metric_by_code
from ..schemas.metrics import Metric as MetricSchema

router = APIRouter(prefix="/metrics", tags=["metrics"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[MetricSchema])
def list_metrics(response: Response, db: Session = Depends(get_db)):
    response.headers["Cache-Control"] = "public, max-age=300"
    return get_all_metrics(db)


@router.get("/by-code", response_model=MetricSchema | None)
def get_by_code(
    metric_code: str = Query(
        ...,
        min_length=1,
        max_length=64,
        pattern=r"^[A-Za-z0-9_\-\.]+$",
        description="Unique metric_code",
    ),
    db: Session = Depends(get_db),
):
    return get_metric_by_code(db, metric_code)
