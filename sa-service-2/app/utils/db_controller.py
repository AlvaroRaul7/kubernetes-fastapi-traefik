
from sqlalchemy.orm import Session
from models.models import rappiuser
from schemas.schema import UserCreate


class UserRepo:
    
 async def create(db: Session, user: UserCreate):
        db_item = rappiuser(name= user.name, lastname= user.lastname, address = user.address, phone = user.phone, age= user.age, hire_date = user.hire_date, fire_date = user.fire_date)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    
 def fetch_by_id(db: Session,_id):
     return db.query(rappiuser).filter(rappiuser.user_id == _id).first()
 
 def fetch_by_name(db: Session,name):
     return db.query(rappiuser).filter(rappiuser.name == name).first()
 
 def fetch_all(db: Session, skip: int = 0, limit: int = 100):
     return db.query(rappiuser).offset(skip).limit(limit).all()
 
 async def delete(db: Session,user_id):
     db_item= db.query(rappiuser).filter_by(user_id=user_id).first()
     db.delete(db_item)
     db.commit()
     
 async def update(db: Session,user_data):
    updated_user = db.merge(user_data)
    db.commit()
    return updated_user
    
    
  