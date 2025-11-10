from sqlalchemy import Column, Date, Numeric
from ..db.base import Base


class Maturity(Base):
    __tablename__ = "maturity"

    date = Column("Date", Date, primary_key=True, nullable=False)
    year_1 = Column("1 Year", Numeric, nullable=True, key="year_1")
    year_2 = Column("2 Year", Numeric, nullable=True, key="year_2")
    year_3 = Column("3 Year", Numeric, nullable=True, key="year_3")
    year_4 = Column("4 Year", Numeric, nullable=True, key="year_4")
    year_5 = Column("5 Year", Numeric, nullable=True, key="year_5")
    year_6 = Column("6 Year", Numeric, nullable=True, key="year_6")
    year_7 = Column("7 Year", Numeric, nullable=True, key="year_7")
    year_8 = Column("8 Year", Numeric, nullable=True, key="year_8")
    year_9 = Column("9 Year", Numeric, nullable=True, key="year_9")
    year_10 = Column("10 Year", Numeric, nullable=True, key="year_10")
    year_11 = Column("11 Year", Numeric, nullable=True, key="year_11")
    year_12 = Column("12 Year", Numeric, nullable=True, key="year_12")
    year_13 = Column("13 Year", Numeric, nullable=True, key="year_13")
    year_14 = Column("14 Year", Numeric, nullable=True, key="year_14")
    year_15 = Column("15 Year", Numeric, nullable=True, key="year_15")
