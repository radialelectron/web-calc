from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String

from database import Base


class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)
    expression = Column(String, nullable=False)
    result = Column(Float, nullable=False)
    mode = Column(String, nullable=False, default="standard")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
