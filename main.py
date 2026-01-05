from fastapi import FastAPI, HTTPException
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "PJFinance API iko live"}

@app.post("/create-user")
def create_user(username: str, password: str):
    db = SessionLocal()

    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        db.close()
        raise HTTPException(status_code=400, detail="Username tayari ipo")

    user = User(username=username, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    return {
        "message": "User ameundwa kikamilifu",
        "user_id": user.id,
        "username": user.username
    }
