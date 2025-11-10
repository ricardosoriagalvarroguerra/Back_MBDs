from sqlalchemy.orm import Session
from typing import Iterable, Sequence
from sqlalchemy import select
from ..models.metric_values import MetricValue


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


def get_values(
    db: Session,
    mdb_ids: Sequence[int] | None = None,
    metric_ids: Sequence[str] | None = None,
    years: Sequence[int] | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
    limit: int | None = None,
) -> list[MetricValue]:
    stmt = select(MetricValue)

    normalized_mdb_ids = _normalize_ints(mdb_ids)
    if normalized_mdb_ids:
        stmt = stmt.where(MetricValue.mdb_id.in_(normalized_mdb_ids))

    normalized_metric_ids = _normalize_strs(metric_ids)
    if normalized_metric_ids:
        stmt = stmt.where(MetricValue.metric_id.in_(normalized_metric_ids))

    normalized_years = _normalize_ints(years)
    if normalized_years:
        stmt = stmt.where(MetricValue.year.in_(normalized_years))
    else:
        if year_from is not None:
            stmt = stmt.where(MetricValue.year >= int(year_from))
        if year_to is not None:
            stmt = stmt.where(MetricValue.year <= int(year_to))

    stmt = stmt.order_by(MetricValue.mdb_id, MetricValue.metric_id, MetricValue.year)

    if limit is not None and limit > 0:
        stmt = stmt.limit(int(limit))

    return db.execute(stmt).scalars().all()
