import os
from decimal import Decimal

import pytest

try:
    from fastapi.testclient import TestClient
except (RuntimeError, ModuleNotFoundError) as exc:  # pragma: no cover - optional dependency guard
    pytest.skip(str(exc), allow_module_level=True)

# Ensure required env vars for settings before the app is imported
os.environ.setdefault("POSTGRES_USER", "test_user")
os.environ.setdefault("POSTGRES_PASSWORD", "test_password")

from app.main import app  # noqa: E402  pylint: disable=wrong-import-position
from app.routers import mdbs, metrics, metric_values


@pytest.fixture(autouse=True)
def override_db_dependencies():
    """Prevent real database connections during the tests."""

    def _fake_get_db():
        yield None

    original_overrides = app.dependency_overrides.copy()
    app.dependency_overrides[mdbs.get_db] = _fake_get_db
    app.dependency_overrides[metrics.get_db] = _fake_get_db
    app.dependency_overrides[metric_values.get_db] = _fake_get_db
    try:
        yield
    finally:
        app.dependency_overrides = original_overrides


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_root_returns_json(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers.get("content-type", "").startswith("application/json")
    assert response.json() == {"status": "ok"}


def test_mdbs_endpoint_content_type(client, monkeypatch):
    monkeypatch.setattr(
        mdbs,
        "get_all_mdbs",
        lambda db: [
            {"mdb_id": 1, "mdb_code": "IDB", "mdb_name": "Inter-American Development Bank"},
        ],
    )
    response = client.get("/api/mdbs/")
    assert response.status_code == 200
    assert response.headers.get("content-type", "").startswith("application/json")
    data = response.json()
    assert data[0]["mdb_code"] == "IDB"


def test_metrics_endpoint_content_type(client, monkeypatch):
    monkeypatch.setattr(
        metrics,
        "get_all_metrics",
        lambda db: [
            {
                "metric_id": "gni",
                "metric_code": "GNI",
                "metric_name": "Gross National Income",
                "source": "World Bank",
            }
        ],
    )
    response = client.get("/api/metrics/")
    assert response.status_code == 200
    assert response.headers.get("content-type", "").startswith("application/json")
    payload = response.json()
    assert payload[0]["metric_id"] == "gni"


def test_metric_values_endpoint_content_type(client, monkeypatch):
    monkeypatch.setattr(
        metric_values,
        "get_values",
        lambda db, **_: [
            {"mdb_id": 1, "metric_id": "gni", "year": 2023, "value": Decimal("10.5")},
        ],
    )
    response = client.get("/api/metric-values/")
    assert response.status_code == 200
    assert response.headers.get("content-type", "").startswith("application/json")
    body = response.json()
    assert body[0]["value"] == "10.5"
