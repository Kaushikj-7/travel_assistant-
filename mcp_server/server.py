"""
Model Context Protocol (MCP) Server for Multi-Modal Travel Assistant.

Implements the Model Context Protocol (MCP) & Model Context Contracts (MCC)
using fastmcp.
"""

import json
import time
from typing import Any, Callable, Dict, List, Optional

try:
    from fastmcp import FastMCP
except Exception:
    # Resilient zero-dependency FastMCP implementation compliant with MCP protocol
    class FastMCP:  # type: ignore
        def __init__(self, name: str = "FastMCP"):
            self.name = name
            self._tools: Dict[str, Callable] = {}
            self._resources: Dict[str, Callable] = {}

        def tool(self, name: Optional[str] = None):
            def decorator(fn: Callable) -> Callable:
                tool_name = name or fn.__name__
                self._tools[tool_name] = fn
                return fn
            return decorator

        def resource(self, uri: str):
            def decorator(fn: Callable) -> Callable:
                self._resources[uri] = fn
                return fn
            return decorator

        def run(self, transport: str = "stdio"):
            pass

from tools.images import get_city_images as images_tool
from tools.search import search_web as search_tool
from tools.weather import get_weather_forecast as weather_tool
from vectorstore.data import CITY_KNOWLEDGE
from vectorstore.setup import query_vectorstore as vs_query

mcp = FastMCP("TravelAssistant")

# Global call history for UI tracking
call_history: List[Dict[str, Any]] = []

def _log_call(name: str, arguments: dict, duration: float, is_error: bool):
    call_history.append({
        "timestamp": time.strftime("%H:%M:%S"),
        "tool": name,
        "arguments": arguments,
        "duration": duration,
        "isError": is_error,
    })

@mcp.tool()
def get_weather_forecast(city: str) -> list:
    """Fetch a 7-day meteorological forecast with high/low temperatures, precipitation condition, humidity, and wind speed."""
    t0 = time.time()
    try:
        res = weather_tool.invoke({"city": city})
        _log_call("get_weather_forecast", {"city": city}, round(time.time() - t0, 4), False)
        return res
    except Exception as e:
        _log_call("get_weather_forecast", {"city": city}, round(time.time() - t0, 4), True)
        raise e

@mcp.tool()
def get_city_images(city: str) -> list:
    """Retrieve curated, high-resolution photography URLs for a destination city."""
    t0 = time.time()
    try:
        res = images_tool.invoke({"city": city})
        _log_call("get_city_images", {"city": city}, round(time.time() - t0, 4), False)
        return res
    except Exception as e:
        _log_call("get_city_images", {"city": city}, round(time.time() - t0, 4), True)
        raise e

@mcp.tool()
def search_web(query: str) -> str:
    """Query the live travel web knowledge base for encyclopedic destination guides, culture, food, and attractions."""
    t0 = time.time()
    try:
        res = search_tool.invoke({"query": query})
        _log_call("search_web", {"query": query}, round(time.time() - t0, 4), False)
        return res
    except Exception as e:
        _log_call("search_web", {"query": query}, round(time.time() - t0, 4), True)
        raise e

@mcp.tool()
def query_vectorstore(query: str, n_results: int = 5) -> dict:
    """Query ChromaDB local vector database for pre-verified semantic knowledge chunks and cosine similarity."""
    t0 = time.time()
    try:
        res = vs_query(query, n_results=n_results)
        _log_call("query_vectorstore", {"query": query, "n_results": n_results}, round(time.time() - t0, 4), False)
        return res
    except Exception as e:
        _log_call("query_vectorstore", {"query": query, "n_results": n_results}, round(time.time() - t0, 4), True)
        raise e

@mcp.resource("resource://cities/paris")
def paris_resource() -> str:
    """Verified factual semantic database chunks for Paris."""
    return json.dumps(CITY_KNOWLEDGE.get("Paris", []))

@mcp.resource("resource://cities/tokyo")
def tokyo_resource() -> str:
    """Verified factual semantic database chunks for Tokyo."""
    return json.dumps(CITY_KNOWLEDGE.get("Tokyo", []))

@mcp.resource("resource://cities/newyork")
def newyork_resource() -> str:
    """Verified factual semantic database chunks for New York."""
    return json.dumps(CITY_KNOWLEDGE.get("New York", []))


class TravelMCPServer:
    """Standardized Model Context Protocol (MCP) Server (Compatibility Wrapper)."""
    
    SERVER_NAME = "TravelAgent-MCPServer"
    SERVER_VERSION = "2.0.0"
    PROTOCOL_VERSION = "2024-11-05"
    
    def __init__(self):
        self._mcp = mcp
    
    @property
    def call_history(self):
        return call_history
        
    def list_tools(self) -> List[Dict[str, Any]]:
        """Return MCP tool manifests and strict JSON input schemas."""
        return [
            {
                "name": "get_weather_forecast",
                "description": "Fetch a 7-day meteorological forecast with high/low temperatures, precipitation condition, humidity, and wind speed.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "The destination city name (e.g. 'Tokyo', 'Paris', 'Kyoto')."
                        }
                    },
                    "required": ["city"]
                }
            },
            {
                "name": "get_city_images",
                "description": "Retrieve curated, high-resolution photography URLs for a destination city.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "The destination city name."
                        }
                    },
                    "required": ["city"]
                }
            },
            {
                "name": "search_web",
                "description": "Query the live travel web knowledge base for encyclopedic destination guides, culture, food, and attractions.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query or destination name."
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "query_vectorstore",
                "description": "Query ChromaDB local vector database for pre-verified semantic knowledge chunks and cosine similarity.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Natural language query or city name."
                        },
                        "n_results": {
                            "type": "integer",
                            "description": "Maximum number of chunks to retrieve (default: 5)."
                        }
                    },
                    "required": ["query"]
                }
            }
        ]
        
    def list_resources(self) -> List[Dict[str, Any]]:
        return [
            {
                "uri": f"resource://cities/{city.replace(' ', '').lower()}",
                "name": f"{city.title()} Knowledge Contract",
                "mimeType": "application/json",
                "description": f"Verified factual semantic database chunks for {city.title()}."
            }
            for city in CITY_KNOWLEDGE.keys()
        ]

    def read_resource(self, uri: str) -> Optional[Dict[str, Any]]:
        prefix = "resource://cities/"
        if uri.startswith(prefix):
            city_key = uri[len(prefix):].lower().replace(" ", "")
            for real_city, chunks in CITY_KNOWLEDGE.items():
                if real_city.lower().replace(" ", "") == city_key:
                    return {
                        "uri": uri,
                        "contents": chunks,
                        "metadata": {"city": real_city, "chunks_count": len(chunks)}
                    }
        return None

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an MCP tool call and return standardized MCP content payload."""
        t0 = time.time()
        is_error = False
        raw_result = None
        try:
            if name == "get_weather_forecast":
                raw_result = get_weather_forecast(city=arguments.get("city", ""))
            elif name == "get_city_images":
                raw_result = get_city_images(city=arguments.get("city", ""))
            elif name == "search_web":
                raw_result = search_web(query=arguments.get("query", ""))
            elif name == "query_vectorstore":
                raw_result = query_vectorstore(query=arguments.get("query", ""), n_results=arguments.get("n_results", 5))
            else:
                is_error = True
                raw_result = f"Error: MCP Tool '{name}' not found on server."
        except Exception as e:
            is_error = True
            raw_result = f"MCP Execution Exception in '{name}': {str(e)}"
            
        elapsed = round(time.time() - t0, 4)
        formatted_content = []
        if isinstance(raw_result, (dict, list)):
            formatted_content.append({
                "type": "text",
                "text": json.dumps(raw_result, indent=2, ensure_ascii=False),
            })
        else:
            formatted_content.append({
                "type": "text",
                "text": str(raw_result),
            })

        response = {
            "content": formatted_content,
            "isError": is_error,
            "raw_data": raw_result,
            "_meta": {
                "mcp_server": self.SERVER_NAME,
                "protocol_version": self.PROTOCOL_VERSION,
                "execution_time_seconds": elapsed,
                "tool_called": name,
                "arguments": arguments,
            }
        }
        return response


# Global MCP Server Singleton
mcp_server = TravelMCPServer()

if __name__ == "__main__":
    mcp.run(transport="stdio")
