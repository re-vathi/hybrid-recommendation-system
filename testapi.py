from fastapi import FastAPI
from fastapi.routing import APIRouter

app = FastAPI()
router = APIRouter(prefix="/api")

@router.get("/health")
def health():
    return {"status": "ok"}

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=5555)
