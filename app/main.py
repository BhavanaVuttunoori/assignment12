from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routes import users, calculations

# Initialize FastAPI app
app = FastAPI(
    title="Web API - User & Calculation Management",
    description="A RESTful API for user registration/login and calculation CRUD operations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(calculations.router)


@app.on_event("startup")
def on_startup():
    """Initialize database on application startup."""
    init_db()


@app.get("/", tags=["root"])
def root():
    """Root endpoint - API health check."""
    return {
        "message": "Welcome to the Web API!",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "users": "/users",
            "calculations": "/calculations"
        }
    }


@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
