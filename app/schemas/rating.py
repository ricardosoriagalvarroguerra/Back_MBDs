from datetime import date
from decimal import Decimal
from pydantic import BaseModel


class Rating(BaseModel):
    date: date
    aaa: Decimal | None = None
    aa1: Decimal | None = None
    aa2: Decimal | None = None
    aa3: Decimal | None = None
    a1: Decimal | None = None
    a2: Decimal | None = None
    a3: Decimal | None = None
    baa1: Decimal | None = None
    baa2: Decimal | None = None
    baa3: Decimal | None = None
    ba1: Decimal | None = None
    ba2: Decimal | None = None
    ba3: Decimal | None = None
    b1: Decimal | None = None
    b2: Decimal | None = None
    b3: Decimal | None = None
    caa_c: Decimal | None = None

    class Config:
        from_attributes = True
