# Tool Definitions Reference

## Pre-Built Tool Library

### Web Search (Tavily)
**When to use**: General web search, recent news, current information

```python
from langchain_tavily import TavilySearch

tavily = TavilySearch(
    max_results=5,
    topic="general"  # or "finance" for financial focus
)

result = tavily.results(
    query="latest AI trends",
    include_answer=True,
    include_raw_content=False
)
```

**Environment**: `TAVILY_API_KEY`

**Cost**: Free tier available (limited queries)

---

### Stock Sentiment (Finnhub)
**When to use**: Market sentiment, news impact, investor mood

```python
from langchain_core.tools import tool
import requests, os

@tool
def get_stock_sentiment(symbol: str) -> str:
    """Get sentiment score for a stock from recent news."""
    api_key = os.getenv("FINNHUB_API_KEY")
    if not api_key:
        raise ValueError("FINNHUB_API_KEY required")
    
    response = requests.get(
        "https://finnhub.io/api/v1/news-sentiment",
        params={"symbol": symbol, "token": api_key}
    )
    if response.ok:
        data = response.json()
        score = data.get("companyNewsScore", 0)
        return f"Sentiment: {score:.2f} (range: -1.0 to +1.0)"
    return "Sentiment unavailable"
```

**Environment**: `FINNHUB_API_KEY` (https://finnhub.io)

**Cost**: Free tier available

---

### Real-Time Prices (Polygon.io)
**When to use**: Current stock prices, OHLCV data, volume

```python
@tool
def get_stock_price(symbol: str) -> str:
    """Get real-time stock price from Polygon.io."""
    api_key = os.getenv("POLYGON_API_KEY")
    if not api_key:
        raise ValueError("POLYGON_API_KEY required")
    
    response = requests.get(
        f"https://api.polygon.io/v2/aggs/ticker/{symbol}/prev",
        params={"apiKey": api_key}
    )
    if response.ok and response.json().get("results"):
        r = response.json()["results"][0]
        return (
            f"${symbol}: O=${r['o']:.2f} C=${r['c']:.2f} "
            f"H=${r['h']:.2f} L=${r['l']:.2f} V={r['v']:,.0f}"
        )
    return "Price unavailable"
```

**Environment**: `POLYGON_API_KEY` (https://polygon.io)

**Cost**: Free tier with rate limits

---

### Technical Analysis (Alpha Vantage)
**When to use**: Moving averages, RSI, MACD, Bollinger Bands

```python
@tool
def get_technical_indicator(symbol: str, indicator: str = "SMA") -> str:
    """Get technical indicator for a stock."""
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        raise ValueError("ALPHA_VANTAGE_API_KEY required")
    
    endpoint = f"https://www.alphavantage.co/query"
    params = {
        "function": indicator,  # "SMA", "RSI", "MACD", "BBANDS"
        "symbol": symbol,
        "interval": "daily",
        "apikey": api_key
    }
    response = requests.get(endpoint, params=params)
    if response.ok:
        return str(response.json())
    return "Indicator unavailable"
```

**Environment**: `ALPHA_VANTAGE_API_KEY` (https://alphavantage.co)

**Cost**: Free tier (5 req/min)

---

### Financial Data (IEX Cloud)
**When to use**: Company fundamentals, earnings, dividends, balance sheet

```python
@tool
def get_company_fundamentals(symbol: str) -> str:
    """Get company financials from IEX Cloud."""
    api_key = os.getenv("IEX_CLOUD_API_KEY")
    if not api_key:
        raise ValueError("IEX_CLOUD_API_KEY required")
    
    response = requests.get(
        f"https://cloud.iexapis.com/stable/stock/{symbol}/quote",
        params={"token": api_key}
    )
    if response.ok:
        data = response.json()
        return (
            f"PE={data['peRatio']} EPS=${data['latestEPS']} "
            f"MktCap=${data['marketCap']:,} Div=${data['dividendRate']}"
        )
    return "Fundamentals unavailable"
```

**Environment**: `IEX_CLOUD_API_KEY` (https://iexcloud.io)

**Cost**: Free tier available

---

### Custom REST API
**When to use**: Proprietary APIs, internal services, specialized data sources

```python
from pydantic import BaseModel, Field

class CustomAPIInput(BaseModel):
    query: str = Field(description="Query to send to API")
    limit: int = Field(default=10, description="Result limit")

@tool(args_schema=CustomAPIInput)
def query_custom_api(query: str, limit: int = 10) -> str:
    """Query custom REST API."""
    api_key = os.getenv("CUSTOM_API_KEY")
    auth_header = {"Authorization": f"Bearer {api_key}"}
    
    response = requests.get(
        "https://api.example.com/search",
        params={"q": query, "limit": limit},
        headers=auth_header,
        timeout=10
    )
    
    if response.ok:
        return response.json()
    raise ValueError(f"API error: {response.status_code}")
```

---

## Tool Combination Patterns

### Stock Research Agent
Combines sentiment + price + technical:
```python
tools = [get_stock_sentiment, get_stock_price, get_technical_indicator]
```

### Fundamental Value Agent
Combines price + fundamentals + dividends:
```python
tools = [get_stock_price, get_company_fundamentals, search_news]
```

### Multi-Stock Portfolio Agent
Tracks multiple symbols with historical data:
```python
tools = [
    get_stock_price,
    get_historical_prices,
    calculate_portfolio_metrics,
    identify_correlation
]
```

## Environment Variable Setup

Create `.env` file in agent directory:

```bash
# Required for agent to function
export FINNHUB_API_KEY="your_key_here"
export POLYGON_API_KEY="your_key_here"
export ALPHA_VANTAGE_API_KEY="your_key_here"
export TAVILY_API_KEY="your_key_here"

# Optional for Redis memory
export REDIS_URL="redis://localhost:6379/0"

# Optional for logging
export LOG_LEVEL="INFO"
```

Load in Python:
```python
import os
from dotenv import load_dotenv

load_dotenv()  # Reads .env file

api_key = os.getenv("FINNHUB_API_KEY")
if not api_key:
    raise ValueError("FINNHUB_API_KEY not set in environment")
```

## Custom Tool Template

For any specialized requirement:

```python
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from typing import Literal
import logging

logger = logging.getLogger(__name__)

class MyToolInput(BaseModel):
    param1: str = Field(description="First parameter")
    param2: Literal["option_a", "option_b"] = Field(description="Choice")
    param3: int = Field(default=10, ge=1, le=100)

@tool(args_schema=MyToolInput)
def my_custom_tool(param1: str, param2: str = "option_a", param3: int = 10) -> str:
    """
    Brief description of tool.
    
    This appears in agent's tool list and helps LLM understand when to call it.
    """
    try:
        # Your implementation here
        result = process(param1, param2, param3)
        logger.info(f"Tool called with {param1}")
        return result
    except Exception as e:
        logger.error(f"Tool error: {e}")
        return f"Error: {str(e)}"
```

### Key Design Principles

1. **Fail gracefully**: Return error strings, don't raise exceptions
2. **Document fully**: Clear docstrings help agent understand when to use
3. **Validate inputs**: Use Pydantic for type safety
4. **Log everything**: Track tool usage for debugging
5. **Use environment variables**: Never hardcode secrets
6. **Handle API errors**: Network calls always fail; plan for it
7. **Set reasonable timeouts**: Default 10-30 seconds depending on API
8. **Cache when possible**: Reduce redundant API calls with @cache decorator
