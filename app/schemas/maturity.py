from datetime import date
from decimal import Decimal
from pydantic import BaseModel


class Maturity(BaseModel):
    date: date
    year_1: Decimal | None = None
    year_2: Decimal | None = None
    year_3: Decimal | None = None
    year_4: Decimal | None = None
    year_5: Decimal | None = None
    year_6: Decimal | None = None
    year_7: Decimal | None = None
    year_8: Decimal | None = None
    year_9: Decimal | None = None
    year_10: Decimal | None = None
    year_11: Decimal | None = None
    year_12: Decimal | None = None
    year_13: Decimal | None = None
    year_14: Decimal | None = None
    year_15: Decimal | None = None

    class Config:
        from_attributes = True
