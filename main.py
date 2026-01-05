from fastapi import FastAPI, HTTPException
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from passlib.context import CryptContext

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)

@app.get("/")
def root():
    return {"status": "PJFinance API iko live na salama"}

@app.post("/create-user")
def create_user(username: str, password: str):
    db = SessionLocal()

    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        db.close()
        raise HTTPException(status_code=400, detail="Username tayari ipo")

    hashed = hash_password(password)

    user = User(username=username, password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    return {
        "message": "User ameundwa kikamilifu",
        "username": user.username
    }

@app.post("/login")
def login(username: str, password: str):
    db = SessionLocal()

    user = db.query(User).filter(User.username == username).first()
    if not user:
        db.close()
        raise HTTPException(status_code=401, detail="Username haipo")

    if not verify_password(password, user.password):
        db.close()
        raise HTTPException(status_code=401, detail="Password sio sahihi")

    db.close()
    return {
        "message": "Login imefanikiwa",
        "user_id": user.id,
        "username": user.username
    }
