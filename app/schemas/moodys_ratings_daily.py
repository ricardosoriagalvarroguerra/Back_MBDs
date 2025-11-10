from datetime import date
from decimal import Decimal
from pydantic import BaseModel


class MoodysRatingDaily(BaseModel):
    mdb_id: int
    metric_id: str
    rating_date: date
    value: Decimal | None = None

    class Config:
        from_attributes = True
