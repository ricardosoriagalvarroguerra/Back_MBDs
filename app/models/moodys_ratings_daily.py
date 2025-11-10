from sqlalchemy import BigInteger, Column, Date, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from ..db.base import Base


class MoodysRatingDaily(Base):
    __tablename__ = "moodys_ratings_daily"

    mdb_id = Column(BigInteger, ForeignKey("mdbs.mdb_id"), primary_key=True, nullable=False)
    metric_id = Column(Text, ForeignKey("metrics.metric_id"), primary_key=True, nullable=False)
    rating_date = Column(Date, primary_key=True, nullable=False)
    value = Column(Numeric, nullable=True)

    mdb = relationship("Mdb", back_populates="moodys_ratings_daily")
    metric = relationship("Metric", back_populates="moodys_ratings_daily")
