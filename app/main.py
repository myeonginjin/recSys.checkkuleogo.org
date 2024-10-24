from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from config.database import SessionLocal, engine, Base
from sqlalchemy import inspect
from models.schemas import Book
from schedulers.scheduler import start_scheduler

Base.metadata.create_all(bind=engine)


app = FastAPI()


# 스케줄러 라우터
@app.on_event("startup")
def on_startup():
    start_scheduler()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


import json
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_FILE = os.path.join(BASE_DIR, "config/secrets.json")

secrets = json.loads(open(SECRET_FILE).read())
db = secrets["db"]

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{db.get('user')}:{db.get('password')}@{db.get('host')}:{db.get('port')}/{db.get('database')}?charset=utf8"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@app.get("/")
async def read_root():

    # 테이블 생성 (만약 아직 생성되지 않았다면)
    Base.metadata.create_all(engine)

    # 데이터베이스에 있는 테이블 확인
    inspector = inspect(engine)  # 수정된 부분
    tables = inspector.get_table_names()

    print("Tables in the database:", tables)

    # Book 모델을 이용한 간단한 SELECT 쿼리
    db = SessionLocal()
    books = db.query(Book).all()

    # 데이터 출력
    for book in books:
        print(f"Title: {book.book_title}, Author: {book.book_author}")

    return {"message": "Hello, World!"}
