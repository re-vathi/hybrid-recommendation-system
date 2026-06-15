from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(
    title="Hybrid Recommendation API"
)

app.include_router(router)

@app.get("/")
def home():
    return {
        "status":"running"
    }