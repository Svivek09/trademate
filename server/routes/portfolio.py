from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
import pandas as pd
from datetime import datetime, timedelta

router = APIRouter()

class PortfolioItem(BaseModel):
    symbol: str
    quantity: float
    purchase_price: float
    purchase_date: str

class PortfolioRequest(BaseModel):
    name: str
    items: List[PortfolioItem]
    description: Optional[str] = None

@router.post("/create")
async def create_portfolio(request: PortfolioRequest):
    """Create a new portfolio"""
    try:
        # In a real app, this would save to a database
        portfolio_id = f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        portfolio = {
            "id": portfolio_id,
            "name": request.name,
            "description": request.description,
            "items": [item.dict() for item in request.items],
            "created_at": datetime.now().isoformat(),
            "total_value": 0,
            "total_return": 0
        }
        
        return portfolio
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
async def get_portfolios():
    """Get list of user portfolios"""
    try:
        # Mock data - in real app, fetch from database
        portfolios = [
            {
                "id": "portfolio_1",
                "name": "Tech Portfolio",
                "description": "Technology stocks portfolio",
                "total_value": 25000.00,
                "total_return": 0.15,
                "created_at": "2024-01-01T00:00:00Z"
            },
            {
                "id": "portfolio_2", 
                "name": "Crypto Portfolio",
                "description": "Cryptocurrency holdings",
                "total_value": 15000.00,
                "total_return": -0.05,
                "created_at": "2024-01-01T00:00:00Z"
            }
        ]
        return {"portfolios": portfolios}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{portfolio_id}")
async def get_portfolio(portfolio_id: str):
    """Get detailed portfolio information"""
    try:
        # Mock data - in real app, fetch from database
        portfolio = {
            "id": portfolio_id,
            "name": "Tech Portfolio",
            "description": "Technology stocks portfolio",
            "items": [
                {
                    "symbol": "AAPL",
                    "quantity": 10,
                    "purchase_price": 150.00,
                    "purchase_date": "2024-01-01",
                    "current_price": 175.00,
                    "current_value": 1750.00,
                    "return": 0.167
                },
                {
                    "symbol": "GOOGL",
                    "quantity": 5,
                    "purchase_price": 2800.00,
                    "purchase_date": "2024-01-01",
                    "current_price": 3000.00,
                    "current_value": 15000.00,
                    "return": 0.071
                }
            ],
            "total_value": 16750.00,
            "total_cost": 15500.00,
            "total_return": 0.081,
            "created_at": "2024-01-01T00:00:00Z"
        }
        return portfolio
    except Exception as e:
        raise HTTPException(status_code=404, detail="Portfolio not found")

@router.get("/{portfolio_id}/performance")
async def get_portfolio_performance(
    portfolio_id: str,
    period: str = Query("1y", regex="^(1mo|3mo|6mo|1y|2y|5y)$")
):
    """Get portfolio performance over time"""
    try:
        # Mock performance data
        performance = {
            "portfolio_id": portfolio_id,
            "period": period,
            "total_return": 0.081,
            "annualized_return": 0.095,
            "volatility": 0.18,
            "sharpe_ratio": 0.52,
            "max_drawdown": -0.12,
            "daily_returns": [
                {"date": "2024-01-01", "return": 0.02},
                {"date": "2024-01-02", "return": -0.01},
                {"date": "2024-01-03", "return": 0.015}
            ]
        }
        return performance
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{portfolio_id}/allocation")
async def get_portfolio_allocation(portfolio_id: str):
    """Get portfolio allocation by sector/asset class"""
    try:
        allocation = {
            "portfolio_id": portfolio_id,
            "by_sector": [
                {"sector": "Technology", "percentage": 60.0, "value": 10050.00},
                {"sector": "Healthcare", "percentage": 25.0, "value": 4187.50},
                {"sector": "Finance", "percentage": 15.0, "value": 2512.50}
            ],
            "by_asset": [
                {"asset": "Stocks", "percentage": 80.0, "value": 13400.00},
                {"asset": "Bonds", "percentage": 15.0, "value": 2512.50},
                {"asset": "Cash", "percentage": 5.0, "value": 837.50}
            ]
        }
        return allocation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{portfolio_id}/add")
async def add_to_portfolio(portfolio_id: str, item: PortfolioItem):
    """Add item to portfolio"""
    try:
        # In real app, add to database
        return {
            "message": "Item added successfully",
            "portfolio_id": portfolio_id,
            "item": item.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{portfolio_id}/remove/{symbol}")
async def remove_from_portfolio(portfolio_id: str, symbol: str):
    """Remove item from portfolio"""
    try:
        return {
            "message": "Item removed successfully",
            "portfolio_id": portfolio_id,
            "symbol": symbol
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{portfolio_id}/rebalance")
async def get_rebalance_suggestions(portfolio_id: str):
    """Get portfolio rebalancing suggestions"""
    try:
        suggestions = {
            "portfolio_id": portfolio_id,
            "current_allocation": {
                "AAPL": 35.0,
                "GOOGL": 25.0,
                "MSFT": 20.0,
                "TSLA": 20.0
            },
            "target_allocation": {
                "AAPL": 30.0,
                "GOOGL": 25.0,
                "MSFT": 25.0,
                "TSLA": 20.0
            },
            "actions": [
                {
                    "action": "sell",
                    "symbol": "AAPL",
                    "quantity": 2,
                    "reason": "Reduce overweight position"
                },
                {
                    "action": "buy",
                    "symbol": "MSFT",
                    "quantity": 3,
                    "reason": "Increase underweight position"
                }
            ]
        }
        return suggestions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{portfolio_id}/risk")
async def get_portfolio_risk(portfolio_id: str):
    """Get portfolio risk analysis"""
    try:
        risk_analysis = {
            "portfolio_id": portfolio_id,
            "beta": 1.2,
            "volatility": 0.18,
            "var_95": -0.08,
            "var_99": -0.12,
            "correlation_matrix": {
                "AAPL": {"GOOGL": 0.7, "MSFT": 0.8, "TSLA": 0.5},
                "GOOGL": {"AAPL": 0.7, "MSFT": 0.9, "TSLA": 0.6},
                "MSFT": {"AAPL": 0.8, "GOOGL": 0.9, "TSLA": 0.5},
                "TSLA": {"AAPL": 0.5, "GOOGL": 0.6, "MSFT": 0.5}
            },
            "concentration_risk": "Medium",
            "sector_risk": "High (Tech heavy)"
        }
        return risk_analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 