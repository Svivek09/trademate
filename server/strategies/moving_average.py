import pandas as pd
import numpy as np
import ta
from typing import Dict, List, Any
from datetime import datetime

class MovingAverageStrategy:
    def __init__(self):
        self.name = "Moving Average Crossover"
        self.description = "Buy when short MA crosses above long MA, sell when it crosses below"
    
    def backtest(self, data: pd.DataFrame, parameters: Dict[str, Any] = {}) -> Dict[str, Any]:
        """Run backtest for moving average crossover strategy"""
        try:
            # Default parameters
            short_period = parameters.get("short_period", 20)
            long_period = parameters.get("long_period", 50)
            
            # Calculate moving averages
            data['sma_short'] = ta.trend.sma_indicator(data['Close'], window=short_period)
            data['sma_long'] = ta.trend.sma_indicator(data['Close'], window=long_period)
            
            # Generate signals
            data['signal'] = 0
            data.loc[data['sma_short'] > data['sma_long'], 'signal'] = 1  # Buy signal
            data.loc[data['sma_short'] < data['sma_long'], 'signal'] = -1  # Sell signal
            
            # Calculate position changes
            data['position_change'] = data['signal'].diff()
            
            # Initialize variables
            position = 0
            cash = 10000  # Starting capital
            shares = 0
            trades = []
            equity_curve = [cash]
            
            # Simulate trading
            for i in range(1, len(data)):
                current_price = data['Close'].iloc[i]
                current_date = data.index[i]
                
                # Buy signal
                if data['position_change'].iloc[i] == 2:  # Signal changed from -1 to 1
                    if position == 0:  # Not currently holding
                        shares = cash / current_price
                        cash = 0
                        position = 1
                        trades.append({
                            "date": current_date.strftime("%Y-%m-%d"),
                            "action": "BUY",
                            "price": current_price,
                            "shares": shares,
                            "value": shares * current_price,
                            "pnl": 0
                        })
                
                # Sell signal
                elif data['position_change'].iloc[i] == -2:  # Signal changed from 1 to -1
                    if position == 1:  # Currently holding
                        cash = shares * current_price
                        pnl = cash - trades[-1]["value"] if trades else 0
                        trades.append({
                            "date": current_date.strftime("%Y-%m-%d"),
                            "action": "SELL",
                            "price": current_price,
                            "shares": shares,
                            "value": cash,
                            "pnl": pnl
                        })
                        shares = 0
                        position = 0
                
                # Calculate current equity
                current_equity = cash + (shares * current_price)
                equity_curve.append(current_equity)
            
            # Close any remaining position at the end
            if position == 1:
                final_price = data['Close'].iloc[-1]
                final_date = data.index[-1]
                cash = shares * final_price
                pnl = cash - trades[-1]["value"] if trades else 0
                trades.append({
                    "date": final_date.strftime("%Y-%m-%d"),
                    "action": "SELL",
                    "price": final_price,
                    "shares": shares,
                    "value": cash,
                    "pnl": pnl
                })
            
            return {
                "trades": trades,
                "equity_curve": equity_curve,
                "parameters": {
                    "short_period": short_period,
                    "long_period": long_period
                }
            }
            
        except Exception as e:
            raise Exception(f"Error in moving average backtest: {e}")
    
    def optimize(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Optimize moving average parameters"""
        try:
            best_sharpe = -np.inf
            best_params = {}
            results = []
            
            # Test different parameter combinations
            short_periods = range(5, 51, 5)
            long_periods = range(20, 201, 10)
            
            for short_period in short_periods:
                for long_period in long_periods:
                    if short_period >= long_period:
                        continue
                    
                    # Run backtest with these parameters
                    backtest_result = self.backtest(data, {
                        "short_period": short_period,
                        "long_period": long_period
                    })
                    
                    # Calculate Sharpe ratio
                    equity_curve = backtest_result["equity_curve"]
                    if len(equity_curve) > 1:
                        returns = [(equity_curve[i] - equity_curve[i-1]) / equity_curve[i-1] 
                                 for i in range(1, len(equity_curve))]
                        
                        if returns:
                            sharpe = np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0
                            
                            result = {
                                "short_period": short_period,
                                "long_period": long_period,
                                "sharpe_ratio": sharpe,
                                "total_return": (equity_curve[-1] - equity_curve[0]) / equity_curve[0] if equity_curve[0] > 0 else 0,
                                "num_trades": len(backtest_result["trades"])
                            }
                            results.append(result)
                            
                            if sharpe > best_sharpe:
                                best_sharpe = sharpe
                                best_params = {
                                    "short_period": short_period,
                                    "long_period": long_period
                                }
            
            return {
                "best_parameters": best_params,
                "best_sharpe": best_sharpe,
                "all_results": results
            }
            
        except Exception as e:
            raise Exception(f"Error optimizing moving average strategy: {e}")
    
    def get_signals(self, data: pd.DataFrame, parameters: Dict[str, Any] = {}) -> Dict[str, Any]:
        """Get current trading signals"""
        try:
            # Default parameters
            short_period = parameters.get("short_period", 20)
            long_period = parameters.get("long_period", 50)
            
            # Calculate moving averages
            data['sma_short'] = ta.trend.sma_indicator(data['Close'], window=short_period)
            data['sma_long'] = ta.trend.sma_indicator(data['Close'], window=long_period)
            
            # Get current values
            current_price = data['Close'].iloc[-1]
            current_sma_short = data['sma_short'].iloc[-1]
            current_sma_long = data['sma_long'].iloc[-1]
            
            # Determine signal
            if current_sma_short > current_sma_long:
                signal = "BUY"
                strength = (current_sma_short - current_sma_long) / current_sma_long
            elif current_sma_short < current_sma_long:
                signal = "SELL"
                strength = (current_sma_long - current_sma_short) / current_sma_long
            else:
                signal = "HOLD"
                strength = 0
            
            return {
                "signal": signal,
                "strength": strength,
                "current_price": current_price,
                "sma_short": current_sma_short,
                "sma_long": current_sma_long,
                "parameters": {
                    "short_period": short_period,
                    "long_period": long_period
                }
            }
            
        except Exception as e:
            raise Exception(f"Error getting moving average signals: {e}") 