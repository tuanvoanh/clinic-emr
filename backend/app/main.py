from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.api_router import api_router

# Initialize FastAPI app with metadata for Swagger UI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    openapi_url="/api/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration (Allows Frontend to call API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, specify explicit domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routes
app.include_router(api_router, prefix="/api")

# Set up global exception handlers
from app.core.exceptions import setup_exception_handlers
setup_exception_handlers(app)

@app.get("/", tags=["Health Check"])
def read_root():
    """
    Endpoint to check the server's running status.
    """
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
