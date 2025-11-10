from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models.metrics import Metric


def get_all_metrics(db: Session) -> list[Metric]:
    return db.execute(
        select(Metric).order_by(Metric.metric_id)
    ).scalars().all()


def get_metric_by_code(db: Session, metric_code: str) -> Metric | None:
    return db.execute(
        select(Metric).where(Metric.metric_code == metric_code)
    ).scalars().first()
