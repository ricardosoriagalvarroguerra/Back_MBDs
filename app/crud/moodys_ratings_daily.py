from datetime import date
from typing import Iterable, Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models.moodys_ratings_daily import MoodysRatingDaily


def _normalize_ints(values: Iterable[int | None] | None) -> list[int]:
    if not values:
        return []
    seen: set[int] = set()
    result: list[int] = []
    for raw in values:
        if raw is None:
            continue
        value = int(raw)
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def _normalize_strs(values: Iterable[str | None] | None) -> list[str]:
    if not values:
        return []
    seen: set[str] = set()
    result: list[str] = []
    for raw in values:
        if raw is None:
            continue
        value = str(raw).strip()
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def get_moodys_ratings_daily(
    db: Session,
    mdb_ids: Sequence[int] | None = None,
    metric_ids: Sequence[str] | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[MoodysRatingDaily]:
    stmt = select(MoodysRatingDaily)

    normalized_mdb_ids = _normalize_ints(mdb_ids)
    if normalized_mdb_ids:
        stmt = stmt.where(MoodysRatingDaily.mdb_id.in_(normalized_mdb_ids))

    normalized_metric_ids = _normalize_strs(metric_ids)
    if normalized_metric_ids:
        stmt = stmt.where(MoodysRatingDaily.metric_id.in_(normalized_metric_ids))

    if start_date is not None:
        stmt = stmt.where(MoodysRatingDaily.rating_date >= start_date)
    if end_date is not None:
        stmt = stmt.where(MoodysRatingDaily.rating_date <= end_date)

    stmt = stmt.order_by(
        MoodysRatingDaily.mdb_id,
        MoodysRatingDaily.metric_id,
        MoodysRatingDaily.rating_date,
    )

    return db.execute(stmt).scalars().all()
