from __future__ import annotations

from typing import Iterable, Sequence
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


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
        if not value:
            continue
        value_up = value.upper()
        if value_up not in seen:
            seen.add(value_up)
            result.append(value_up)
    return result


def _build_in_clause(prefix: str, values: Sequence[int]) -> tuple[str | None, dict[str, int]]:
    if not values:
        return None, {}
    names: list[str] = []
    params: dict[str, int] = {}
    for i, v in enumerate(values):
        key = f"{prefix}_{i}"
        names.append(f":{key}")
        params[key] = int(v)
    return ", ".join(names), params


def get_wabr_wasr_values(
    db: Session,
    metrics: Sequence[str] | None = None,
    mdb_ids: Sequence[int] | None = None,
    years: Sequence[int] | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
    limit: int | None = None,
) -> list[dict]:
    target_metrics = _normalize_strs(metrics) or ["WABR", "WASR"]
    # Limitar estrictamente a métricas permitidas
    target_metrics = [m for m in target_metrics if m in ("WABR", "WASR")]
    if not target_metrics:
        return []

    normalized_mdb_ids = _normalize_ints(mdb_ids)
    normalized_years = _normalize_ints(years)

    results: list[dict] = []

    for metric in target_metrics:
        # Probar variantes de nombre de tabla: no citado minúsculas (convención Postgres) y citado tal como está
        table_candidates = [
            f"public.{metric.lower()}",
            f'public."{metric}"',
        ]

        last_error: SQLAlchemyError | None = None
        fetched_any = False
        for table_qualified in table_candidates:
            base_sql = [
                "SELECT",
                "  m.mdb_id AS mdb_id,",
                "  :metric_id AS metric_id,",
                "  w.year AS year,",
                "  w.rating_ord AS value,",
                "  w.rating_text AS rating_text",
                f"FROM {table_qualified} AS w",
                "JOIN mdbs AS m ON UPPER(TRIM(m.mdb_code)) = UPPER(TRIM(w.mdb_code))",
                "WHERE 1=1",
            ]

            params: dict[str, object] = {"metric_id": metric}

            if normalized_mdb_ids:
                in_clause, in_params = _build_in_clause("mdb_id", normalized_mdb_ids)
                if in_clause:
                    base_sql.append(f"AND m.mdb_id IN ({in_clause})")
                    params.update(in_params)

            if normalized_years:
                in_clause, in_params = _build_in_clause("year", normalized_years)
                if in_clause:
                    base_sql.append(f"AND w.year IN ({in_clause})")
                    params.update(in_params)
            else:
                if year_from is not None:
                    base_sql.append("AND w.year >= :year_from")
                    params["year_from"] = int(year_from)
                if year_to is not None:
                    base_sql.append("AND w.year <= :year_to")
                    params["year_to"] = int(year_to)

            base_sql.append("ORDER BY m.mdb_id, w.year")
            if limit is not None and limit > 0:
                base_sql.append("LIMIT :limit")
                params["limit"] = int(limit)

            sql = "\n".join(base_sql)
            try:
                rows = db.execute(text(sql), params).mappings().all()
                for r in rows:
                    results.append({
                        "mdb_id": int(r.get("mdb_id")),
                        "metric_id": str(r.get("metric_id")),
                        "year": int(r.get("year")),
                        "value": r.get("value"),
                        "rating_text": r.get("rating_text"),
                    })
                fetched_any = True
                break
            except SQLAlchemyError as exc:  # intentar con la siguiente variante
                last_error = exc
                continue

        # si no se pudo con ninguna variante, propagar el último error
        if not fetched_any and last_error is not None:
            raise last_error

    # Ordenar consistentemente
    results.sort(key=lambda x: (x["mdb_id"], x["metric_id"], x["year"]))
    return results


