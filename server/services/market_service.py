import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import os
from typing import Dict, List, Optional, Any
import ta

class MarketService:
    def __init__(self):
        self.alpha_vantage_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        self.coingecko_base_url = "https://api.coingecko.com/api/v3"
    
    async def search_symbols(self, query: str) -> List[Dict[str, Any]]:
        """Search for stock/crypto symbols"""
        try:
            # For stocks, use yfinance search
            if len(query) >= 2:
                ticker = yf.Ticker(query)
                info = ticker.info
                
                if info and 'regularMarketPrice' in info:
                    return [{
                        "symbol": query.upper(),
                        "name": info.get('longName', query.upper()),
                        "type": "stock",
                        "price": info.get('regularMarketPrice', 0),
                        "change": info.get('regularMarketChangePercent', 0)
                    }]
            
            # For crypto, search common symbols
            crypto_symbols = ["BTC", "ETH", "ADA", "DOT", "LINK", "LTC", "BCH", "XRP"]
            if query.upper() in crypto_symbols:
                return [{
                    "symbol": f"{query.upper()}-USD",
                    "name": f"{query.upper()}",
                    "type": "crypto",
                    "price": 0,  # Would fetch from API
                    "change": 0
                }]
            
            return []
        except Exception as e:
            print(f"Error searching symbols: {e}")
            return []
    
    async def get_quote(self, symbol: str) -> Dict[str, Any]:
        """Get real-time quote for a symbol"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            if not info or 'regularMarketPrice' not in info:
                raise Exception("Symbol not found")
            
            return {
                "symbol": symbol.upper(),
                "name": info.get('longName', symbol.upper()),
                "price": info.get('regularMarketPrice', 0),
                "change": info.get('regularMarketChange', 0),
                "change_percent": info.get('regularMarketChangePercent', 0),
                "volume": info.get('volume', 0),
                "market_cap": info.get('marketCap', 0),
                "high_52_week": info.get('fiftyTwoWeekHigh', 0),
                "low_52_week": info.get('fiftyTwoWeekLow', 0),
                "pe_ratio": info.get('trailingPE', 0),
                "dividend_yield": info.get('dividendYield', 0),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            raise Exception(f"Error fetching quote: {e}")
    
    async def get_historical_data(self, symbol: str, period: str = "1y", interval: str = "1d") -> Dict[str, Any]:
        """Get historical price data for a symbol"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period, interval=interval)
            
            if hist.empty:
                raise Exception("No historical data available")
            
            # Convert to list format for JSON serialization
            data = []
            for date, row in hist.iterrows():
                data.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "open": float(row['Open']),
                    "high": float(row['High']),
                    "low": float(row['Low']),
                    "close": float(row['Close']),
                    "volume": int(row['Volume'])
                })
            
            return {
                "symbol": symbol.upper(),
                "period": period,
                "interval": interval,
                "data": data
            }
        except Exception as e:
            raise Exception(f"Error fetching historical data: {e}")
    
    async def get_technical_indicators(self, symbol: str, period: str = "1y") -> Dict[str, Any]:
        """Get technical indicators for a symbol"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                raise Exception("No historical data available")
            
            # Calculate technical indicators
            indicators = {}
            
            # Moving averages
            indicators['sma_20'] = ta.trend.sma_indicator(hist['Close'], window=20).tolist()
            indicators['sma_50'] = ta.trend.sma_indicator(hist['Close'], window=50).tolist()
            indicators['ema_12'] = ta.trend.ema_indicator(hist['Close'], window=12).tolist()
            indicators['ema_26'] = ta.trend.ema_indicator(hist['Close'], window=26).tolist()
            
            # RSI
            indicators['rsi'] = ta.momentum.rsi(hist['Close'], window=14).tolist()
            
            # MACD
            macd = ta.trend.MACD(hist['Close'])
            indicators['macd'] = macd.macd().tolist()
            indicators['macd_signal'] = macd.macd_signal().tolist()
            indicators['macd_histogram'] = macd.macd_diff().tolist()
            
            # Bollinger Bands
            bb = ta.volatility.BollingerBands(hist['Close'])
            indicators['bb_upper'] = bb.bollinger_hband().tolist()
            indicators['bb_middle'] = bb.bollinger_mavg().tolist()
            indicators['bb_lower'] = bb.bollinger_lband().tolist()
            
            # Stochastic
            stoch = ta.momentum.StochasticOscillator(hist['High'], hist['Low'], hist['Close'])
            indicators['stoch_k'] = stoch.stoch().tolist()
            indicators['stoch_d'] = stoch.stoch_signal().tolist()
            
            # Volume indicators
            indicators['volume_sma'] = ta.volume.volume_sma(hist['Close'], hist['Volume']).tolist()
            
            # Get dates for the indicators
            dates = [date.strftime("%Y-%m-%d") for date in hist.index]
            
            return {
                "symbol": symbol.upper(),
                "period": period,
                "dates": dates,
                "indicators": indicators
            }
        except Exception as e:
            raise Exception(f"Error calculating indicators: {e}")
    
    async def get_trending_symbols(self) -> List[Dict[str, Any]]:
        """Get trending stocks/crypto"""
        try:
            # Mock trending data - in real app, fetch from API
            trending = [
                {
                    "symbol": "AAPL",
                    "name": "Apple Inc.",
                    "price": 175.50,
                    "change_percent": 2.5,
                    "volume": 50000000
                },
                {
                    "symbol": "TSLA",
                    "name": "Tesla Inc.",
                    "price": 250.75,
                    "change_percent": -1.2,
                    "volume": 35000000
                },
                {
                    "symbol": "BTC-USD",
                    "name": "Bitcoin",
                    "price": 45000.00,
                    "change_percent": 3.8,
                    "volume": 25000000000
                }
            ]
            return trending
        except Exception as e:
            print(f"Error fetching trending symbols: {e}")
            return []
    
    async def get_market_summary(self) -> Dict[str, Any]:
        """Get overall market summary"""
        try:
            # Mock market summary - in real app, fetch from API
            summary = {
                "sp500": {
                    "symbol": "^GSPC",
                    "price": 4500.00,
                    "change_percent": 0.5
                },
                "nasdaq": {
                    "symbol": "^IXIC", 
                    "price": 14000.00,
                    "change_percent": 0.8
                },
                "dow": {
                    "symbol": "^DJI",
                    "price": 35000.00,
                    "change_percent": 0.3
                },
                "vix": {
                    "symbol": "^VIX",
                    "price": 15.50,
                    "change_percent": -2.0
                }
            }
            return summary
        except Exception as e:
            print(f"Error fetching market summary: {e}")
            return {}
    
    async def get_top_crypto(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top cryptocurrencies by market cap"""
        try:
            # Mock crypto data - in real app, fetch from CoinGecko API
            crypto = [
                {
                    "symbol": "BTC-USD",
                    "name": "Bitcoin",
                    "price": 45000.00,
                    "market_cap": 850000000000,
                    "change_24h": 2.5
                },
                {
                    "symbol": "ETH-USD", 
                    "name": "Ethereum",
                    "price": 3200.00,
                    "market_cap": 380000000000,
                    "change_24h": 1.8
                },
                {
                    "symbol": "ADA-USD",
                    "name": "Cardano",
                    "price": 1.20,
                    "market_cap": 38000000000,
                    "change_24h": -0.5
                }
            ]
            return crypto[:limit]
        except Exception as e:
            print(f"Error fetching top crypto: {e}")
            return []
    
    async def get_top_stocks(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top stocks by market cap"""
        try:
            # Mock stock data - in real app, fetch from API
            stocks = [
                {
                    "symbol": "AAPL",
                    "name": "Apple Inc.",
                    "price": 175.50,
                    "market_cap": 2800000000000,
                    "change_percent": 2.5
                },
                {
                    "symbol": "MSFT",
                    "name": "Microsoft Corporation",
                    "price": 350.00,
                    "market_cap": 2600000000000,
                    "change_percent": 1.8
                },
                {
                    "symbol": "GOOGL",
                    "name": "Alphabet Inc.",
                    "price": 3000.00,
                    "market_cap": 2000000000000,
                    "change_percent": 0.9
                }
            ]
            return stocks[:limit]
        except Exception as e:
            print(f"Error fetching top stocks: {e}")
            return [] 