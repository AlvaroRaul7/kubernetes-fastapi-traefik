from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class rappiuser(Base):
    __tablename__ = 'rappiuser'

    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    lastname = Column(String)
    address = Column(String)
    phone = Column(Integer)
    age = Column(Integer)
    hire_date = Column(Date)
    fire_date = Column(Date)

    def __repr__(self):
       return "<User(name='%s', lastname='%s', address='%s')>" % (self.name, self.lastname, self.address)