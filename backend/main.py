from fastapi import FastAPI
from database import engine, Base
from routers import auth_router, appointments_router, prescriptions_router, billing_router, notifications_router

# Create FastAPI app
app = FastAPI(
    title="Eye Clinic Management System API",
    description="API for managing eye clinic appointments, prescriptions, billing, and notifications",
    version="1.0.0"
)

# Create database tables on startup
@app.on_event("startup")
def create_tables():
    """Create database tables."""
    Base.metadata.create_all(bind=engine)


# Root endpoint
@app.get("/")
def root():
    """API info."""
    return {"message": "Eye Clinic API"}

# Include routers with /api/v1 prefix
app.include_router(auth_router, prefix="/api/v1", tags=["authentication"])
app.include_router(appointments_router, prefix="/api/v1", tags=["appointments"])
app.include_router(prescriptions_router, prefix="/api/v1", tags=["prescriptions"])
app.include_router(billing_router, prefix="/api/v1", tags=["billing"])
app.include_router(notifications_router, prefix="/api/v1", tags=["notifications"])


@app.get("/health")
def health_check():
    """Check health."""
    return {"status": "healthy"}