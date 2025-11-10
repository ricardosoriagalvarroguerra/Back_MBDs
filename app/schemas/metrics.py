from pydantic import BaseModel


class Metric(BaseModel):
    metric_id: str
    metric_code: str | None = None
    metric_name: str
    source: str | None = None

    class Config:
        from_attributes = True
