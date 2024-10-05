from sqlalchemy.orm import Session
from . import models, schemas

def create_lost_item(db: Session, item: schemas.LostItemCreate):
    db_item = models.LostItem(**item.dict())  # Convert Pydantic model to dictionary
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session):
    return db.query(models.LostItem).all()
