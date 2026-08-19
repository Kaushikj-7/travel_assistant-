"""
Retrieval Agent — Agentsway Methodology (2510.23664v1) & MCC Protocol (2510.19856v1).

Role:
- Interacts with ChromaDB / Chroma Cloud via MCP Client
- Evaluates semantic cosine distance & knowledge availability (The Switch)
- Enforces guardrail pass-through and short-circuiting on invalid inputs
- Synthesizes verified local knowledge chunks into travel guides
"""

from datetime import datetime
from typing import Dict, Any
from langchain_core.messages import HumanMessage
from mcp_server.client import mcp_client


class RetrievalAgent:
    """Agent responsible for vector store retrieval and semantic decision routing."""

    def __init__(self, llm=None):
        self.llm = llm

    def check_knowledge_availability(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute MCP query_vectorstore tool and decide routing."""
        city = state.get("city", "")
        is_valid = state.get("is_valid_destination", True)

        # ── Guardrail check ──────────────────────────────────────────
        if not is_valid:
            trace_entry = {
                "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
                "node": "RetrievalAgent.check_knowledge",
                "agent_role": "Retrieval & Guardrail Routing",
                "action": f"⚠️ Input Guardrail Rejection: '{city}' is not a valid destination. Bypassing tool execution.",
                "details": {
                    "city": city,
                    "is_valid_destination": False,
                    "guardrail_error": state.get("guardrail_error"),
                    "route_decision": "guardrail_rejected"
                }
            }
            return {
                "source": "guardrail_rejected",
                "city_info": "",
                "execution_trace": [trace_entry],
            }

        # Invoke MCP Server Tool
        mcp_res = mcp_client.execute_tool("query_vectorstore", {"query": city, "n_results": 5})
        raw_data = mcp_res.get("raw_data", {})

        found_city = raw_data.get("found_city")
        dists = raw_data.get("distances", [])
        top_dist = dists[0] if dists else "N/A"

        if found_city:
            source = "vectorstore"
            city_info = "\n\n".join(raw_data.get("documents", []))
            action_desc = f"Verified local knowledge for '{city}' in ChromaDB (top distance: {top_dist}). Routing to Vector Store path."
        else:
            source = "websearch"
            city_info = ""
            action_desc = f"'{city}' not found in ChromaDB. The Switch dynamically routes to Web Research Agent."

        trace_entry = {
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "node": "RetrievalAgent.check_knowledge",
            "agent_role": "Retrieval & Routing",
            "action": action_desc,
            "details": {
                "mcp_server": "TravelMCPServer",
                "mcp_tool": "query_vectorstore",
                "cosine_distance": top_dist,
                "route_decision": source,
                "chunks_count": len(raw_data.get("documents", [])),
            }
        }

        return {
            "source": source,
            "city_info": city_info,
            "execution_trace": [trace_entry],
        }

    def synthesize_knowledge(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize retrieved vector store knowledge into an engaging summary."""
        city = state.get("city", "")
        city_info = state.get("city_info", "")

        # Preserve summary on follow-up (Distinction 3)
        existing = state.get("city_summary", "")
        if state.get("is_weather_followup") and existing:
            trace_entry = {
                "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
                "node": "RetrievalAgent.synthesize",
                "agent_role": "Retrieval & Synthesis",
                "action": f"Preserved existing summary for '{city}' (Distinction 3: Context Memory).",
                "details": {"summary_length": len(existing)}
            }
            return {"city_summary": existing, "execution_trace": [trace_entry]}

        summary = ""
        llm_used = False
        if self.llm and city_info:
            try:
                prompt = (
                    f"You are the Retrieval Agent in an AI agent team. Based on the verified ChromaDB facts for {city}, "
                    f"write a rich 2-3 paragraph travel summary highlighting iconic landmarks, cuisine, and culture.\n\n"
                    f"Context:\n{city_info}"
                )
                res = self.llm.invoke([HumanMessage(content=prompt)])
                summary = res.content
                llm_used = True
            except Exception as e:
                import logging
                logging.getLogger("travel_agent").warning(f"LLM synthesis failed for {city}: {e}")

        if not summary:
            paragraphs = [p.strip() for p in city_info.split("\n\n") if p.strip()]
            summary = "\n\n".join(paragraphs[:3]) if paragraphs else f"Verified destination guide for {city}."

        trace_entry = {
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "node": "RetrievalAgent.synthesize",
            "agent_role": "Retrieval & Synthesis",
            "action": f"Synthesized verified destination guide for '{city}'.",
            "details": {"llm_used": llm_used, "summary_length": len(summary)}
        }

        return {"city_summary": summary, "execution_trace": [trace_entry]}
