import os
from typing import Optional, Dict, Any, List
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import pymysql
import asyncio

class DatabaseService:
    def __init__(self):
        self.db_type = os.getenv("DATABASE_TYPE", "sqlite")
        self.db_url = os.getenv("DATABASE_URL", "sqlite:///./trademate.db")
        self.client = None
        self.engine = None
        
    async def connect(self):
        """Connect to the database based on configuration"""
        try:
            if self.db_type == "mongodb":
                await self._connect_mongodb()
            elif self.db_type in ["postgresql", "mysql"]:
                await self._connect_sql()
            else:
                # SQLite (default)
                self._connect_sqlite()
                
            print(f"✅ Connected to {self.db_type} database")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            raise
    
    async def _connect_mongodb(self):
        """Connect to MongoDB Atlas"""
        self.client = AsyncIOMotorClient(self.db_url)
        # Test the connection
        await self.client.admin.command('ping')
        self.db = self.client.trademate
    
    async def _connect_sql(self):
        """Connect to PostgreSQL or MySQL"""
        if self.db_type == "postgresql":
            # Convert to async URL for PostgreSQL
            async_url = self.db_url.replace("postgresql://", "postgresql+asyncpg://")
            self.engine = create_async_engine(async_url)
        else:
            # MySQL
            async_url = self.db_url.replace("mysql://", "mysql+aiomysql://")
            self.engine = create_async_engine(async_url)
        
        # Test the connection
        async with self.engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
    
    def _connect_sqlite(self):
        """Connect to SQLite (synchronous)"""
        self.engine = create_engine(self.db_url)
        # Test the connection
        with self.engine.begin() as conn:
            conn.execute(text("SELECT 1"))
    
    async def save_portfolio(self, portfolio_data: Dict[str, Any]) -> str:
        """Save portfolio data to database"""
        try:
            if self.db_type == "mongodb":
                result = await self.db.portfolios.insert_one(portfolio_data)
                return str(result.inserted_id)
            else:
                # For SQL databases, you'd implement table creation and insertion
                # This is a simplified version
                portfolio_id = f"portfolio_{len(portfolio_data)}"
                return portfolio_id
        except Exception as e:
            print(f"Error saving portfolio: {e}")
            raise
    
    async def get_portfolio(self, portfolio_id: str) -> Optional[Dict[str, Any]]:
        """Get portfolio by ID"""
        try:
            if self.db_type == "mongodb":
                from bson import ObjectId
                portfolio = await self.db.portfolios.find_one({"_id": ObjectId(portfolio_id)})
                if portfolio:
                    portfolio["_id"] = str(portfolio["_id"])
                return portfolio
            else:
                # For SQL databases
                return {"id": portfolio_id, "name": "Sample Portfolio"}
        except Exception as e:
            print(f"Error getting portfolio: {e}")
            return None
    
    async def save_backtest_result(self, backtest_data: Dict[str, Any]) -> str:
        """Save backtest result to database"""
        try:
            if self.db_type == "mongodb":
                result = await self.db.backtests.insert_one(backtest_data)
                return str(result.inserted_id)
            else:
                backtest_id = f"backtest_{len(backtest_data)}"
                return backtest_id
        except Exception as e:
            print(f"Error saving backtest: {e}")
            raise
    
    async def get_backtest_result(self, backtest_id: str) -> Optional[Dict[str, Any]]:
        """Get backtest result by ID"""
        try:
            if self.db_type == "mongodb":
                from bson import ObjectId
                backtest = await self.db.backtests.find_one({"_id": ObjectId(backtest_id)})
                if backtest:
                    backtest["_id"] = str(backtest["_id"])
                return backtest
            else:
                return {"id": backtest_id, "status": "completed"}
        except Exception as e:
            print(f"Error getting backtest: {e}")
            return None
    
    async def save_user_preferences(self, user_id: str, preferences: Dict[str, Any]):
        """Save user preferences"""
        try:
            if self.db_type == "mongodb":
                await self.db.user_preferences.update_one(
                    {"user_id": user_id},
                    {"$set": preferences},
                    upsert=True
                )
            else:
                # For SQL databases
                pass
        except Exception as e:
            print(f"Error saving preferences: {e}")
    
    async def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user preferences"""
        try:
            if self.db_type == "mongodb":
                prefs = await self.db.user_preferences.find_one({"user_id": user_id})
                return prefs or {}
            else:
                return {"theme": "dark", "notifications": True}
        except Exception as e:
            print(f"Error getting preferences: {e}")
            return {}
    
    async def close(self):
        """Close database connections"""
        try:
            if self.db_type == "mongodb" and self.client:
                self.client.close()
            elif self.engine:
                await self.engine.dispose()
        except Exception as e:
            print(f"Error closing database: {e}")

# Global database service instance
db_service = DatabaseService() 