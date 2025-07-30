import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import ta
import uuid

from strategies.moving_average import MovingAverageStrategy
from strategies.rsi_strategy import RSIStrategy
from strategies.macd_strategy import MACDStrategy

class StrategyService:
    def __init__(self):
        self.strategies = {
            "moving_average": MovingAverageStrategy(),
            "rsi": RSIStrategy(),
            "macd": MACDStrategy()
        }
        self.backtest_results = {}  # In real app, use database
    
    async def run_backtest(
        self, 
        symbol: str, 
        strategy: str, 
        start_date: str, 
        end_date: str, 
        parameters: Dict[str, Any] = {}
    ) -> Dict[str, Any]:
        """Run backtest for a trading strategy"""
        try:
            # Get historical data
            ticker = yf.Ticker(symbol)
            hist = ticker.history(start=start_date, end=end_date)
            
            if hist.empty:
                raise Exception("No historical data available for the specified period")
            
            # Get strategy instance
            if strategy not in self.strategies:
                raise Exception(f"Strategy '{strategy}' not found")
            
            strategy_instance = self.strategies[strategy]
            
            # Run backtest
            results = strategy_instance.backtest(hist, parameters)
            
            # Calculate performance metrics
            performance = self._calculate_performance_metrics(results)
            
            # Generate backtest ID
            backtest_id = str(uuid.uuid4())
            
            # Store results
            self.backtest_results[backtest_id] = {
                "symbol": symbol,
                "strategy": strategy,
                "start_date": start_date,
                "end_date": end_date,
                "parameters": parameters,
                "results": results,
                "performance": performance,
                "timestamp": datetime.now().isoformat()
            }
            
            return {
                "backtest_id": backtest_id,
                "symbol": symbol,
                "strategy": strategy,
                "start_date": start_date,
                "end_date": end_date,
                "parameters": parameters,
                "performance": performance,
                "trades": results.get("trades", []),
                "equity_curve": results.get("equity_curve", [])
            }
            
        except Exception as e:
            raise Exception(f"Error running backtest: {e}")
    
    async def get_backtest_result(self, backtest_id: str) -> Dict[str, Any]:
        """Get backtest result by ID"""
        if backtest_id not in self.backtest_results:
            raise Exception("Backtest not found")
        
        return self.backtest_results[backtest_id]
    
    async def compare_strategies(self, symbol: str, period: str = "1y") -> Dict[str, Any]:
        """Compare performance of different strategies for a symbol"""
        try:
            # Get historical data
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                raise Exception("No historical data available")
            
            comparison = {}
            
            # Test each strategy
            for strategy_name, strategy_instance in self.strategies.items():
                try:
                    results = strategy_instance.backtest(hist, {})
                    performance = self._calculate_performance_metrics(results)
                    comparison[strategy_name] = performance
                except Exception as e:
                    comparison[strategy_name] = {"error": str(e)}
            
            return {
                "symbol": symbol,
                "period": period,
                "comparison": comparison
            }
            
        except Exception as e:
            raise Exception(f"Error comparing strategies: {e}")
    
    async def optimize_strategy(
        self, 
        symbol: str, 
        strategy: str, 
        start_date: str, 
        end_date: str
    ) -> Dict[str, Any]:
        """Optimize strategy parameters for a symbol"""
        try:
            if strategy not in self.strategies:
                raise Exception(f"Strategy '{strategy}' not found")
            
            # Get historical data
            ticker = yf.Ticker(symbol)
            hist = ticker.history(start=start_date, end=end_date)
            
            if hist.empty:
                raise Exception("No historical data available")
            
            strategy_instance = self.strategies[strategy]
            
            # Run optimization
            optimization = strategy_instance.optimize(hist)
            
            return {
                "symbol": symbol,
                "strategy": strategy,
                "optimization": optimization
            }
            
        except Exception as e:
            raise Exception(f"Error optimizing strategy: {e}")
    
    async def analyze_risk(
        self, 
        symbol: str, 
        strategy: str, 
        start_date: str, 
        end_date: str, 
        parameters: str = "{}"
    ) -> Dict[str, Any]:
        """Analyze risk for a strategy"""
        try:
            # Parse parameters
            import json
            params = json.loads(parameters) if parameters else {}
            
            # Get historical data
            ticker = yf.Ticker(symbol)
            hist = ticker.history(start=start_date, end=end_date)
            
            if hist.empty:
                raise Exception("No historical data available")
            
            # Run backtest
            strategy_instance = self.strategies.get(strategy)
            if not strategy_instance:
                raise Exception(f"Strategy '{strategy}' not found")
            
            results = strategy_instance.backtest(hist, params)
            
            # Calculate risk metrics
            risk_metrics = self._calculate_risk_metrics(results)
            
            return {
                "symbol": symbol,
                "strategy": strategy,
                "start_date": start_date,
                "end_date": end_date,
                "parameters": params,
                "risk_metrics": risk_metrics
            }
            
        except Exception as e:
            raise Exception(f"Error analyzing risk: {e}")
    
    async def get_trading_signals(
        self, 
        symbol: str, 
        strategy: str, 
        parameters: str = "{}"
    ) -> Dict[str, Any]:
        """Get current trading signals for a symbol"""
        try:
            # Parse parameters
            import json
            params = json.loads(parameters) if parameters else {}
            
            # Get recent historical data
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="6mo")  # Get 6 months of data for indicators
            
            if hist.empty:
                raise Exception("No historical data available")
            
            strategy_instance = self.strategies.get(strategy)
            if not strategy_instance:
                raise Exception(f"Strategy '{strategy}' not found")
            
            # Get current signals
            signals = strategy_instance.get_signals(hist, params)
            
            return {
                "symbol": symbol,
                "strategy": strategy,
                "parameters": params,
                "signals": signals,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Error getting trading signals: {e}")
    
    def _calculate_performance_metrics(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate performance metrics from backtest results"""
        try:
            trades = results.get("trades", [])
            equity_curve = results.get("equity_curve", [])
            
            if not trades or not equity_curve:
                return {"error": "No trades or equity curve data"}
            
            # Calculate basic metrics
            total_return = (equity_curve[-1] - equity_curve[0]) / equity_curve[0] if equity_curve[0] > 0 else 0
            
            # Calculate daily returns
            daily_returns = []
            for i in range(1, len(equity_curve)):
                daily_return = (equity_curve[i] - equity_curve[i-1]) / equity_curve[i-1]
                daily_returns.append(daily_return)
            
            # Calculate volatility
            volatility = np.std(daily_returns) * np.sqrt(252) if daily_returns else 0
            
            # Calculate Sharpe ratio
            risk_free_rate = 0.02  # Assume 2% risk-free rate
            excess_returns = [r - risk_free_rate/252 for r in daily_returns]
            sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252) if np.std(excess_returns) > 0 else 0
            
            # Calculate max drawdown
            peak = equity_curve[0]
            max_drawdown = 0
            for value in equity_curve:
                if value > peak:
                    peak = value
                drawdown = (peak - value) / peak
                max_drawdown = max(max_drawdown, drawdown)
            
            # Calculate win rate
            winning_trades = sum(1 for trade in trades if trade.get("pnl", 0) > 0)
            win_rate = winning_trades / len(trades) if trades else 0
            
            # Calculate average trade
            total_pnl = sum(trade.get("pnl", 0) for trade in trades)
            avg_trade = total_pnl / len(trades) if trades else 0
            
            return {
                "total_return": total_return,
                "annualized_return": total_return * 252 / len(equity_curve) if equity_curve else 0,
                "volatility": volatility,
                "sharpe_ratio": sharpe_ratio,
                "max_drawdown": max_drawdown,
                "win_rate": win_rate,
                "num_trades": len(trades),
                "avg_trade": avg_trade,
                "total_pnl": total_pnl
            }
            
        except Exception as e:
            return {"error": f"Error calculating metrics: {e}"}
    
    def _calculate_risk_metrics(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate risk metrics from backtest results"""
        try:
            trades = results.get("trades", [])
            equity_curve = results.get("equity_curve", [])
            
            if not trades or not equity_curve:
                return {"error": "No trades or equity curve data"}
            
            # Calculate Value at Risk (VaR)
            daily_returns = []
            for i in range(1, len(equity_curve)):
                daily_return = (equity_curve[i] - equity_curve[i-1]) / equity_curve[i-1]
                daily_returns.append(daily_return)
            
            var_95 = np.percentile(daily_returns, 5) if daily_returns else 0
            var_99 = np.percentile(daily_returns, 1) if daily_returns else 0
            
            # Calculate beta (assuming market return of 0.1 annually)
            market_return = 0.1 / 252  # Daily market return
            excess_returns = [r - market_return for r in daily_returns]
            beta = np.cov(daily_returns, [market_return] * len(daily_returns))[0, 1] / np.var([market_return]) if len(daily_returns) > 1 else 0
            
            return {
                "var_95": var_95,
                "var_99": var_99,
                "beta": beta,
                "volatility": np.std(daily_returns) * np.sqrt(252) if daily_returns else 0,
                "max_drawdown": self._calculate_max_drawdown(equity_curve),
                "calmar_ratio": self._calculate_calmar_ratio(equity_curve)
            }
            
        except Exception as e:
            return {"error": f"Error calculating risk metrics: {e}"}
    
    def _calculate_max_drawdown(self, equity_curve: List[float]) -> float:
        """Calculate maximum drawdown"""
        peak = equity_curve[0]
        max_drawdown = 0
        for value in equity_curve:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak
            max_drawdown = max(max_drawdown, drawdown)
        return max_drawdown
    
    def _calculate_calmar_ratio(self, equity_curve: List[float]) -> float:
        """Calculate Calmar ratio"""
        if len(equity_curve) < 2:
            return 0
        
        total_return = (equity_curve[-1] - equity_curve[0]) / equity_curve[0]
        max_drawdown = self._calculate_max_drawdown(equity_curve)
        
        return total_return / max_drawdown if max_drawdown > 0 else 0 