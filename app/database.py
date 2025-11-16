# database.py
import MySQLdb
from contextlib import contextmanager

# @contextmanager
# def get_cursor():
#     conn = MySQLdb.connect(host="localhost", user="root", passwd="Mrinal", db="mysql")
#     try:
#         cursor = conn.cursor()
#         yield cursor
#         conn.commit()
#     finally:
#         cursor.close()
#         conn.close()


from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:Mrinal@localhost/mysql")
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
