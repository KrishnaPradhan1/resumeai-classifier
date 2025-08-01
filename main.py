"""
ResumeAI Classifier - Backend Application
Advanced AI-based resume classification system
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Create FastAPI app
app = FastAPI(
    title="ResumeAI Classifier API",
    description="Advanced AI-based resume classification system for recruiters and job portals",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for Railway deployment"""
    return {"status": "healthy", "service": "ResumeAI Classifier API"}

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ResumeAI Classifier API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# Test endpoint
@app.get("/test")
async def test():
    """Test endpoint"""
    return {"message": "API is working!"}

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Endpoint not found"}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 