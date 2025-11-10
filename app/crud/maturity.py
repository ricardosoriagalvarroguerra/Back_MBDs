from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models.maturity import Maturity


def get_maturity_rows(
    db: Session,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[Maturity]:
    stmt = select(Maturity)
    if start_date is not None:
        stmt = stmt.where(Maturity.date >= start_date)
    if end_date is not None:
        stmt = stmt.where(Maturity.date <= end_date)
    stmt = stmt.order_by(Maturity.date)
    return db.execute(stmt).scalars().all()
