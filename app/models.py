from app.database import Base
from sqlalchemy import Column,String,Boolean,Integer,Float,TIMESTAMP,ForeignKey
from datetime import datetime
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import Relationship

class Expense(Base):
   __tablename__="expense"
   id=Column(Integer,primary_key=True,nullable=False)
   title=Column(String,nullable=False)
   amount=Column(Float,nullable=False)
   category=Column(String,nullable=False)
   description=Column(String,nullable=False)
   created_at=Column(TIMESTAMP(timezone=True),nullable=True,default=text("now()"))
   owner_id=Column(Integer,ForeignKey("users.id"),nullable=False)
   owner=Relationship("User")
   


class User(Base):
   __tablename__="users"
   id=Column(Integer,primary_key=True,nullable=False)   
   email=Column(String,nullable=False)
   password=Column(String,nullable=False)
   created_at=Column(TIMESTAMP(timezone=True),nullable=True,default=text("now()"))