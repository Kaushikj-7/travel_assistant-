"""
Web Research Agent — Agentsway Methodology (2510.23664v1) & MCP Protocol.

Role:
- Executes dynamic web intelligence search when unknown cities are encountered
- 🏆 Distinction 1: Manual Transmission Tool Execution over MCP
- Manually handles LLM tool binding, tool_calls inspection, and ToolMessage creation
"""

import time
from datetime import datetime
from typing import Dict, Any
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from mcp_server.client import mcp_client
from tools.search import search_web
from utils.logger import logger


class WebResearchAgent:
    """Agent responsible for live web research with raw MCP tool execution protocol."""

    def __init__(self, llm=None):
        self.llm = llm

    def execute_research(self, state: Dict[str, Any]) -> Dict[str, Any]:
        city = state.get("city", "")

        # Preserve summary on follow-up (Distinction 3)
        existing = state.get("city_summary", "")
        if state.get("is_weather_followup") and existing:
            trace_entry = {
                "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
                "node": "WebResearchAgent",
                "agent_role": "Web Intelligence",
                "action": f"Preserved existing summary for '{city}' (Distinction 3: Context Memory).",
                "details": {"summary_length": len(existing)}
            }
            return {"city_summary": existing, "execution_trace": [trace_entry]}

        search_result = ""
        summary = ""
        tool_calls_payload = []
        tool_messages = []
        ai_msg = None

        if self.llm:
            try:
                # 1. Bind search tool to LLM
                llm_with_tools = self.llm.bind_tools([search_web])

                # 2. Invoke LLM to generate tool call
                ai_msg = llm_with_tools.invoke([
                    SystemMessage(content="You are the Web Research Agent. Use the search_web tool to look up destination insights."),
                    HumanMessage(content=f"Research travel information and sights in {city}"),
                ])

                # 3. Distinction 1: Manual Transmission over MCP
                if hasattr(ai_msg, "tool_calls") and ai_msg.tool_calls:
                    for call in ai_msg.tool_calls:
                        t_name = call.get("name")
                        t_args = call.get("args", {})
                        t_id = call.get("id", "call_mcp_search_1")
                        tool_calls_payload.append({"tool": t_name, "arguments": t_args, "id": t_id})

                        # Execute via MCP Client
                        mcp_res = mcp_client.execute_tool("search_web", t_args)
                        search_result = mcp_res.get("raw_data", "")

                        tool_messages.append(
                            ToolMessage(content=str(search_result), tool_call_id=t_id, name=t_name)
                        )
                else:
                    mcp_res = mcp_client.execute_tool("search_web", {"query": city})
                    search_result = mcp_res.get("raw_data", "")

                # 4. Synthesize summary
                synth_prompt = (
                    f"You are the Web Research Agent. Synthesize the following web intelligence for {city} "
                    f"into an engaging, informative 2-3 paragraph travel summary:\n\n{search_result}"
                )
                res = self.llm.invoke([HumanMessage(content=synth_prompt)])
                summary = res.content
            except Exception as e:
                logger.warning(f"LLM tool execution failed: {e}")

        if not search_result:
            from langchain_core.messages import AIMessage
            call_id = f"manual_call_{int(time.time())}"
            ai_msg_fallback = AIMessage(
                content="",
                tool_calls=[{"name": "search_web", "args": {"query": city}, "id": call_id}]
            )
            tool_calls_payload.append({"tool": "search_web", "arguments": {"query": city}, "id": call_id})
            mcp_res = mcp_client.execute_tool("search_web", {"query": city})
            search_result = mcp_res.get("raw_data", "")
            tool_messages.append(
                ToolMessage(content=str(search_result), tool_call_id=call_id, name="search_web")
            )
            ai_msg = ai_msg_fallback
            summary = search_result

        trace_entry = {
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "node": "WebResearchAgent",
            "agent_role": "Web Intelligence & Manual MCP Protocol",
            "action": f"Executed Manual Transmission tool protocol for search_web('{city}') via MCP (Distinction 1).",
            "details": {
                "mcp_server": "TravelMCPServer",
                "tool_calls": tool_calls_payload,
                "tool_messages_count": len(tool_messages),
                "search_preview": f"{search_result[:140]}...",
            }
        }

        new_msgs = ([ai_msg] if ai_msg else []) + tool_messages

        return {
            "city_info": search_result,
            "city_summary": summary,
            "execution_trace": [trace_entry],
            "messages": new_msgs if new_msgs else [],
        }
