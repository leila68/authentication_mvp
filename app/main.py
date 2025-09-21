from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.api import auth, users

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bright Health Auth MVP",
    description="Authentication MVP for AI Integration Platform",
    version="1.0.0",
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/")
def read_root():
    return {
        "message": "Bright Health Auth MVP",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "auth-mvp"}