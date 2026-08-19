"""
MCP Client Bridge — In-Process Direct Invocation.

NOTE: This client connects directly to the FastMCP server tools
within the same process for zero-latency execution. In a production
deployment, this would use stdio/SSE transport to a separate MCP
server process.
"""

from typing import Dict, Any, List, Optional
from mcp_server.server import mcp_server, TravelMCPServer


class MCPClientBridge:
    """Client for interacting with MCP Servers."""

    def __init__(self, server: TravelMCPServer = mcp_server):
        self.server = server

    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Discover tools exposed by the MCP Server."""
        return self.server.list_tools()

    def get_available_resources(self) -> List[Dict[str, Any]]:
        """Discover MCC knowledge resources exposed by the MCP Server."""
        return self.server.list_resources()

    def read_resource(self, uri: str) -> Optional[Dict[str, Any]]:
        """Read MCC resource content by URI."""
        return self.server.read_resource(uri)

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke an MCP tool through standard MCP protocol."""
        return self.server.call_tool(tool_name, arguments)

    def get_call_history(self) -> List[Dict[str, Any]]:
        """Retrieve recent MCP tool call transactions."""
        return self.server.call_history


# Global MCP Client Singleton
mcp_client = MCPClientBridge()
