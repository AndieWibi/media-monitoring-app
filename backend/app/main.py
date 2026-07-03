from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.database import init_db
from app.api.routes import articles, alerts
from app.config import APP_NAME, APP_VERSION, DEBUG

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    debug=DEBUG
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
async def startup_event():
    init_db()
    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")

# Include routers
app.include_router(articles.router)
app.include_router(alerts.router)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "app": APP_NAME}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
