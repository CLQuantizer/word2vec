from sqlalchemy.orm import Session
import models, schemas

def get_writings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Writing).offset(skip).limit(limit).all()

def create_writing(db: Session, writing: schemas.WritingCreate):
    db_writing = models.Writing(**writing.dict())
    db.add(db_writing)
    db.commit()
    db.refresh(db_writing)
    return db_writing
