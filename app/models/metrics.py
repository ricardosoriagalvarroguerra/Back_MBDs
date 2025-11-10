from sqlalchemy import Column, Text
from sqlalchemy.orm import relationship
from ..db.base import Base


class Metric(Base):
    __tablename__ = "metrics"

    metric_id = Column(Text, primary_key=True, nullable=False)
    metric_code = Column(Text, unique=True, nullable=True)
    metric_name = Column(Text, nullable=False)
    source = Column(Text, nullable=True)

    metric_values = relationship("MetricValue", back_populates="metric")
    moodys_ratings_daily = relationship("MoodysRatingDaily", back_populates="metric")
