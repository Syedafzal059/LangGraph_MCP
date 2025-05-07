import asyncio
import os
import logging
from fastmcp import FastMCP

# 1) Configure Python logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("weather-server")

# 2) Create the MCP server instance
mcp = FastMCP("Weather Server 🚀")

#### Tools ####

@mcp.tool()
def get_current_weather(location: str) -> dict:
    """
    Return dummy current weather for a given location.
    """
    # In a real server you'd call a weather API here.
    return {
        "location": location,
        "temperature_c": 25,
        "condition": "Sunny",
        "humidity_pct": 40,
    }

@mcp.tool()
def get_forecast(location: str, days: int) -> list[dict]:
    """
    Return a dummy multi-day forecast.
    """
    dummy_conditions = ["Sunny", "Partly Cloudy", "Rain", "Thunderstorms"]
    forecast = []
    for i in range(1, days + 1):
        forecast.append({
            "day": f"Day {i}",
            "location": location,
            "high_c": 20 + i,
            "low_c": 10 + i,
            "condition": dummy_conditions[i % len(dummy_conditions)],
        })
    return forecast

if __name__ == "__main__":
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 8002))
    endpoint = "/events"  # SSE endpoint

    logger.debug(f"🚀 Starting FastMCP SSE Weather Server on http://{host}:{port}{endpoint}")

    # 3) Run the server over SSE
    asyncio.run(
        mcp.run_sse_async(
            host=host,
            port=port,
        )
    )
