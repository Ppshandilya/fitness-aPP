# database.py
import MySQLdb
from contextlib import contextmanager
import base64



from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine



# RDS connection details
RDS_ENDPOINT = "database-2.cjyoeqqiqelm.eu-north-1.rds.amazonaws.com"
RDS_USER = "admin"
RDS_PASSWORD_ENCODED= "TXJpbmFsMDEwOA=="
RDS_DB = "local_copy"
#import pdb; pdb.set_trace()
RDS_PASSWORD = base64.b64decode(RDS_PASSWORD_ENCODED).decode()
engine = create_engine(
    f"mysql+pymysql://{RDS_USER}:{RDS_PASSWORD}@{RDS_ENDPOINT}/{RDS_DB}"
)


SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
