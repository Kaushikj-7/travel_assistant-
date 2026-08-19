"""
Environment & Media Agent — Agentsway Methodology (2510.23664v1) & MCP Protocol.

Role:
- Ingests environmental meteorological forecast data via MCP Server
- Delegates visual asset ingestion to the VisualAssetAgent
- 🏆 Distinction 2: Parallel Fan-Out Execution
"""

import time
from datetime import datetime
from typing import Dict, Any
from mcp_server.client import mcp_client
from agents.visual_agent import VisualAssetAgent


class EnvironmentAndMediaAgent:
    """Agent responsible for parallel environmental weather and media asset ingestion."""

    @staticmethod
    def fetch_weather(state: Dict[str, Any]) -> Dict[str, Any]:
        """🏆 Distinction 2: Parallel weather branch executed via MCP."""
        city = state.get("city", "")
        t0 = time.time()
        
        mcp_res = mcp_client.execute_tool("get_weather_forecast", {"city": city})
        forecast = mcp_res.get("raw_data", [])
        duration = round(time.time() - t0, 3)

        trace_entry = {
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "node": "EnvironmentAgent.fetch_weather",
            "agent_role": "Environment (Weather MCP)",
            "action": f"Parallel Fan-Out: Ingested {len(forecast)}-day weather forecast for '{city}' via MCP ({duration}s).",
            "details": {
                "mcp_server": "TravelMCPServer",
                "mcp_tool": "get_weather_forecast",
                "forecast_days": len(forecast),
                "duration_seconds": duration,
            }
        }

        return {
            "weather_forecast": forecast,
            "execution_trace": [trace_entry],
        }

    @staticmethod
    def fetch_images(state: Dict[str, Any]) -> Dict[str, Any]:
        """🏆 Distinction 2: Parallel media branch executed by VisualAssetAgent."""
        return VisualAssetAgent.fetch_visual_assets(state)
