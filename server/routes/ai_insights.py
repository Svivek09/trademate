from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict, Any
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# Initialize Gemini Pro
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

class AIInsightRequest(BaseModel):
    question: str
    context: Optional[Dict[str, Any]] = None
    symbol: Optional[str] = None

@router.post("/ask")
async def ask_ai_insight(request: AIInsightRequest):
    """Ask AI for trading insights and analysis"""
    try:
        if not os.getenv("GEMINI_API_KEY"):
            raise HTTPException(status_code=500, detail="Gemini API key not configured")
        
        # Build context-aware prompt
        prompt = build_trading_prompt(request.question, request.context, request.symbol)
        
        response = model.generate_content(prompt)
        
        return {
            "answer": response.text,
            "model": "gemini-pro",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/explain-indicator/{indicator}")
async def explain_indicator(indicator: str):
    """Get AI explanation of a technical indicator"""
    try:
        if not os.getenv("GEMINI_API_KEY"):
            raise HTTPException(status_code=500, detail="Gemini API key not configured")
        
        prompt = f"Explain the {indicator} technical indicator in simple terms. Include: what it measures, how to interpret it, common values, and trading signals."
        
        response = model.generate_content(prompt)
        
        return {
            "indicator": indicator,
            "explanation": response.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analyze-strategy/{strategy}")
async def analyze_strategy(strategy: str):
    """Get AI analysis of a trading strategy"""
    try:
        if not os.getenv("GEMINI_API_KEY"):
            raise HTTPException(status_code=500, detail="Gemini API key not configured")
        
        prompt = f"Analyze the {strategy} trading strategy. Include: how it works, pros and cons, when it works best, risk considerations, and example implementation."
        
        response = model.generate_content(prompt)
        
        return {
            "strategy": strategy,
            "analysis": response.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-backtest")
async def analyze_backtest_result(backtest_data: Dict[str, Any]):
    """Get AI analysis of backtest results"""
    try:
        if not os.getenv("GEMINI_API_KEY"):
            raise HTTPException(status_code=500, detail="Gemini API key not configured")
        
        prompt = f"""Analyze these backtest results:
        Strategy: {backtest_data.get('strategy', 'Unknown')}
        Symbol: {backtest_data.get('symbol', 'Unknown')}
        Total Return: {backtest_data.get('total_return', 'Unknown')}
        Sharpe Ratio: {backtest_data.get('sharpe_ratio', 'Unknown')}
        Max Drawdown: {backtest_data.get('max_drawdown', 'Unknown')}
        Number of Trades: {backtest_data.get('num_trades', 'Unknown')}
        
        Provide insights on the strategy performance, potential improvements, and risk considerations."""
        
        response = model.generate_content(prompt)
        
        return {
            "analysis": response.text,
            "backtest_data": backtest_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/market-sentiment/{symbol}")
async def get_market_sentiment(symbol: str):
    """Get AI-generated market sentiment analysis"""
    try:
        if not os.getenv("GEMINI_API_KEY"):
            raise HTTPException(status_code=500, detail="Gemini API key not configured")
        
        prompt = f"Provide a brief market sentiment analysis for {symbol}. Consider technical indicators, recent price action, and market conditions. Keep it educational and balanced."
        
        response = model.generate_content(prompt)
        
        return {
            "symbol": symbol,
            "sentiment": response.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trading-advice")
async def get_trading_advice(
    symbol: str = Query(...),
    timeframe: str = Query("1d"),
    strategy: str = Query("general")
):
    """Get AI trading advice for a specific symbol"""
    try:
        if not os.getenv("GEMINI_API_KEY"):
            raise HTTPException(status_code=500, detail="Gemini API key not configured")
        
        prompt = f"""Provide educational trading advice for {symbol} on a {timeframe} timeframe using {strategy} analysis. 
        Focus on technical analysis, risk management, and educational insights. 
        Always include appropriate disclaimers that this is for educational purposes only."""
        
        response = model.generate_content(prompt)
        
        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "strategy": strategy,
            "advice": response.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/risk-assessment/{symbol}")
async def get_risk_assessment(symbol: str):
    """Get AI risk assessment for a symbol"""
    try:
        if not os.getenv("GEMINI_API_KEY"):
            raise HTTPException(status_code=500, detail="Gemini API key not configured")
        
        prompt = f"""Provide a comprehensive risk assessment for {symbol}. Include:
        - Volatility analysis
        - Market risk factors
        - Sector-specific risks
        - Technical risk indicators
        - Risk management recommendations
        
        Keep it educational and balanced."""
        
        response = model.generate_content(prompt)
        
        return {
            "symbol": symbol,
            "risk_assessment": response.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def build_trading_prompt(question: str, context: Optional[Dict[str, Any]] = None, symbol: Optional[str] = None) -> str:
    """Build a context-aware prompt for trading questions"""
    prompt = f"""You are a knowledgeable trading analyst and educator. 
    Provide clear, educational insights about trading strategies, market analysis, and technical indicators.
    Always include disclaimers that this is for educational purposes only and not financial advice.
    
    Question: {question}"""
    
    if context:
        prompt += f"\n\nContext: {context}"
    
    if symbol:
        prompt += f"\n\nSymbol: {symbol}"
    
    prompt += "\n\nProvide educational insights and include appropriate disclaimers."
    
    return prompt 