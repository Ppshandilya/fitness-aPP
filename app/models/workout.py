from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse

from typing import Dict
from app.database import get_db
from pydantic import BaseModel

from sqlalchemy import Column, Integer, String,Boolean,ForeignKey,Text,create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()





class Workout(Base):
    __tablename__ = 'workout'
    id = Column(Integer, primary_key=True, index=True)
    date= Column(String(50),  index=True)
    did_workout= Column(Boolean,  default=True)
    intensity = Column(Integer, nullable=False)
   

# class Circles(Base):
#     __tablename__ = 'circle'
#     id = Column(Integer, primary_key=True, index=True)
#     circle_name = Column(String(50),  index=True)
#     recipients = Column(String(200)) 

# class Accounts(Base):
#     __tablename__ = 'accounts'
#     id = Column(Integer, primary_key=True, index=True)
#     login_name= Column(String(50),  index=True)
#     login_password= Column(String(200)) 

    

engine = create_engine("mysql+pymysql://root:Mrinal@localhost/mysql")


#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


