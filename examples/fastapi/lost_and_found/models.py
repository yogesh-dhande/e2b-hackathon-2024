from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class LostItem(Base):
    __tablename__ = "lost_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    location = Column(String)
    lost_date = Column(DateTime)
