


import os 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
  

try: 
    
    engine = create_engine('postgresql+psycopg2://postgres:postgres@postgres-ip-service/users', pool_pre_ping=True)
    print(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    
except:

    print("error connecting to the database")



# Dependency
def get_db():
    db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    
    try:
        yield db
    finally:
        db.close()
