import pandas as pd
import numpy as np
import ta
from typing import Dict, List, Any
from datetime import datetime

class RSIStrategy:
    def __init__(self):
        self.name = "RSI Strategy"
        self.description = "Buy when RSI is oversold (< 30), sell when overbought (> 70)"
    
    def backtest(self, data: pd.DataFrame, parameters: Dict[str, Any] = {}) -> Dict[str, Any]:
        """Run backtest for RSI strategy"""
        try:
            # Default parameters
            rsi_period = parameters.get("rsi_period", 14)
            oversold = parameters.get("oversold", 30)
            overbought = parameters.get("overbought", 70)
            
            # Calculate RSI
            data['rsi'] = ta.momentum.rsi(data['Close'], window=rsi_period)
            
            # Generate signals
            data['signal'] = 0
            data.loc[data['rsi'] < oversold, 'signal'] = 1  # Buy signal (oversold)
            data.loc[data['rsi'] > overbought, 'signal'] = -1  # Sell signal (overbought)
            
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
                current_rsi = data['rsi'].iloc[i]
                
                # Buy signal (oversold)
                if data['position_change'].iloc[i] == 1:  # Signal changed from 0 to 1
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
                            "pnl": 0,
                            "rsi": current_rsi
                        })
                
                # Sell signal (overbought)
                elif data['position_change'].iloc[i] == -1:  # Signal changed from 0 to -1
                    if position == 1:  # Currently holding
                        cash = shares * current_price
                        pnl = cash - trades[-1]["value"] if trades else 0
                        trades.append({
                            "date": current_date.strftime("%Y-%m-%d"),
                            "action": "SELL",
                            "price": current_price,
                            "shares": shares,
                            "value": cash,
                            "pnl": pnl,
                            "rsi": current_rsi
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
                final_rsi = data['rsi'].iloc[-1]
                cash = shares * final_price
                pnl = cash - trades[-1]["value"] if trades else 0
                trades.append({
                    "date": final_date.strftime("%Y-%m-%d"),
                    "action": "SELL",
                    "price": final_price,
                    "shares": shares,
                    "value": cash,
                    "pnl": pnl,
                    "rsi": final_rsi
                })
            
            return {
                "trades": trades,
                "equity_curve": equity_curve,
                "parameters": {
                    "rsi_period": rsi_period,
                    "oversold": oversold,
                    "overbought": overbought
                }
            }
            
        except Exception as e:
            raise Exception(f"Error in RSI backtest: {e}")
    
    def optimize(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Optimize RSI parameters"""
        try:
            best_sharpe = -np.inf
            best_params = {}
            results = []
            
            # Test different parameter combinations
            rsi_periods = range(10, 21, 2)
            oversold_levels = range(20, 41, 5)
            overbought_levels = range(60, 81, 5)
            
            for rsi_period in rsi_periods:
                for oversold in oversold_levels:
                    for overbought in overbought_levels:
                        if oversold >= overbought:
                            continue
                        
                        # Run backtest with these parameters
                        backtest_result = self.backtest(data, {
                            "rsi_period": rsi_period,
                            "oversold": oversold,
                            "overbought": overbought
                        })
                        
                        # Calculate Sharpe ratio
                        equity_curve = backtest_result["equity_curve"]
                        if len(equity_curve) > 1:
                            returns = [(equity_curve[i] - equity_curve[i-1]) / equity_curve[i-1] 
                                     for i in range(1, len(equity_curve))]
                            
                            if returns:
                                sharpe = np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0
                                
                                result = {
                                    "rsi_period": rsi_period,
                                    "oversold": oversold,
                                    "overbought": overbought,
                                    "sharpe_ratio": sharpe,
                                    "total_return": (equity_curve[-1] - equity_curve[0]) / equity_curve[0] if equity_curve[0] > 0 else 0,
                                    "num_trades": len(backtest_result["trades"])
                                }
                                results.append(result)
                                
                                if sharpe > best_sharpe:
                                    best_sharpe = sharpe
                                    best_params = {
                                        "rsi_period": rsi_period,
                                        "oversold": oversold,
                                        "overbought": overbought
                                    }
            
            return {
                "best_parameters": best_params,
                "best_sharpe": best_sharpe,
                "all_results": results
            }
            
        except Exception as e:
            raise Exception(f"Error optimizing RSI strategy: {e}")
    
    def get_signals(self, data: pd.DataFrame, parameters: Dict[str, Any] = {}) -> Dict[str, Any]:
        """Get current trading signals"""
        try:
            # Default parameters
            rsi_period = parameters.get("rsi_period", 14)
            oversold = parameters.get("oversold", 30)
            overbought = parameters.get("overbought", 70)
            
            # Calculate RSI
            data['rsi'] = ta.momentum.rsi(data['Close'], window=rsi_period)
            
            # Get current values
            current_price = data['Close'].iloc[-1]
            current_rsi = data['rsi'].iloc[-1]
            
            # Determine signal
            if current_rsi < oversold:
                signal = "BUY"
                strength = (oversold - current_rsi) / oversold
            elif current_rsi > overbought:
                signal = "SELL"
                strength = (current_rsi - overbought) / (100 - overbought)
            else:
                signal = "HOLD"
                strength = 0
            
            return {
                "signal": signal,
                "strength": strength,
                "current_price": current_price,
                "current_rsi": current_rsi,
                "oversold_level": oversold,
                "overbought_level": overbought,
                "parameters": {
                    "rsi_period": rsi_period,
                    "oversold": oversold,
                    "overbought": overbought
                }
            }
            
        except Exception as e:
            raise Exception(f"Error getting RSI signals: {e}") 