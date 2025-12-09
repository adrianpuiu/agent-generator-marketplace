#!/usr/bin/env python3
"""
stock_sentiment_agent - Example Agent Template

This template shows the complete structure of a production-ready agent:
- Tool definitions with Pydantic schemas
- Error handling and logging
- Memory persistence (Redis optional)
- Agent initialization
- Main execution loop

Copy and customize this for your own agents.
"""

import os
import sys
import json
import logging
import asyncio
from typing import Optional

# Agent framework
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from pydantic import BaseModel, Field

# Optional: Redis memory
try:
    from langchain_community.chat_message_histories import RedisChatMessageHistory
    from langchain_core.runnables.history import RunnableWithMessageHistory
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

# === Logging Configuration ===
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# === Tool Definitions ===

class GetStockSentimentInput(BaseModel):
    symbol: str = Field(description="Stock ticker symbol (e.g., AAPL)")

@tool(args_schema=GetStockSentimentInput)
def get_stock_sentiment(symbol: str) -> str:
    """
    Get market sentiment for a stock from recent news.
    
    Sentiment ranges from -1.0 (very negative) to +1.0 (very positive).
    Requires FINNHUB_API_KEY environment variable.
    """
    try:
        api_key = os.getenv("FINNHUB_API_KEY")
        if not api_key:
            raise ValueError("FINNHUB_API_KEY not set")
        
        import requests
        response = requests.get(
            "https://finnhub.io/api/v1/news-sentiment",
            params={"symbol": symbol.upper(), "token": api_key},
            timeout=10
        )
        
        if response.ok:
            data = response.json()
            score = data.get("companyNewsScore", 0)
            logger.info(f"Sentiment for {symbol}: {score:.2f}")
            return f"Sentiment score: {score:.2f} (range: -1.0 to +1.0)"
        else:
            logger.error(f"API error: {response.status_code}")
            return "Sentiment unavailable - API error"
            
    except Exception as e:
        logger.error(f"Error getting sentiment: {e}")
        return f"Error: {str(e)}"

class GetStockPriceInput(BaseModel):
    symbol: str = Field(description="Stock ticker symbol")

@tool(args_schema=GetStockPriceInput)
def get_stock_price(symbol: str) -> str:
    """
    Get real-time stock price and OHLCV data.
    
    Returns open, high, low, close prices and volume.
    Requires POLYGON_API_KEY environment variable.
    """
    try:
        api_key = os.getenv("POLYGON_API_KEY")
        if not api_key:
            raise ValueError("POLYGON_API_KEY not set")
        
        import requests
        response = requests.get(
            f"https://api.polygon.io/v2/aggs/ticker/{symbol.upper()}/prev",
            params={"apiKey": api_key},
            timeout=10
        )
        
        if response.ok and response.json().get("results"):
            r = response.json()["results"][0]
            logger.info(f"Price for {symbol}: ${r['c']:.2f}")
            return (
                f"${symbol.upper()}: "
                f"Open=${r['o']:.2f} High=${r['h']:.2f} "
                f"Low=${r['l']:.2f} Close=${r['c']:.2f} "
                f"Volume={r['v']:,.0f}"
            )
        else:
            return "Price unavailable - no data"
            
    except Exception as e:
        logger.error(f"Error getting price: {e}")
        return f"Error: {str(e)}"

class GetTechnicalInput(BaseModel):
    symbol: str = Field(description="Stock ticker symbol")
    indicator: str = Field(
        default="SMA",
        description="Technical indicator: SMA, RSI, MACD, BBANDS"
    )

@tool(args_schema=GetTechnicalInput)
def get_technical_analysis(symbol: str, indicator: str = "SMA") -> str:
    """
    Get technical analysis indicators.
    
    Supported: SMA (Simple Moving Average), RSI (Relative Strength),
    MACD (Moving Average Convergence), BBANDS (Bollinger Bands)
    Requires ALPHA_VANTAGE_API_KEY environment variable.
    """
    try:
        api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        if not api_key:
            raise ValueError("ALPHA_VANTAGE_API_KEY not set")
        
        import requests
        response = requests.get(
            "https://www.alphavantage.co/query",
            params={
                "function": indicator,
                "symbol": symbol.upper(),
                "interval": "daily",
                "apikey": api_key
            },
            timeout=10
        )
        
        if response.ok:
            data = response.json()
            if "Error Message" in data:
                return f"API error: {data['Error Message']}"
            logger.info(f"Technical analysis for {symbol}: {indicator}")
            return json.dumps(data, indent=2)[:500]  # Truncate for brevity
        else:
            return "Technical data unavailable"
            
    except Exception as e:
        logger.error(f"Error getting technical analysis: {e}")
        return f"Error: {str(e)}"

# === Memory Initialization (Optional) ===

def init_redis_memory() -> Optional[callable]:
    """Initialize Redis memory if available."""
    if not REDIS_AVAILABLE:
        logger.warning("Redis not available - using in-memory storage")
        return None
    
    try:
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        pool = redis.ConnectionPool.from_url(
            redis_url,
            max_connections=10,
            decode_responses=True
        )
        redis_client = redis.Redis(connection_pool=pool)
        redis_client.ping()
        logger.info("Redis connection established")
        
        def get_history(session_id: str):
            return RedisChatMessageHistory(
                session_id=f"stock_agent:{session_id}",
                url=redis_url,
                key_prefix="agent:memory:",
                ttl=int(os.getenv("SESSION_TTL", 3600))
            )
        
        return get_history
        
    except Exception as e:
        logger.error(f"Redis initialization failed: {e}")
        logger.warning("Falling back to in-memory storage")
        return None

# === Agent Setup ===

logger.info("Initializing stock sentiment agent...")

# Tool list
tools = [get_stock_sentiment, get_stock_price, get_technical_analysis]

# Create agent
agent = create_react_agent(
    model="anthropic:claude-sonnet-4-20250514",
    tools=tools,
    prompt="""You are an expert stock analyst. When analyzing stocks:

1. Always check sentiment first to understand market perception
2. Get real-time prices to confirm current valuation
3. Use technical indicators to identify trends
4. Provide balanced analysis considering all three data points
5. Clearly state any limitations (missing data, API errors)

When the user asks about a stock, gather all available data before providing analysis."""
)

# Optional: Add Redis memory
memory_accessor = init_redis_memory()

if memory_accessor and REDIS_AVAILABLE:
    agent_with_memory = RunnableWithMessageHistory(
        agent,
        get_session_history=memory_accessor,
        input_messages_key="messages",
        history_messages_key="history"
    )
    logger.info("Agent initialized with Redis memory")
else:
    agent_with_memory = agent
    logger.warning("Agent initialized without persistent memory")

# === Main Execution ===

async def analyze_stock(symbol: str, session_id: str = "default") -> dict:
    """Analyze a stock using the agent."""
    logger.info(f"Analyzing {symbol}...")
    
    try:
        user_message = f"Analyze {symbol} stock comprehensively. Consider sentiment, price, and technical indicators."
        
        config = {"configurable": {"thread_id": session_id}} if session_id else {}
        
        result = await agent_with_memory.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            },
            config=config
        )
        
        logger.info(f"Analysis complete for {symbol}")
        return result
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        return {"error": str(e), "symbol": symbol}

if __name__ == "__main__":
    # Get stock symbol from command line or use default
    symbol = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    session = os.getenv("SESSION_ID", f"session_{symbol}")
    
    # Run analysis
    result = asyncio.run(analyze_stock(symbol, session_id=session))
    
    # Pretty print result
    print("\n" + "="*60)
    print(f"ANALYSIS RESULT FOR {symbol.upper()}")
    print("="*60)
    print(json.dumps(result, indent=2, default=str))
    print("="*60 + "\n")
