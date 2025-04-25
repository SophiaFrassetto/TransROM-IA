from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth
from .database.database import engine
from .models import user

# Create database tables
user.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TransROM-IA API",
    description="API for TransROM-IA - AI-Assisted ROM Translation and Dubbing System",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])


@app.get("/")
async def root():
    return {"message": "Welcome to TransROM-IA API"}
