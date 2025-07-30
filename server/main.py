from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from dotenv import load_dotenv
import os

from routes import market_data, strategies, ai_insights, portfolio
from services.market_service import MarketService
from services.strategy_service import StrategyService
from services.database_service import db_service

# Load environment variables
load_dotenv()

app = FastAPI(
    title="TradeMate API",
    description="A comprehensive trading analytics dashboard API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    try:
        await db_service.connect()
        print("🚀 TradeMate API started successfully!")
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")

# Database shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    await db_service.close()

# Include routers
app.include_router(market_data.router, prefix="/api/market", tags=["Market Data"])
app.include_router(strategies.router, prefix="/api/strategies", tags=["Trading Strategies"])
app.include_router(ai_insights.router, prefix="/api/ai", tags=["AI Insights"])
app.include_router(portfolio.router, prefix="/api/portfolio", tags=["Portfolio"])

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "TradeMate API is running!",
        "version": "1.0.0",
        "status": "healthy",
        "database": db_service.db_type
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 