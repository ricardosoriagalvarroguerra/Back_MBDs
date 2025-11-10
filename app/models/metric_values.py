from sqlalchemy import BigInteger, Column, ForeignKey, Integer, Numeric, Text
from sqlalchemy.orm import relationship
from ..db.base import Base


class MetricValue(Base):
    __tablename__ = "metric_values"

    mdb_id = Column(BigInteger, ForeignKey("mdbs.mdb_id"), primary_key=True, nullable=False)
    metric_id = Column(Text, ForeignKey("metrics.metric_id"), primary_key=True, nullable=False)
    year = Column(Integer, primary_key=True, nullable=False)
    value = Column(Numeric, nullable=True)

    mdb = relationship("Mdb", back_populates="metric_values")
    metric = relationship("Metric", back_populates="metric_values")
