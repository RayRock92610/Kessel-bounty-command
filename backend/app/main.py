from fastapi import FastAPI
from app.db.session import init_db
from app.api.routes import reports

app = FastAPI(title="Kessel Bounty Command")

@app.on_event("startup")
def startup():
    init_db()

# Wired to the 17-entity domain
app.include_router(reports.router, prefix="/api/v1/reports")

@app.get("/health/live")
def health():
    return {
        "status": "healthy",
        "engine": "Kessel Force-Align",
        "auth": "1987-locked",
        "port": 8081
    }
