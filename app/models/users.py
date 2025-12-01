from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse

from typing import Dict
from app.database import get_db
from pydantic import BaseModel

from sqlalchemy import Column, Integer, String,Boolean,ForeignKey,Text,create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



class Accounts(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, index=True)
    login_name= Column(String(20))
    login_password= Column(String(20))
    


engine = create_engine("mysql+pymysql://root:Mrinal@localhost/mysql")


#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


