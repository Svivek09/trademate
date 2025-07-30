import pandas as pd
import numpy as np
import ta
from typing import Dict, List, Any

def calculate_technical_indicators(data: pd.DataFrame) -> Dict[str, List[float]]:
    """Calculate all technical indicators for a dataset"""
    indicators = {}
    
    try:
        # Moving averages
        indicators['sma_20'] = ta.trend.sma_indicator(data['Close'], window=20).tolist()
        indicators['sma_50'] = ta.trend.sma_indicator(data['Close'], window=50).tolist()
        indicators['ema_12'] = ta.trend.ema_indicator(data['Close'], window=12).tolist()
        indicators['ema_26'] = ta.trend.ema_indicator(data['Close'], window=26).tolist()
        
        # RSI
        indicators['rsi'] = ta.momentum.rsi(data['Close'], window=14).tolist()
        
        # MACD
        macd = ta.trend.MACD(data['Close'])
        indicators['macd'] = macd.macd().tolist()
        indicators['macd_signal'] = macd.macd_signal().tolist()
        indicators['macd_histogram'] = macd.macd_diff().tolist()
        
        # Bollinger Bands
        bb = ta.volatility.BollingerBands(data['Close'])
        indicators['bb_upper'] = bb.bollinger_hband().tolist()
        indicators['bb_middle'] = bb.bollinger_mavg().tolist()
        indicators['bb_lower'] = bb.bollinger_lband().tolist()
        
        # Stochastic
        stoch = ta.momentum.StochasticOscillator(data['High'], data['Low'], data['Close'])
        indicators['stoch_k'] = stoch.stoch().tolist()
        indicators['stoch_d'] = stoch.stoch_signal().tolist()
        
        # Volume indicators
        indicators['volume_sma'] = ta.volume.volume_sma(data['Close'], data['Volume']).tolist()
        
        # ATR (Average True Range)
        indicators['atr'] = ta.volatility.average_true_range(data['High'], data['Low'], data['Close']).tolist()
        
        # Williams %R
        indicators['williams_r'] = ta.momentum.williams_r(data['High'], data['Low'], data['Close']).tolist()
        
        # CCI (Commodity Channel Index)
        indicators['cci'] = ta.trend.cci(data['High'], data['Low'], data['Close']).tolist()
        
    except Exception as e:
        print(f"Error calculating indicators: {e}")
    
    return indicators

def calculate_support_resistance(data: pd.DataFrame, window: int = 20) -> Dict[str, float]:
    """Calculate support and resistance levels"""
    try:
        high = data['High'].rolling(window=window).max()
        low = data['Low'].rolling(window=window).min()
        
        current_price = data['Close'].iloc[-1]
        resistance = high.iloc[-1]
        support = low.iloc[-1]
        
        return {
            "support": support,
            "resistance": resistance,
            "current_price": current_price
        }
    except Exception as e:
        print(f"Error calculating support/resistance: {e}")
        return {}

def calculate_fibonacci_levels(data: pd.DataFrame) -> Dict[str, float]:
    """Calculate Fibonacci retracement levels"""
    try:
        high = data['High'].max()
        low = data['Low'].min()
        diff = high - low
        
        levels = {
            "0.0": low,
            "0.236": low + 0.236 * diff,
            "0.382": low + 0.382 * diff,
            "0.500": low + 0.500 * diff,
            "0.618": low + 0.618 * diff,
            "0.786": low + 0.786 * diff,
            "1.0": high
        }
        
        return levels
    except Exception as e:
        print(f"Error calculating Fibonacci levels: {e}")
        return {}

def calculate_volatility(data: pd.DataFrame, window: int = 20) -> float:
    """Calculate historical volatility"""
    try:
        returns = data['Close'].pct_change()
        volatility = returns.rolling(window=window).std() * np.sqrt(252)
        return volatility.iloc[-1]
    except Exception as e:
        print(f"Error calculating volatility: {e}")
        return 0.0

def calculate_beta(data: pd.DataFrame, market_data: pd.DataFrame) -> float:
    """Calculate beta relative to market"""
    try:
        stock_returns = data['Close'].pct_change()
        market_returns = market_data['Close'].pct_change()
        
        # Remove NaN values
        stock_returns = stock_returns.dropna()
        market_returns = market_returns.dropna()
        
        # Align the data
        common_index = stock_returns.index.intersection(market_returns.index)
        stock_returns = stock_returns[common_index]
        market_returns = market_returns[common_index]
        
        if len(stock_returns) > 1:
            covariance = np.cov(stock_returns, market_returns)[0, 1]
            market_variance = np.var(market_returns)
            beta = covariance / market_variance if market_variance > 0 else 0
            return beta
        else:
            return 0.0
    except Exception as e:
        print(f"Error calculating beta: {e}")
        return 0.0

def calculate_sharpe_ratio(returns: List[float], risk_free_rate: float = 0.02) -> float:
    """Calculate Sharpe ratio"""
    try:
        if not returns:
            return 0.0
        
        returns_array = np.array(returns)
        excess_returns = returns_array - risk_free_rate / 252  # Daily risk-free rate
        
        if np.std(excess_returns) > 0:
            sharpe = np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)
            return sharpe
        else:
            return 0.0
    except Exception as e:
        print(f"Error calculating Sharpe ratio: {e}")
        return 0.0

def calculate_max_drawdown(equity_curve: List[float]) -> float:
    """Calculate maximum drawdown"""
    try:
        if not equity_curve:
            return 0.0
        
        peak = equity_curve[0]
        max_drawdown = 0.0
        
        for value in equity_curve:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak
            max_drawdown = max(max_drawdown, drawdown)
        
        return max_drawdown
    except Exception as e:
        print(f"Error calculating max drawdown: {e}")
        return 0.0

def calculate_value_at_risk(returns: List[float], confidence_level: float = 0.05) -> float:
    """Calculate Value at Risk (VaR)"""
    try:
        if not returns:
            return 0.0
        
        returns_array = np.array(returns)
        var = np.percentile(returns_array, confidence_level * 100)
        return var
    except Exception as e:
        print(f"Error calculating VaR: {e}")
        return 0.0 