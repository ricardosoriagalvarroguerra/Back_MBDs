from pydantic import BaseModel
from decimal import Decimal


class MetricValue(BaseModel):
    mdb_id: int
    metric_id: str
    year: int
    value: Decimal | None = None

    class Config:
        from_attributes = True
