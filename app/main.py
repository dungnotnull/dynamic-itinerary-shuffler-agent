from fastapi import FastAPI
from app.api.main_routes import router as api_router
from app.core.config import settings

app = FastAPI(title="Dynamic Itinerary Shuffler - Production Engine")

app.include_router(api_router)

@app.get("/health")
async def health():
    return {"status": "online", "version": "1.0.0"}
