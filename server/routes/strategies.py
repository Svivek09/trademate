from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
import pandas as pd
from datetime import datetime, timedelta

from services.strategy_service import StrategyService
from strategies.moving_average import MovingAverageStrategy
from strategies.rsi_strategy import RSIStrategy
from strategies.macd_strategy import MACDStrategy

router = APIRouter()
strategy_service = StrategyService()

class BacktestRequest(BaseModel):
    symbol: str
    strategy: str
    start_date: str
    end_date: str
    parameters: Dict[str, Any] = {}

class StrategyInfo(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]
    example: Dict[str, Any]

@router.get("/available")
async def get_available_strategies():
    """Get list of available trading strategies"""
    strategies = [
        {
            "name": "Moving Average Crossover",
            "description": "Buy when short MA crosses above long MA, sell when it crosses below",
            "parameters": {
                "short_period": {"type": "int", "default": 20, "min": 5, "max": 50},
                "long_period": {"type": "int", "default": 50, "min": 20, "max": 200}
            },
            "example": {
                "symbol": "AAPL",
                "short_period": 20,
                "long_period": 50
            }
        },
        {
            "name": "RSI Strategy",
            "description": "Buy when RSI is oversold (< 30), sell when overbought (> 70)",
            "parameters": {
                "rsi_period": {"type": "int", "default": 14, "min": 5, "max": 30},
                "oversold": {"type": "int", "default": 30, "min": 10, "max": 40},
                "overbought": {"type": "int", "default": 70, "min": 60, "max": 90}
            },
            "example": {
                "symbol": "AAPL",
                "rsi_period": 14,
                "oversold": 30,
                "overbought": 70
            }
        },
        {
            "name": "MACD Strategy",
            "description": "Buy when MACD line crosses above signal line, sell when it crosses below",
            "parameters": {
                "fast_period": {"type": "int", "default": 12, "min": 5, "max": 20},
                "slow_period": {"type": "int", "default": 26, "min": 20, "max": 50},
                "signal_period": {"type": "int", "default": 9, "min": 5, "max": 20}
            },
            "example": {
                "symbol": "AAPL",
                "fast_period": 12,
                "slow_period": 26,
                "signal_period": 9
            }
        }
    ]
    return {"strategies": strategies}

@router.post("/backtest")
async def run_backtest(request: BacktestRequest):
    """Run backtest for a trading strategy"""
    try:
        result = await strategy_service.run_backtest(
            symbol=request.symbol,
            strategy=request.strategy,
            start_date=request.start_date,
            end_date=request.end_date,
            parameters=request.parameters
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/backtest/{backtest_id}")
async def get_backtest_result(backtest_id: str):
    """Get backtest result by ID"""
    try:
        result = await strategy_service.get_backtest_result(backtest_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail="Backtest not found")

@router.get("/performance/{symbol}")
async def get_strategy_performance(
    symbol: str,
    period: str = Query("1y", regex="^(1mo|3mo|6mo|1y|2y|5y)$")
):
    """Get performance comparison of different strategies for a symbol"""
    try:
        performance = await strategy_service.compare_strategies(symbol, period)
        return performance
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/optimize/{symbol}")
async def optimize_strategy(
    symbol: str,
    strategy: str = Query(..., regex="^(moving_average|rsi|macd)$"),
    start_date: str = Query(...),
    end_date: str = Query(...)
):
    """Optimize strategy parameters for a symbol"""
    try:
        optimization = await strategy_service.optimize_strategy(
            symbol, strategy, start_date, end_date
        )
        return optimization
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/risk-analysis/{symbol}")
async def get_risk_analysis(
    symbol: str,
    strategy: str = Query(...),
    start_date: str = Query(...),
    end_date: str = Query(...),
    parameters: str = Query("{}")
):
    """Get risk analysis for a strategy"""
    try:
        risk_analysis = await strategy_service.analyze_risk(
            symbol, strategy, start_date, end_date, parameters
        )
        return risk_analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/signals/{symbol}")
async def get_trading_signals(
    symbol: str,
    strategy: str = Query(...),
    parameters: str = Query("{}")
):
    """Get current trading signals for a symbol"""
    try:
        signals = await strategy_service.get_trading_signals(symbol, strategy, parameters)
        return signals
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 