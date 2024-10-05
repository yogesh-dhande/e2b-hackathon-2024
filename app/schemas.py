from pydantic import BaseModel
from datetime import datetime

class LostItemCreate(BaseModel):
    name: str
    description: str
    location: str
    lost_date: datetime

    class Config:
        from_attributes = True  # In Pydantic v2, use `from_attributes` instead of `orm_mode`

class LostItemResponse(BaseModel):
    id: int
    name: str
    description: str
    location: str
    lost_date: datetime

    class Config:
        from_attributes = True
