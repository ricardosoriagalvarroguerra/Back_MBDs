from sqlalchemy import BigInteger, Column, Text
from sqlalchemy.orm import relationship
from ..db.base import Base


class Mdb(Base):
    __tablename__ = "mdbs"

    mdb_id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    mdb_code = Column(Text, unique=True, nullable=True)
    mdb_name = Column(Text, nullable=False)

    metric_values = relationship("MetricValue", back_populates="mdb")
    moodys_ratings_daily = relationship("MoodysRatingDaily", back_populates="mdb")
