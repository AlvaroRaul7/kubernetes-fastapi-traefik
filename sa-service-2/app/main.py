
import sys
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
import socket
from services.connect_db import get_db
from fastapi.encoders import jsonable_encoder
import models.models as models
import schemas.schema as schemas
from utils.db_controller import UserRepo,UserCreate
from sqlalchemy.orm import Session
import uvicorn
from typing import List,Optional








app = FastAPI()
hostname = socket.gethostname()
version = f"{sys.version_info.major}.{sys.version_info.minor}"







@app.get("/")
async def read_root():

    " Hello FastApi, useful when recognizing which pod is executing the service"
    return {
        "name": "service-two",
        "host": hostname,
        "version": f"Hello world! From FastAPI running on Uvicorn with Gunicorn in Alpine. Using Python {version}",
        "connection": "hi"
    }


@app.post('/users', tags=["User"],response_model=schemas.User,status_code=201)
async def create_user(user_request: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create an User and store it in the database
    """
    
    db_item = UserRepo.fetch_by_name(db, name=user_request.name)
    if db_item:
        raise HTTPException(status_code=400, detail="User already exists!")

    return await UserRepo.create(db=db, user=user_request)

@app.get("/users",  tags=["User"])
async def get_users(name: Optional[str] = None,db: Session = Depends(get_db)):
    "Get all users or retrieve a user by name using query strings"
    if name:
        items =[]
        db_item = UserRepo.fetch_by_name(db,name)
        items.append(db_item)
        return items
    
    else:
        list_users =[]
        user = UserRepo.fetch_all(db)
        print(user)

        list_users.append(user)
        return list_users

@app.get('/users/{user_id}', tags=["User"],response_model=schemas.User)
def get_user(user_id: int,db: Session = Depends(get_db)):
    """
    Get the User  with the given ID provided by the database
    """
    db_user = UserRepo.fetch_by_id(db,user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found with the given ID")
    return db_user


@app.delete('/users/{user_id}', tags=["User"])
async def delete_user(user_id: int,db: Session = Depends(get_db)):
    """
    Delete the User with the given ID provided by the database
    """
    db_user = UserRepo.fetch_by_id(db,user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found with the given ID")
    await UserRepo.delete(db,user_id)
    return "User deleted successfully!"


@app.put('/users/{user_id}', tags=["User"],response_model=schemas.User)
async def update_user(user_id: int,user_request: schemas.User, db: Session = Depends(get_db)):
    """
    Update an User and  store it in the database
    """
    user = UserRepo.fetch_by_id(db, user_id)
    if user:
        update_item_encoded = jsonable_encoder(user_request)
        user.name = update_item_encoded['name']
        user.lastname =update_item_encoded['lastname']
        user.phone = update_item_encoded['phone']
        user.address = update_item_encoded['address']
        user.age = update_item_encoded['age']
        user.hire_date = update_item_encoded['hire_date']
        user.fire_date = update_item_encoded['fire_date']
        return await UserRepo.update(db=db, user_data=user)
    else:
        raise HTTPException(status_code=400, detail="Item not found with the given ID")
    