from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# USER WA MFANO (simple, no hashing)
FAKE_USER = {
    "username": "admin",
    "password": "1234"
}

class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/")
def root():
    return {"message": "PJFinance App is running"}

@app.post("/login")
def login(data: LoginRequest):
    if (
        data.username == FAKE_USER["username"]
        and data.password == FAKE_USER["password"]
    ):
        return {
            "status": "success",
            "message": "Login successful",
            "user": data.username
        }

    raise HTTPException(status_code=401, detail="Invalid username or password")
