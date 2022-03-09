from datetime import date
from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    user_id: Optional[int]
    name: Optional[str]
    lastname: Optional[str]
    address: Optional[str]
    phone: Optional[int]
    age: Optional[int]
    hire_date: Optional[date]
    fire_date: Optional[date]


class UserCreate(UserBase):
    pass


class User(UserBase):
    user_id: Optional[int]

    class Config:
        orm_mode = True