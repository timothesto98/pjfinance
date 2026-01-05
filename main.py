from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext

app = FastAPI(title="PJFinance")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# USER WA MFANO (temporary)
FAKE_USER = {
    "username": "admin",
    "password_hash": pwd_context.hash("admin123")
}

class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/")
def root():
    return {"message": "PJFinance App is running"}

@app.post("/login")
def login(data: LoginRequest):
    if data.username != FAKE_USER["username"]:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not pwd_context.verify(data.password, FAKE_USER["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {
        "status": "success",
        "message": "Login successful",
        "user": data.username
    }
