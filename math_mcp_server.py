import asyncio
import os
import logging
from fastmcp import FastMCP

# 1) Configure Python logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("demo-server")

mcp = FastMCP("Math-Server 🚀")
#### Tools ####
# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print(f"Adding {a} and {b}")
    return a + b

# More tools can be added here

#### Resources ####
# Add a static resource
@mcp.resource("resource://some_static_resource")
def get_static_resource() -> str:
    """Static resource data"""
    return "Any static data can be returned"


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


#### Prompts ####
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"


@mcp.prompt()
def debug_error(error: str) -> list[tuple]:
    return [
        ("user", "I'm seeing this error:"),
        ("user", error),
        ("assistant", "I'll help debug that. What have you tried so far?"),
    ]


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b


if __name__ == "__main__":
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 8001))
    # Decide your SSE endpoint here:
    endpoint = "/events"

    # 2) Your startup message
    logger.debug(f"🚀 Starting FastMCP SSE server on http://{host}:{port}{endpoint}")

    # 3) Lower-case log_level
    asyncio.run(
        mcp.run_sse_async(
            host=host,
            port=port,
        )
    )  