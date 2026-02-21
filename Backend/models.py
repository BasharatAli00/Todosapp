from database import Base
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey


class Users(Base):
    __tablename__='Users'
    ID=Column(Integer, primary_key=True, index=True)
    Username=Column(String, unique=True)
    Email=Column(String, unique=True)
    First_name= Column(String)
    Last_name=Column(String)
    Hashed_password=Column(String)
    Is_active=Column(Boolean, default=True)
    Role=Column(String)
    phone_number=Column(String)



class todosapp(Base):
    __tablename__='Todos'
    ID=Column(Integer, primary_key=True, index=True)
    Title=Column(String)
    Description= Column(String)
    Priority=Column(Integer)
    Complete=Column(Boolean, default=False)
    Owner_id=Column(Integer, ForeignKey('Users.ID'))
    
