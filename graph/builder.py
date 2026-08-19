"""
LangGraph compilation — constructs the Multi-Modal Agentic Workflow.

Topology:
    START
      │
      ▼
  parse_input (PlanningAgent + Input Guardrail)
      │
      ▼
check_knowledge (RetrievalAgent)
      │
  [Conditional Edge: The Switch]
      ├── vectorstore_retrieve ─┐
      ├── web_search ───────────┤
      └── aggregate_response ───┤ (Guardrail Rejection short-circuit)
                                │
                        [Parallel Fan-Out]
                                ├── fetch_weather ─┐
                                └── fetch_images ──┤
                                                   │
                                            [Fan-In Join]
                                                   │
                                                   ▼
                                           aggregate_response (GovernanceAgent)
                                                   │
                                                   ▼
                                                  END

Distinctions Implemented:
  🏆 Distinction 1: Manual tool protocol in `web_search` node
  🏆 Distinction 2: Parallel async/concurrent fan-out of weather + images
  🏆 Distinction 3: State persistence with MemorySaver checkpointer
"""

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
import os
import contextlib

# Try to import PostgresSaver for industrial persistence
try:
    from langgraph.checkpoint.postgres import PostgresSaver
    from psycopg import Connection
    HAS_POSTGRES = True
except ImportError:
    HAS_POSTGRES = False

from graph.state import AgentState
from graph.nodes import (
    parse_input,
    check_knowledge,
    vectorstore_retrieve,
    web_search,
    fetch_weather,
    fetch_images,
    aggregate_response,
)
from graph.edges import route_by_knowledge


def build_graph(conn=None):
    """Build and compile the multi-modal travel assistant StateGraph with memory checkpointer."""
    workflow = StateGraph(AgentState)

    # ── 1. Register all nodes ─────────────────────────────────────────
    workflow.add_node("parse_input", parse_input)
    workflow.add_node("check_knowledge", check_knowledge)
    workflow.add_node("vectorstore_retrieve", vectorstore_retrieve)
    workflow.add_node("web_search", web_search)
    workflow.add_node("fetch_weather", fetch_weather)
    workflow.add_node("fetch_images", fetch_images)
    workflow.add_node("aggregate_response", aggregate_response)

    # ── 2. Sequential pipeline start ──────────────────────────────────
    workflow.add_edge(START, "parse_input")
    workflow.add_edge("parse_input", "check_knowledge")

    # ── 3. Conditional Edge: The "Switch" + Guardrail Short-Circuit ───
    workflow.add_conditional_edges(
        "check_knowledge",
        route_by_knowledge,
        {
            "vectorstore_retrieve": "vectorstore_retrieve",
            "web_search": "web_search",
            "aggregate_response": "aggregate_response",
        },
    )

    # ── 4. Parallel Fan-Out (Distinction 2) ────────────────────────────
    workflow.add_edge("vectorstore_retrieve", "fetch_weather")
    workflow.add_edge("vectorstore_retrieve", "fetch_images")
    workflow.add_edge("web_search", "fetch_weather")
    workflow.add_edge("web_search", "fetch_images")

    # ── 5. Fan-In Synchronization (Join) ──────────────────────────────
    workflow.add_edge("fetch_weather", "aggregate_response")
    workflow.add_edge("fetch_images", "aggregate_response")

    # ── 6. Pipeline Termination ───────────────────────────────────────
    workflow.add_edge("aggregate_response", END)

    # ── 7. Compile with Checkpointer (Distinction 3) ──────────────────
    if conn and HAS_POSTGRES:
        checkpointer = PostgresSaver(conn)
        checkpointer.setup()
        return workflow.compile(checkpointer=checkpointer)
    else:
        checkpointer = MemorySaver()
        return workflow.compile(checkpointer=checkpointer)
