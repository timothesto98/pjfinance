from fastapi import FastAPI, HTTPException
import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from passlib.context import CryptContext

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------- MODELS ----------

class Branch(Base):
    __tablename__ = "branches"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=True)

Base.metadata.create_all(bind=engine)

# ---------- HELPERS ----------

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)

# ---------- ENDPOINTS ----------

@app.get("/")
def root():
    return {"status": "STEP 5 iko live"}

@app.post("/create-branch")
def create_branch(name: str):
    db = SessionLocal()

    if db.query(Branch).filter(Branch.name == name).first():
        db.close()
        raise HTTPException(status_code=400, detail="Branch tayari ipo")

    branch = Branch(name=name)
    db.add(branch)
    db.commit()
    db.refresh(branch)
    db.close()

    return {"message": "Branch imeundwa", "branch_id": branch.id}

@app.post("/create-user")
def create_user(
    username: str,
    password: str,
    role: str,
    branch_id: int = None
):
    db = SessionLocal()

    if db.query(User).filter(User.username == username).first():
        db.close()
        raise HTTPException(status_code=400, detail="Username tayari ipo")

    if role != "super_admin" and branch_id is None:
        db.close()
        raise HTTPException(status_code=400, detail="Branch inahitajika kwa role hii")

    user = User(
        username=username,
        password=hash_password(password),
        role=role,
        branch_id=branch_id
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    return {
        "message": "User ameundwa",
        "username": user.username,
        "role": user.role,
        "branch_id": user.branch_id
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
        "role": user.role,
        "branch_id": user.branch_id
    }
