import pandas as pd
import numpy as np
import ta
from typing import Dict, List, Any
from datetime import datetime

class MACDStrategy:
    def __init__(self):
        self.name = "MACD Strategy"
        self.description = "Buy when MACD line crosses above signal line, sell when it crosses below"
    
    def backtest(self, data: pd.DataFrame, parameters: Dict[str, Any] = {}) -> Dict[str, Any]:
        """Run backtest for MACD strategy"""
        try:
            # Default parameters
            fast_period = parameters.get("fast_period", 12)
            slow_period = parameters.get("slow_period", 26)
            signal_period = parameters.get("signal_period", 9)
            
            # Calculate MACD
            macd = ta.trend.MACD(data['Close'], window_fast=fast_period, window_slow=slow_period, window_sign=signal_period)
            data['macd'] = macd.macd()
            data['macd_signal'] = macd.macd_signal()
            data['macd_histogram'] = macd.macd_diff()
            
            # Generate signals
            data['signal'] = 0
            data.loc[data['macd'] > data['macd_signal'], 'signal'] = 1  # Buy signal
            data.loc[data['macd'] < data['macd_signal'], 'signal'] = -1  # Sell signal
            
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
                current_macd = data['macd'].iloc[i]
                current_signal = data['macd_signal'].iloc[i]
                
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
                            "pnl": 0,
                            "macd": current_macd,
                            "signal": current_signal
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
                            "pnl": pnl,
                            "macd": current_macd,
                            "signal": current_signal
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
                final_macd = data['macd'].iloc[-1]
                final_signal = data['macd_signal'].iloc[-1]
                cash = shares * final_price
                pnl = cash - trades[-1]["value"] if trades else 0
                trades.append({
                    "date": final_date.strftime("%Y-%m-%d"),
                    "action": "SELL",
                    "price": final_price,
                    "shares": shares,
                    "value": cash,
                    "pnl": pnl,
                    "macd": final_macd,
                    "signal": final_signal
                })
            
            return {
                "trades": trades,
                "equity_curve": equity_curve,
                "parameters": {
                    "fast_period": fast_period,
                    "slow_period": slow_period,
                    "signal_period": signal_period
                }
            }
            
        except Exception as e:
            raise Exception(f"Error in MACD backtest: {e}")
    
    def optimize(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Optimize MACD parameters"""
        try:
            best_sharpe = -np.inf
            best_params = {}
            results = []
            
            # Test different parameter combinations
            fast_periods = range(8, 17, 2)
            slow_periods = range(20, 31, 2)
            signal_periods = range(7, 12, 1)
            
            for fast_period in fast_periods:
                for slow_period in slow_periods:
                    for signal_period in signal_periods:
                        if fast_period >= slow_period:
                            continue
                        
                        # Run backtest with these parameters
                        backtest_result = self.backtest(data, {
                            "fast_period": fast_period,
                            "slow_period": slow_period,
                            "signal_period": signal_period
                        })
                        
                        # Calculate Sharpe ratio
                        equity_curve = backtest_result["equity_curve"]
                        if len(equity_curve) > 1:
                            returns = [(equity_curve[i] - equity_curve[i-1]) / equity_curve[i-1] 
                                     for i in range(1, len(equity_curve))]
                            
                            if returns:
                                sharpe = np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0
                                
                                result = {
                                    "fast_period": fast_period,
                                    "slow_period": slow_period,
                                    "signal_period": signal_period,
                                    "sharpe_ratio": sharpe,
                                    "total_return": (equity_curve[-1] - equity_curve[0]) / equity_curve[0] if equity_curve[0] > 0 else 0,
                                    "num_trades": len(backtest_result["trades"])
                                }
                                results.append(result)
                                
                                if sharpe > best_sharpe:
                                    best_sharpe = sharpe
                                    best_params = {
                                        "fast_period": fast_period,
                                        "slow_period": slow_period,
                                        "signal_period": signal_period
                                    }
            
            return {
                "best_parameters": best_params,
                "best_sharpe": best_sharpe,
                "all_results": results
            }
            
        except Exception as e:
            raise Exception(f"Error optimizing MACD strategy: {e}")
    
    def get_signals(self, data: pd.DataFrame, parameters: Dict[str, Any] = {}) -> Dict[str, Any]:
        """Get current trading signals"""
        try:
            # Default parameters
            fast_period = parameters.get("fast_period", 12)
            slow_period = parameters.get("slow_period", 26)
            signal_period = parameters.get("signal_period", 9)
            
            # Calculate MACD
            macd = ta.trend.MACD(data['Close'], window_fast=fast_period, window_slow=slow_period, window_sign=signal_period)
            data['macd'] = macd.macd()
            data['macd_signal'] = macd.macd_signal()
            data['macd_histogram'] = macd.macd_diff()
            
            # Get current values
            current_price = data['Close'].iloc[-1]
            current_macd = data['macd'].iloc[-1]
            current_signal = data['macd_signal'].iloc[-1]
            current_histogram = data['macd_histogram'].iloc[-1]
            
            # Determine signal
            if current_macd > current_signal:
                signal = "BUY"
                strength = abs(current_histogram) / abs(current_macd) if current_macd != 0 else 0
            elif current_macd < current_signal:
                signal = "SELL"
                strength = abs(current_histogram) / abs(current_macd) if current_macd != 0 else 0
            else:
                signal = "HOLD"
                strength = 0
            
            return {
                "signal": signal,
                "strength": strength,
                "current_price": current_price,
                "current_macd": current_macd,
                "current_signal": current_signal,
                "current_histogram": current_histogram,
                "parameters": {
                    "fast_period": fast_period,
                    "slow_period": slow_period,
                    "signal_period": signal_period
                }
            }
            
        except Exception as e:
            raise Exception(f"Error getting MACD signals: {e}") 