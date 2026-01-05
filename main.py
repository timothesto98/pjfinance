from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="PJFinance", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "PJFinance App is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/docs", include_in_schema=False)
def docs():
    return {"docs": "API documentation available at /docs"}
