from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"status": "PJFinance connected to database"}

@app.post("/create-user")
def create_user(username: str, password: str):
    db = SessionLocal()
    user = User(username=username, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return {"message": "User created", "user": username}
