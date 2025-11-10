from sqlalchemy import Column, Date, Numeric
from ..db.base import Base


class Rating(Base):
    __tablename__ = "rating"

    date = Column("Date", Date, primary_key=True, nullable=False)
    aaa = Column("Aaa", Numeric, nullable=True, key="aaa")
    aa1 = Column("Aa1", Numeric, nullable=True, key="aa1")
    aa2 = Column("Aa2", Numeric, nullable=True, key="aa2")
    aa3 = Column("Aa3", Numeric, nullable=True, key="aa3")
    a1 = Column("A1", Numeric, nullable=True, key="a1")
    a2 = Column("A2", Numeric, nullable=True, key="a2")
    a3 = Column("A3", Numeric, nullable=True, key="a3")
    baa1 = Column("Baa1", Numeric, nullable=True, key="baa1")
    baa2 = Column("Baa2", Numeric, nullable=True, key="baa2")
    baa3 = Column("Baa3", Numeric, nullable=True, key="baa3")
    ba1 = Column("Ba1", Numeric, nullable=True, key="ba1")
    ba2 = Column("Ba2", Numeric, nullable=True, key="ba2")
    ba3 = Column("Ba3", Numeric, nullable=True, key="ba3")
    b1 = Column("B1", Numeric, nullable=True, key="b1")
    b2 = Column("B2", Numeric, nullable=True, key="b2")
    b3 = Column("B3", Numeric, nullable=True, key="b3")
    caa_c = Column("Caa_C", Numeric, nullable=True, key="caa_c")
