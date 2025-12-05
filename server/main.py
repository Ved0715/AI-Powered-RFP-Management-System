from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import vendors, rfps, proposals

app = FastAPI(
    title="AI-Powered RFP Management System",
    description="Backend API for RFP processing with AI agents",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vendors.router)
app.include_router(rfps.router)
app.include_router(proposals.router)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "AI-Powered RFP Management System API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "ok",
        "service": "rfp-management-api"
    }