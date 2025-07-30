from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import ta

from services.market_service import MarketService
from utils.indicators import calculate_technical_indicators

router = APIRouter()
market_service = MarketService()

@router.get("/search")
async def search_symbols(query: str = Query(..., min_length=1)):
    """Search for stock/crypto symbols"""
    try:
        results = await market_service.search_symbols(query)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/quote/{symbol}")
async def get_quote(symbol: str):
    """Get real-time quote for a symbol"""
    try:
        quote = await market_service.get_quote(symbol)
        return quote
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/historical/{symbol}")
async def get_historical_data(
    symbol: str,
    period: str = Query("1y", regex="^(1d|5d|1mo|3mo|6mo|1y|2y|5y|10y|ytd|max)$"),
    interval: str = Query("1d", regex="^(1m|2m|5m|15m|30m|60m|90m|1h|1d|5d|1wk|1mo|3mo)$")
):
    """Get historical price data for a symbol"""
    try:
        data = await market_service.get_historical_data(symbol, period, interval)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/indicators/{symbol}")
async def get_technical_indicators(
    symbol: str,
    period: str = Query("1y", regex="^(1mo|3mo|6mo|1y|2y|5y)$")
):
    """Get technical indicators for a symbol"""
    try:
        indicators = await market_service.get_technical_indicators(symbol, period)
        return indicators
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trending")
async def get_trending_symbols():
    """Get trending stocks/crypto"""
    try:
        trending = await market_service.get_trending_symbols()
        return {"trending": trending}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/market-summary")
async def get_market_summary():
    """Get overall market summary"""
    try:
        summary = await market_service.get_market_summary()
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/crypto/top")
async def get_top_crypto(limit: int = Query(10, ge=1, le=50)):
    """Get top cryptocurrencies by market cap"""
    try:
        crypto = await market_service.get_top_crypto(limit)
        return {"crypto": crypto}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stocks/top")
async def get_top_stocks(limit: int = Query(10, ge=1, le=50)):
    """Get top stocks by market cap"""
    try:
        stocks = await market_service.get_top_stocks(limit)
        return {"stocks": stocks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 