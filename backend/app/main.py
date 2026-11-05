from fastapi import FastAPI
from app.routers import applications


app = FastAPI(title="Job Tracker")

app.include_router(applications.router)

@app.get("/health")
def health():
    return {"status": "ok"}