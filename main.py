from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import create_db_and_tables
from app.routes import (
    estudiante_router,
    profesor_router,
    facultad_router,
    carrera_router,
    curso_router,
    seccion_router,
    matricula_router,
    pago_router,
    calificacion_router,
)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Event handlers
@app.on_event("startup")
def on_startup():
    """Create database tables on startup"""
    create_db_and_tables()


# Health check endpoint
@app.get("/")
def root():
    """Root endpoint - health check"""
    return {
        "message": "Sistema Académico API",
        "version": settings.VERSION,
        "status": "active"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Include routers
app.include_router(estudiante_router, prefix=settings.API_V1_STR)
app.include_router(profesor_router, prefix=settings.API_V1_STR)
app.include_router(facultad_router, prefix=settings.API_V1_STR)
app.include_router(carrera_router, prefix=settings.API_V1_STR)
app.include_router(curso_router, prefix=settings.API_V1_STR)
app.include_router(seccion_router, prefix=settings.API_V1_STR)
app.include_router(matricula_router, prefix=settings.API_V1_STR)
app.include_router(pago_router, prefix=settings.API_V1_STR)
app.include_router(calificacion_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
