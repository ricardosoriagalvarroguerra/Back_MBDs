from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models.rating import Rating


def get_rating_rows(
    db: Session,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[Rating]:
    stmt = select(Rating)
    if start_date is not None:
        stmt = stmt.where(Rating.date >= start_date)
    if end_date is not None:
        stmt = stmt.where(Rating.date <= end_date)
    stmt = stmt.order_by(Rating.date)
    return db.execute(stmt).scalars().all()
